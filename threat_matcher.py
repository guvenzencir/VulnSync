import mysql.connector
from mysql.connector import Error

def check_target_vulnerabilities(target_platform, max_results=5):
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'YOUR_PASSWORD', # IMPORTANT: Update with your DB password
        'database': 'vulnsync_db'
    }

    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        search_query = """
            SELECT title, type, link 
            FROM exploits 
            WHERE platform LIKE %s 
            ORDER BY id DESC 
            LIMIT %s
        """
        
        search_term = f"%{target_platform}%"
        cursor.execute(search_query, (search_term, max_results))
        
        results = cursor.fetchall()

        if not results:
            return None
            
        return results 

    except Error as db_err:
        print(f"[-] Database Error: {db_err}")
        return None
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
