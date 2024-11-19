import re
from flask import jsonify
from flask_restful import Resource, reqparse, abort
from psycopg2 import errors
from utils import db_connection, table_exists, custom_response
from constants import DEVICE_NAME, MAC_ADDRESS, TABLE_NAME, ID, LAST_SEEN


def valid_mac_address(mac_id: str) -> bool:
    return re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", mac_id.lower())


class DatabaseHealthResource(Resource):
    def get(self):
        try:
            with db_connection() as (conn, cursor):
                cursor.execute(
                    """
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' AND table_name = %s
                    );
                    """,
                    (TABLE_NAME,)
                )
                table_exists = cursor.fetchone()[0]

                if not table_exists:
                    return custom_response(f"Table '{TABLE_NAME}' does not exist", 500)

            return jsonify({'status': 'Guest Database API is running!'})

        except Exception as e:
            return custom_response(f"Health check failed: {str(e)}", 500)


class DatabaseGuestsResource(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("device_name", type=str, required=True, help='Device Name is required',
                                 location='json')
        self.parser.add_argument("mac_address", type=str, required=True, help='Mac Address is required',
                                 location='json')

    def get(self):
        with db_connection() as (conn, cursor):
            if not table_exists(cursor, TABLE_NAME):
                return custom_response(f"Table '{TABLE_NAME}' does not exist. Please initialize the database.", 404)
            cursor.execute(f"SELECT * FROM {TABLE_NAME};")
            rows = cursor.fetchall()

        guests = [{ID: row[0], DEVICE_NAME: row[1], MAC_ADDRESS: row[2], LAST_SEEN: row[3]} for row in rows]
        return jsonify(guests)

    def post(self):
        guest = self.parser.parse_args()

        if not valid_mac_address(guest[MAC_ADDRESS]):
            return custom_response(f'{guest[MAC_ADDRESS]} is not a valid mac address', 400)

        with db_connection() as (conn, cursor):
            if not table_exists(cursor, TABLE_NAME):
                return custom_response(f"Table '{TABLE_NAME}' does not exist. Please initialize the database.", 404)
            try:
                cursor.execute(
                    f"INSERT INTO {TABLE_NAME} ({DEVICE_NAME}, {MAC_ADDRESS}, {LAST_SEEN}) VALUES (%s, %s, NOW()) RETURNING {ID};",
                    (guest[DEVICE_NAME], guest[MAC_ADDRESS])
                )
                new_id = cursor.fetchone()[0]
                conn.commit()
                return jsonify({"id": new_id, "message": "Guest added successfully"})

            except errors.UniqueViolation:
                conn.rollback()
                return custom_response("Guest with this device name and MAC address already exists", 400)

            except Exception as e:
                conn.rollback()
                abort(500, message=str(e))

    def put(self):
        guest = self.parser.parse_args()

        with db_connection() as (conn, cursor):
            if not table_exists(cursor, TABLE_NAME):
                return custom_response(f"Table '{TABLE_NAME}' does not exist. Please initialize the database.", 404)
            try:
                cursor.execute(
                    f"SELECT * FROM {TABLE_NAME} WHERE {MAC_ADDRESS} = %s AND {DEVICE_NAME} = %s;",
                    (guest[MAC_ADDRESS], guest[DEVICE_NAME])
                )
                existing_guest = cursor.fetchone()

                if not existing_guest:
                    return custom_response("Guest with this MAC address and device name does not exist.", 404)

                cursor.execute(
                    f"UPDATE {TABLE_NAME} SET {MAC_ADDRESS} = %s WHERE {DEVICE_NAME} = %s;",
                    (guest[MAC_ADDRESS], guest[DEVICE_NAME])
                )
                conn.commit()
                return jsonify({"message": f"Device {guest[DEVICE_NAME]} updated successfully"})

            except Exception as e:
                conn.rollback()
                abort(400, message=str(e))


class DatabaseGuestIdResource(Resource):
    def get(self, guest_id: int):
        with db_connection() as (conn, cursor):
            if not table_exists(cursor, TABLE_NAME):
                return custom_response(f"Table '{TABLE_NAME}' does not exist. Please initialize the database.", 404)
            cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE {ID} = %s;", (guest_id,))
            row = cursor.fetchone()

        if row:
            selected_guest = {ID: row[0], DEVICE_NAME: row[1], MAC_ADDRESS: row[2], LAST_SEEN: row[3]}
            return jsonify(selected_guest)
        else:
            return custom_response("Guest not found", 404)

    def delete(self, guest_id: int):
        with db_connection() as (conn, cursor):
            if not table_exists(cursor, TABLE_NAME):
                return custom_response(f"Table '{TABLE_NAME}' does not exist. Please initialize the database.", 404)
            try:
                cursor.execute(f"DELETE FROM {TABLE_NAME} WHERE id = %s RETURNING {ID};", (guest_id,))
                deleted_guest = cursor.fetchone()

                if not deleted_guest:
                    return custom_response(f"Guest with {ID} {guest_id} does not exist", 404)

                conn.commit()
                return jsonify({"message": f"Guest with {ID} {guest_id} deleted successfully"})

            except Exception as e:
                conn.rollback()
                abort(500, message=str(e))
