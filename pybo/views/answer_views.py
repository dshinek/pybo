from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from .. import db
from ..models import Question, Answer
from ..forms import AnswerForm

from .auth_views import login_required

bp = Blueprint('answer',__name__, url_prefix='/answer')

#답과 관련된거 관리하는 파일

@bp.route('/create/<int:question_id>', methods= ('POST',))
@login_required #로그인 해야 쓸 수 있음
def create(question_id): 
    form = AnswerForm() #정답 폼 가져오고
    question = Question.query.get_or_404(question_id) # 질문 객체 로드
    if form.validate_on_submit():
        content = request.form["content"]

        answer = Answer(content=content, create_date=datetime.now(), user=g.user) #내용, 시간, 유저 객체로 객체 생성 !
        question.answer_set.append(answer) #역참조 엔서에 엔서셋이라고 있음 그걸 퀘스쳔이 참조함
        db.session.commit()
        return redirect('{}#answer_{}'.format(url_for('question.detail', question_id=question_id), answer.id))
    return render_template("question/question_detail.html", question=question,form=form)

@bp.route('/modify/<int:answer_id>', methods=('GET', 'POST'))
@login_required #답변 수정시 로그인 해야 됨
def modify(answer_id):
    answer = Answer.query.get_or_404(answer_id) #answer 가져옴
    if g.user != answer.user:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.detail', question_id=answer.question.id))
    if request.method == "POST":
        form = AnswerForm()
        if form.validate_on_submit():
            form.populate_obj(answer) #앤서 업데이트하고
            answer.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit() #커밋
            return redirect('{}#answer_{}'.format(url_for('question.detail', question_id=answer.question.id), answer.id))
            ##answer_9에 대한 uri는 누가 정한거지....? # 이후에 대한 정보는 url이 받아들이지 않음, 즉 주석 느낌
    else:
        form = AnswerForm(obj=answer) #get으로 들어오면 즉, 작성을 한건 아니고 하려고 하는거면 그냥 폼만 받아
    return render_template('answer/answer_form.html', form=form)

@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id) #answer 받아오고
    question_id = answer.question.id #퀘스쳔 id 가져오고
    if g.user != answer.user:
        flash('삭제권한이 없습니다') #삭제 권한 없음 !
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))

@bp.route('/vote/<int:answer_id>/')
@login_required
def vote(answer_id):
    _answer = Answer.query.get_or_404(answer_id) #답 가져오고
    if g.user == _answer.user: #유저 같으면 아웃 
        flash('본인이 작성한 글은 추천할수 없습니다')
    else:
        _answer.voter.append(g.user) 
        db.session.commit()
    return redirect('{}#answer_{}'.format(url_for('question.detail', question_id=_answer.question.id), _answer.id))