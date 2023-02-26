from pybo import db

# db 관리해주는 파일 우리는 db를 SQLAlchemy로 정의함

question_voter = db.Table(
    'question_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True)
)

answer_voter = db.Table(
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
)

#db 객체들을 아래에 선언, 이 전체에 앱에 걸쳐 필요한 객체는 질문, 답변, 유저 3개가 전부인 것

class Question(db.Model): #db 객체 Question이라는 대상이 되려면 아래의 컬럼을 지녀야 함
    id = db.Column(db.Integer,primary_key = True) #아이디가 있어야 하고
    subject = db.Column(db.String(200),nullable=False) #주제가 있어야 하고
    content = db.Column(db.Text(), nullable=False) #내용이 있어야 하고
    create_date = db.Column(db.DateTime(), nullable=False) #만들어진 시간이 있어야 하고
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=True, server_default='1') 
    user = db.relationship("User", backref=db.backref("question_set"))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=question_voter, backref=db.backref('question_voter_set')) #유저 객체와 관련 있는 컬럼이라는 뜻

class Answer(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id",ondelete="CASCADE"))
    question = db.relationship("Question", backref=db.backref("answer_set"))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id",ondelete="CASCADE"),nullable=False)
    user = db.relationship("User", backref=db.backref("answer_set"))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set')) 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

