import os
import logging
import clickhouse_connect

# Configure logging
log_file = '/home/user/ch-migration/migration.log'
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def migrate():
    # Read connection details from environment variables
    host = os.environ.get('CLICKHOUSE_HOST')
    port = int(os.environ.get('CLICKHOUSE_PORT', 8443))
    user = os.environ.get('CLICKHOUSE_USER', 'default')
    password = os.environ.get('CLICKHOUSE_PASSWORD')

    if not host or not password:
        logging.error("CLICKHOUSE_HOST and CLICKHOUSE_PASSWORD must be set")
        print("Error: CLICKHOUSE_HOST and CLICKHOUSE_PASSWORD must be set")
        return

    try:
        # Connect to ClickHouse Cloud
        client = clickhouse_connect.get_client(
            host=host,
            port=port,
            username=user,
            password=password,
            secure=True
        )
        logging.info("Connected to ClickHouse Cloud")

        # Ensure users table exists
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id UInt64,
            username String
        ) ENGINE = MergeTree 
        ORDER BY id
        """
        client.command(create_table_query)
        logging.info("Table 'users' verified/created")

        # Ensure last_login column exists
        alter_table_query = "ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login DateTime"
        client.command(alter_table_query)
        logging.info("Column 'last_login' verified/added")

        print("Migration completed successfully.")
        logging.info("Migration completed successfully.")

    except Exception as e:
        logging.error(f"Migration failed: {str(e)}")
        print(f"Error during migration: {str(e)}")

if __name__ == '__main__':
    migrate()
