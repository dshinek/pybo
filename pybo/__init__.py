from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from flaskext.markdown import Markdown
import config

naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention)) #db 만드는 코드 
migrate = Migrate()

def create_app(): #flask의 메인이 되는 부분, 메인 프로그램에서 구현되는 어플리케이션을 만듬
    app = Flask(__name__) #flask 객체로 __name__ 선언
    app.config.from_object(config) #상수들 들어있는 콘피그 파일, Flask 객체가 꼭 챙겨야 하는 친구인듯
    #ORM
    db.init_app(app) #SQLAlchemy로 플라스크 객체 초기화
    migrate.init_app(app,db) #migrate 객체로 플라스크 객체 초기화
    if app.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app,db)
    from . import models

    # blue print #Unified Resorce Identifier 정리하는 역할
    from .views import main_views, question_views, answer_views, auth_views
    app.register_blueprint(main_views.bp) #main_views내의 변수 bp에 접근
    app.register_blueprint(question_views.bp) #question_views내의 변수 bp에 접근
    app.register_blueprint(answer_views.bp) #answer_views내의 변수 bp에 접근
    app.register_blueprint(auth_views.bp) #auth_views내의 변수 bp에 접근

    from .filter import format_datetime 
    app.jinja_env.filters["datetime"] = format_datetime #시간 양식 나타내주는 함수 등록
    
    #markdown
    Markdown(app, extensions=["nl2br", "fenced_code"])
#    breakpoint()
    return app