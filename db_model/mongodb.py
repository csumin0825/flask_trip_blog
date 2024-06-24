import pymongo

MONGO_HOST = "localhost"
MONGO_CONN = pymongo.MongoClient("mongodb://%s" % (MONGO_HOST))  # 로컬호스트로 몽고디비 접속


def conn_mongodb():
    try:
        MONGO_CONN.admin.command("ismaster")
        blog_ab = MONGO_CONN.blog_session_db.blog_db  # blog_session_db에 있는 blog_db 컬렉션을 객체로 가지고와라
    except:
        MONGO_CONN = pymongo.MongoClient("mongodb://%s" % (MONGO_HOST))  # 다시 커넥션 함수 호출
        blog_ab = MONGO_CONN.blog_session_db.blog_ab
    return blog_ab
