from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

#입력 폼을 관리하는 파일
#관리해야 될 부분만 클래스 구성 요소로 사용하면 됨
#flask form 객체는 request로 들어온 요청을 잘 배분해주는 역할을 함
#따지고 보면 검증을 위해 필요한거지 꼭 필요한 객체는 아닌거임 ㅇㅇ

class QuestionForm(FlaskForm):
    subject = StringField("제목", validators=[DataRequired("제목은 필수")])
    content = TextAreaField("내용", validators=[DataRequired("내용은 필수")])

class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수')])

class UserCreateForm(FlaskForm):
    username = StringField("사용자이름", validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField("비밀번호",validators=[DataRequired(), EqualTo("password2","비밀번호가 일치하지 않습니다.")])
    password2 = PasswordField("비밀번호 확인",validators=[DataRequired()])
    email = EmailField("이메일", validators=[DataRequired(), Email()])

class UserLoginForm(FlaskForm):
    username = StringField("사용자이름", validators=[DataRequired(), Length(min=3,max=25)])
    password = PasswordField("비밀번호", validators=[DataRequired()])
    