from datetime import datetime

from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect

from .. import db
from ..forms import QuestionForm, AnswerForm
from ..models import Question, Answer, User

from pybo.views.auth_views import login_required

bp = Blueprint("question",__name__, url_prefix="/question")
#질문과 관련한거 관리하는 파일

@bp.route('/list/')
def _list():
    #print("#################",request.args.get)
    page = request.args.get('page', type=int, default=1) #페이지 클릭으로 접근시 사용
    kw = request.args.get('kw', type=str, default='') #검색시 keyword 가져오는 인자
    question_list = Question.query.order_by(Question.create_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username).join(User, Answer.user_id == User.id).subquery()
        question_list = question_list.join(User).outerjoin(sub_query, sub_query.c.question_id == Question.id).filter(Question.subject.ilike(search) |  # 질문제목
                    Question.content.ilike(search) |  # 질문내용
                    User.username.ilike(search) |  # 질문작성자
                    sub_query.c.content.ilike(search) |  # 답변내용
                    sub_query.c.username.ilike(search)  # 답변작성자
                    ) \
            .distinct()
    question_list = question_list.paginate(page=page, per_page=10) #db 객체에 paginate 등 지정 가능
    print("#################",question_list.has_prev)
    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw) #render template은 맨처음엔 넘겨줄 html 파일 정의하고 뒤에는 인자 전달

@bp.route("/detail/<int:question_id>/") #/다음에 uri로 다루는 파트는 무조건 아래 함수가 파라미터로 받아야함
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template("question/question_detail.html", question=question, form=form) #question 페이지에 렌더링

@bp.route("/create/", methods=("GET","POST"))
@login_required #로그인 되어 있는지 확인해주는 함수
def create():
    form = QuestionForm()
    #print("########ASDFHJSHDGA!#%@$^%",request.form["content"]) #글 생성하는 함수
    if request.method == "POST" and form.validate_on_submit(): # 요청 방식이 post고 양식이 유효하다면 ~
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now()) #form의 내용들을 퀘스쳔 객체로 생성
        db.session.add(question) #퀘스쳔 항목을 db에 올리고
        db.session.commit() #확정시킴
        return redirect(url_for("main.index")) #글 썼으니 메인 인덱스로 리다이렉트 하면 다시 퀘스쳔 리스트로 리다이렉트됨
    return render_template("question/question_form.html",form=form) #유효하지 않으면 퀘스쳔 폼 html로 감 퀘스쳔 폼 html은 에러 코드 띄우는 곳

@bp.route("/modify/<int:question_id>", methods=("GET", "POST"))
@login_required
def modify(question_id):
    print("#################",request.method)
    question = Question.query.get_or_404(question_id)
    if g.user != question.user: #수정 권한이 있는지 먼저 검증
        flash("수정권한이 없습니다")
        return redirect(url_for("question.detail", question_id=question_id))
    if request.method == "POST": #방법이 포스트라면 또 수정 권한이 있다면? 위의 if를 뚫으려면 수정권한이 있어야 함
        form = QuestionForm() 
        if form.validate_on_submit(): #질문 양식 준수하는가 validate_on_submit은 페이지가 준수하는지 확인하는 과정, FlaskForm 내재 패키지 메서드
            form.populate_obj(question) #퀘스쳔폼 객체 업데이트 하는 역할, add랑 비슷
            question.modify_date = datetime.now()
            db.session.commit() #업데이트 된 객체 커밋
            return redirect(url_for("question.detail",question_id=question_id))
    else:
        form = QuestionForm(obj=question) #request 방식이 포스트가 아니라면? => 아 수정하러 들어온거면 수정할 수 있도록 html 파일 제공
    return render_template("question/question_form.html",form=form)

@bp.route('/delete/<int:question_id>')
@login_required #로그인 되어있나
def delete(question_id):
    question = Question.query.get_or_404(question_id) #퀘스쳔 뭐 가져오삼
    if g.user != question.user:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.detail', question_id=question_id)) #권한 없으면 탈락
    db.session.delete(question) #이 질문 삭제하삼
    db.session.commit() #커밋 ㄱㄱ
    return redirect(url_for('question._list'))

@bp.route('/vote/<int:question_id>/')
@login_required #로그인 되어잇?
def vote(question_id):
    _question = Question.query.get_or_404(question_id) #퀘스쳔 객체 가져오삼, 퀘스쳔 데이터 가져와
    if g.user == _question.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    else:
        _question.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))

