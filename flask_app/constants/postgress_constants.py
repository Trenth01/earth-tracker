DB_CONFIG = {
    "dbname": "guestwifi",
    "user": "admin",
    "password": "adminpassword",
    "host": "localhost",  # Or 'postgres-service' if running in Kubernetes
    "port": 5432
}

TABLE_NAME = 'guests'
MAC_ADDRESS = 'mac_address'
DEVICE_NAME = 'device_name'
LAST_SEEN = 'last_seen'
ID = 'id'