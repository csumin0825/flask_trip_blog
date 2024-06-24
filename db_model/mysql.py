import pymysql

MYSQL_HOST = "localhost"
MYSQL_CONN = pymysql.connect(host=MYSQL_HOST, port=3306, user="root", passwd="Sm000825!", db="blog_db", charset="utf8")


def conn_mysqldb():
    if not MYSQL_CONN.open:  # 커넥션이 끊어졌을 경우
        MYSQL_CONN.ping(reconnect=True)  # 다시 연결
    return MYSQL_CONN
