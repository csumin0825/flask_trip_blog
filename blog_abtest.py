from flask import Flask, jsonify, request, render_template, make_response, session
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_cors import CORS
from blog_view import blog
from blog_control.user_mgmt import User
import os

# https 만을 지원하는 기능을 http에서 테스트할 때 필요한 설정
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

app = Flask(__name__, static_url_path="/static")
CORS(app)
app.secret_key = "dave_server2"

app.register_blueprint(blog.blog_abtest, url_prefix="/blog")
login_manager = LoginManager()
login_manager.init_app(app)  # flask 객체를 등록
login_manager.session_protection = "strong"  # 복잡한 세션정보를 만든다


@login_manager.user_loader
def login_user(user_id):  # flaks_login 이 http request 에서 유저 아이디를 자동으로 추출, 넣어준다
    return User.get(user_id)  # mysql 에서 user_id로 데이터를 뽑아와서 객체를 만들고 리턴할 수 있게해줌


@login_manager.unauthorized_handler
def unauthoried():  # 로그인된 사용자만 접근할 수 있는 api를 로그인하지 않은 사용자가 접근했을 경우, 호출할 함수
    return make_response(jsonify(success=False), 401)  # 401: 허용되지 않음


@app.before_request  # 모든 요청 전에 실행
def app_before_request():
    if "client_id" not in session:
        session["client_id"] = request.environ.get(
            "HTTP_X_REAL_IP", request.remote_addr
        )  # http 실제 정보를 client_id에 저장해라
        # 클라이언트 아이디가 해당 세션에 없다면 세션 정보를 넣는다


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")
