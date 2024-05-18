import psycopg2
import requests
import logging
import json
import time

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# PostgreSQL connection details
pg_conn = psycopg2.connect(
    dbname="mydatabase",
    user="user",
    password="12345678",
    host="postgres",  # Using Docker service name
    port="5432"
)

# Elasticsearch connection details
es_url = 'http://elasticsearch:9200/students/_bulk'
headers = {"Content-Type": "application/x-ndjson"}

# Track the highest ID that has been synced to avoid resyncing the same data
last_synced_id = 0

def fetch_data(last_id):
    try:
        cursor = pg_conn.cursor()
        cursor.execute("""
            SELECT student_id, name, title, skills, deleted
            FROM students
            WHERE student_id > %s
            ORDER BY student_id ASC
        """, (last_id,))
        rows = cursor.fetchall()
        cursor.close()
        logger.debug("Database rows fetched: %s", rows)
        return rows
    except Exception as e:
        logger.error("Error fetching data from PostgreSQL: %s", e)
        raise

def format_data(rows):
    actions = []
    for row in rows:
        if row[4]:  # If the deleted flag is true
            action = {
                "delete": {
                    "_index": "students",
                    "_id": row[0]  # Assuming student_id is the first column
                }
            }
        else:
            action = {
                "index": {
                    "_index": "students",
                    "_id": row[0]  # Assuming student_id is the first column
                }
            }
            doc = {
                "student_id": row[0],
                "name": row[1],
                "title": row[2],
                "skills": row[3]
            }
            actions.append(json.dumps(action))
            actions.append(json.dumps(doc))
    return "\n".join(actions) + "\n"

def sync_data():
    global last_synced_id
    try:
        rows = fetch_data(last_synced_id)
        if not rows:
            logger.debug("No new data to sync.")
            return

        bulk_data = format_data(rows)
        logger.debug("Bulk data to be inserted/updated: %s", bulk_data)
        response = requests.post(es_url, headers=headers, data=bulk_data)
        response.raise_for_status()
        logger.debug("Bulk insert/update response: %s", response.json())

        # Update the last_synced_id
        last_synced_id = rows[-1][0]
        logger.debug("Updated last_synced_id: %s", last_synced_id)
    except Exception as e:
        logger.error("Error during sync: %s", e)
        raise

if __name__ == "__main__":
    while True:
        sync_data()
        time.sleep(10)  # Poll every 10 seconds
