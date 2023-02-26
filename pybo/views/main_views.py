from flask import Blueprint, url_for
from werkzeug.utils import redirect

bp = Blueprint("main", __name__, url_prefix='/') #url_prefix는 해당 파일 아래에 있는 모든 라우팅에 붙은 오프셋 앞의 "main"은 url_for를 위해 필요한 스트링

@bp.route("/hello")
def hello_pybo():
    return "Hello, Pybo!"

@bp.route('/')
def index():
    #print(url_for('question._list')) #question._list가 보내는 uri인 /question/list 반환
    return redirect(url_for('question._list')) #question._list 부분으로 라우팅 #redirect는 그곳으로 쏨