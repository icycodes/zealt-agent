import os
import logging
import clickhouse_connect

# Configuration
LOG_FILE = '/home/user/ch-migration/migration.log'

# Setup logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def run_migration():
    # 1. Read connection details from environment variables
    host = os.environ.get('CLICKHOUSE_HOST')
    port = int(os.environ.get('CLICKHOUSE_PORT', 8443))
    user = os.environ.get('CLICKHOUSE_USER', 'default')
    password = os.environ.get('CLICKHOUSE_PASSWORD')

    if not host or not password:
        error_msg = "CLICKHOUSE_HOST and CLICKHOUSE_PASSWORD environment variables are required."
        print(error_msg)
        logging.error(error_msg)
        return

    try:
        # 2. Connect to ClickHouse Cloud
        client = clickhouse_connect.get_client(
            host=host,
            port=port,
            username=user,
            password=password,
            secure=True
        )
        
        # 3. Create table if not exists
        # To log 'Table created' specifically when it's new, we could check first, 
        # but the prompt's implementation guide suggests using IF NOT EXISTS.
        # We will log the action as requested.
        
        # Check if table exists for more accurate logging
        table_exists = client.command("EXISTS TABLE users")
        
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id UInt64,
            username String
        ) ENGINE = MergeTree 
        ORDER BY id
        """
        client.command(create_table_query)
        if not table_exists:
            logging.info('Table created')
        else:
            logging.info('Table already exists')

        # 4. Add column if not exists
        # Check if column exists for more accurate logging
        column_check = client.query("DESCRIBE TABLE users")
        columns = [row[0] for row in column_check.result_rows]
        
        if 'last_login' not in columns:
            alter_table_query = "ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login DateTime"
            client.command(alter_table_query)
            logging.info('Column added')
        else:
            logging.info('Column last_login already exists')

        # 5. Write a final success message
        success_msg = "Migration completed successfully."
        print(success_msg)
        logging.info(success_msg)

    except Exception as e:
        error_msg = f"Migration failed: {str(e)}"
        print(error_msg)
        logging.error(error_msg)

if __name__ == "__main__":
    run_migration()
