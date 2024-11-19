import psycopg2
from flask import jsonify
from flask_restful import Resource

from constants import TABLE_NAME, DB_CONFIG
from utils import db_connection, custom_response


def create_guests_table(cursor):
    """Creates the guests table if it doesn't already exist."""
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id SERIAL PRIMARY KEY,
            device_name VARCHAR(100) NOT NULL,
            mac_address VARCHAR(17) NOT NULL UNIQUE,
            last_seen TIMESTAMPTZ NOT NULL
        );
    """)


def create_update_last_seen_trigger(cursor):
    """Creates or replaces the update_last_seen trigger function and its trigger."""
    cursor.execute("""
        CREATE OR REPLACE FUNCTION update_last_seen()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.last_seen = current_timestamp;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)

    cursor.execute(f"""
        DO $$ BEGIN
            IF NOT EXISTS (
                SELECT FROM pg_trigger WHERE tgname = 'update_last_seen_trigger'
            ) THEN
                CREATE TRIGGER update_last_seen_trigger
                BEFORE UPDATE ON {TABLE_NAME}
                FOR EACH ROW
                EXECUTE FUNCTION update_last_seen();
            END IF;
        END $$;
    """)


def drop_guests_table(cursor):
    """Drops the guests table if it exists."""
    cursor.execute(f"DROP TABLE IF EXISTS {TABLE_NAME};")


def create_database_if_not_exists():
    """
    Attempt to connect to the target database. If it doesn't exist, connect to the default
    database (usually 'postgres') and create it.
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.close()
    except psycopg2.OperationalError as e:
        if "does not exist" in str(e):
            db_name = DB_CONFIG.get("dbname")
            host = DB_CONFIG.get("host", "localhost")
            user = DB_CONFIG.get("user")
            password = DB_CONFIG.get("password")
            port = DB_CONFIG.get("port", 5432)

            fallback_config = {
                "dbname": "postgres",
                "host": host,
                "user": user,
                "password": password,
                "port": port,
            }

            try:
                with psycopg2.connect(**fallback_config) as conn:
                    conn.autocommit = True  # Required for CREATE DATABASE
                    with conn.cursor() as cursor:
                        cursor.execute(f"CREATE DATABASE {db_name};")
                        print(f"Database '{db_name}' created successfully.")
            except Exception as db_create_error:
                raise RuntimeError(
                    f"Failed to create database '{db_name}': {db_create_error}"
                )
        else:
            raise


class DatabaseInitResource(Resource):
    def post(self):
        try:
            create_database_if_not_exists()

            with db_connection() as (conn, cursor):
                create_guests_table(cursor)
                create_update_last_seen_trigger(cursor)
                conn.commit()

            return jsonify(
                {"message": f"Database table '{TABLE_NAME}' initialized successfully."}
            )

        except Exception as e:
            return custom_response(f"Error initializing database: {str(e)}", 500)


class DatabaseFlushRestartResource(Resource):
    def post(self):
        try:
            with db_connection() as (conn, cursor):
                drop_guests_table(cursor)
                create_guests_table(cursor)
                create_update_last_seen_trigger(cursor)
                conn.commit()
                return jsonify({"message": f"Database table '{TABLE_NAME}' flushed and restarted successfully."})

        except Exception as e:
            return custom_response(f"Error flushing and restarting database: {str(e)}", 500)
