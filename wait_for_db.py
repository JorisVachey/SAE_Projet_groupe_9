import os
import time
import pymysql

host = os.getenv("DB_HOST", "db")
user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
database = os.getenv("DB_NAME")
port = int(os.getenv("DB_PORT", 3306))

print(" en attente de MariaDB...")

while True:
    try:
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port,
            connect_timeout=2,
        )
        conn.close()
        print("MariaDB est prêt !")
        

    except pymysql.MySQLError:
        print("MariaDB pas encore prêt")
        time.sleep(2) # on attend pour ne pas spamer de requête inutile
