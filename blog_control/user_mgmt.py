from flask_login import UserMixin
from db_model.mysql import conn_mysqldb


# UserMixin을 상속받아서 기본 함수들을 사용할 수 있음
class User(UserMixin):
    # User 객체에 저장할 정보
    def __init__(self, user_id, user_email, blog_id):
        self.id = user_id
        self.user_email = user_email
        self.blog_id = blog_id

    def get_id(self):
        return str(self.id)

    # user 아이디로 찾는 방법
    # staticmethod 이기 때문에 User 객체를 생성하지 않아도 함수 사용가능
    @staticmethod
    def get(user_id):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM user_info WHERE USER_ID = '" + str(user_id) + "'"
        db_cursor.execute(sql)
        user = db_cursor.fetchone()
        if not user:
            return None
        user = User(user_id=user[0], user_email=user[1], blog_id=user[2])
        return user

    # 유저 이메일로 찾는 방법
    @staticmethod
    def find(user_email):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "SELECT * FROM user_info WHERE USER_EMAIL = '" + str(user_email) + "'"
        db_cursor.execute(sql)
        user = db_cursor.fetchone()
        if not user:
            return None
        user = User(user_id=user[0], user_email=user[1], blog_id=user[2])
        return user

    # 레코드 생성
    @staticmethod
    def create(user_email, blog_id):
        user = User.find(user_email)
        if user == None:  # 중복된 이메일이 mysql에 들어가지않도록
            mysql_db = conn_mysqldb()
            db_cursor = mysql_db.cursor()
            sql = "INSERT INTO user_info (USER_EMAIL, BLOG_ID) VALUES ('%s', '%s')" % (str(user_email), str(blog_id))
            db_cursor.execute(sql)  # sql문 실행
            mysql_db.commit()  # 트랜잭션을 데이터베이스에 적용
            return User.find(user_email)
        else:
            return user

    @staticmethod
    def delete(user_id):
        mysql_db = conn_mysqldb()
        db_cursor = mysql_db.cursor()
        sql = "DELETE FROM user_info WHERE USER_ID = %d" % (user_id)
        deleted = db_cursor.execute(sql)  # sql문 실행
        mysql_db.commit()  # 트랜잭션을 데이터베이스에 적용
        return deleted
