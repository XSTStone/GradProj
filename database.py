import pymysql

conn = pymysql.connect(
    host='sh-cynosdbmysql-grp-krdmzg9q.sql.tencentcdb.com',
    port=24711,
    user='root',
    password='beyond2016',
    database='Wine',
)