from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

import functools

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User

#유저 관리하는 파일

bp = Blueprint("auth", __name__, url_prefix="/auth")

@bp.route("/signup/", methods=("GET", "POST"))
def signup():
    form = UserCreateForm()
    if request.method == "POST" and form.validate_on_submit(): #요청이 post이고 맞는 요청이라면
        user = User.query.filter_by(username=form.username.data).first() 
        if not user: #유저의 유저 네임 데이터가 없다면 
            user = User(username=form.username.data, password=generate_password_hash(form.password1.data),email=form.email.data)
            db.session.add(user) #만들어서 세션에 넣어줌
            db.session.commit() #커밋
            return redirect(url_for("main.index"))
        else: #유저 네임이 이미 있으면 존재하는 사용자
            flash("이미 존재하는 사용자입니다.")
    return render_template("auth/signup.html",form=form)

@bp.route("/login/", methods=("GET", "POST"))
def login():
    form = UserLoginForm()
    if request.method == "POST" and form.validate_on_submit(): #누굴 위한 Post인지는 지정하지 않음 지정 안하고 일단 post 때려버려
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data): #유저의 비밀번호와 폼 비교
            error = "비밀번호가 올바르지 않습니다."
        if error is None: #여기까지 문제 없으면
            session.clear() #세션 클리어하고 로그인 해줌
            session["user_id"] = user.id #유저 id는 유저 id
            _next = request.args.get('next','')
            if _next:
                return redirect(_next) #넥스트에 대한 요청이 있는거면 넥스트로, 원래 가려던 페이지가 있는 케이스 
            else:
                return redirect(url_for("main.index")) #처음 온거면 main.index로
        flash(error) #에러 있으면 에러 방출
    return render_template("auth/login.html", form=form)

@bp.before_app_request #라우트 함수보다 앞서는 친구, 로그인이나 로그아웃 하기전에 유저 id 있는지 확인
def load_logged_in_user():
    user_id = session.get("user_id") #유저 id 세션 가져오고
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

@bp.route("/logout/")
def logout(): #로그 아웃 누르면 세션 클리어 시키면서 메인 인덱스로 보냄 # 메인 인덱스 가면 원본 question list로
    session.clear()
    return redirect(url_for("main.index")) 

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == "GET" else ''
            return redirect(url_for("auth.login", next=_next))
        return view(*args, **kwargs) #로그인 되어 있으면 원래 함수 실행
    return wrapped_view