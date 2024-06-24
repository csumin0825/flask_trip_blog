from flask import Flask, Blueprint, request, render_template, make_response, jsonify, redirect, url_for, session
from flask_login import login_user, current_user, logout_user
from blog_control.user_mgmt import User
from blog_control.session_mgmt import BlogSession
import datetime

blog_abtest = Blueprint("blog", __name__)


@blog_abtest.route("/set_email", methods=["GET", "POST"])
def set_email():
    if request.method == "GET":
        # print("set_email", request.headers)
        print("set_email", request.args.get("user_email"))
        return redirect(
            url_for("blog.test_blog")
        )  # url_for 는 라우팅 이름을 넣으면 라우팅 경로를 리턴함, blog는 blueprint 이름, test_blog는 라우팅 함수명
        # return redirect("/blog/test_blog")
        # return make_response(jsonify(success=True), 401)
    else:
        # print("set_email", request.headers)
        # print("set_email", request.get_json())  content-type이 application/json이 아닌 경우 오류가 생길 수 있다.
        # print("set_email", request.form["user_email"])  # form 데이터로 넘어올 경우 request.form으로 가져와야함
        # print("set_email", request.form["blog_id"])
        user = User.create(
            request.form["user_email"], request.form["blog_id"]
        )  # sessoin_mgmt에서 blog_page가 'blog_A.html'로 정의된 'A'
        login_user(
            user, remember=True, duration=datetime.timedelta(days=365)
        )  # 쿠키정보에 세션정보를 넣어서 보낸다 세션 정보는 flask_login에 있는 login_user라는  메서드에 생성된 사용자 객체를 넣어줘야함

        return redirect(url_for("blog.blog_fullstack1"))


@blog_abtest.route("/logout")
def logout():
    User.delete(current_user.id)
    logout_user()  # 현재 사용자의 세션정보를 지움
    return redirect(url_for("blog.blog_fullstack1"))


@blog_abtest.route("/blog_fullstack1")
def blog_fullstack1():
    if current_user.is_authenticated:  # 로그인되어 있는 사용자인지 확인
        webpage_name = BlogSession.get_blog_page(current_user.blog_id)
        BlogSession.save_session_info(session["client_id"], current_user.user_email, webpage_name)
        return render_template(webpage_name, user_email=current_user.user_email)
    else:  # 한번도 등록되지 않은 사용자일 경우
        webpage_name = BlogSession.get_blog_page()
        BlogSession.save_session_info(session["client_id"], "anonymous", webpage_name)
        return render_template(webpage_name)
