HOSTNAME = 'sh-cynosdbmysql-grp-krdmzg9q.sql.tencentcdb.com'
PORT = 24711
USERNAME = 'root'
PASSWORD = 'Beyond2016'
DATABASE = 'Wine'
DB_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"

import pymysql


conn = pymysql.connect(
    host=HOSTNAME,
    port=PORT,
    user=USERNAME,
    password=PASSWORD,
    database=DATABASE
)

