import psycopg2
import requests
import logging
import json
import time
from psycopg2.extras import DictCursor
from requests.exceptions import HTTPError

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def connect_to_postgres():
    """Establishes a PostgreSQL connection."""
    return psycopg2.connect(
        dbname="alumni_db",
        user="postgres",
        password="qwerty",
        host="152.42.163.114",  # Using Docker service name
        port="5434"
    )

def connect_to_elasticsearch():
    """Returns Elasticsearch bulk URL and headers."""
    return 'http://elasticsearch:9200/user_details/_bulk', {"Content-Type": "application/x-ndjson"}

def fetch_all_data(pg_conn):
    """Fetch all user details from PostgreSQL."""
    try:
        with pg_conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute("""
                SELECT id, achievements, address, educations, email, first_name, gender, interests, languages, last_name, nationality, skills, telephone, work_experiences, generation_id, user_id
                FROM al_user_details
                ORDER BY id ASC  -- Ensuring a consistent order
            """)
            return cursor.fetchall()
    except Exception as e:
        logger.error("Error fetching data from PostgreSQL: %s", e)
        raise

def format_data(rows):
    """Formats rows into a bulk JSON action list for Elasticsearch."""
    actions = []
    for row in rows:
        action = {
            "index": {
                "_index": "user_details",
                "_id": row['id']
            }
        }
        doc = {key: row[key] for key in row.keys() if key != 'id'}
        actions.append(json.dumps(action))
        actions.append(json.dumps(doc))
    return "\n".join(actions) + "\n"

def sync_data(pg_conn, es_url, headers):
    """Synchronizes data from PostgreSQL to Elasticsearch."""
    try:
        rows = fetch_all_data(pg_conn)
        if not rows:
            logger.debug("No new data to sync.")
            return

        bulk_data = format_data(rows)
        response = requests.post(es_url, headers=headers, data=bulk_data)
        response.raise_for_status()
        logger.debug("Data successfully synchronized to Elasticsearch.")
    except HTTPError as e:
        logger.error("HTTP error during sync: %s", e.response.text)
        raise
    except Exception as e:
        logger.error("Error during sync: %s", e)
        raise

if __name__ == "__main__":
    pg_conn = connect_to_postgres()
    es_url, headers = connect_to_elasticsearch()
    try:
        while True:
            sync_data(pg_conn, es_url, headers)
            time.sleep(10)  # Poll every 10 seconds
    finally:
        pg_conn.close()
