from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Tạo database đặt tên database là database.db
db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '1'
    # Thiết lập đường dẫn cho Flask-SQLAlchemy 
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # Khởi tạo đối tượng liên kết với Flask
    db.init_app(app)
    
    #import module vào 
    from .views import views
    from .auth import auth

    # Đăng ký blueprint xác thực người dùng với ứng dụng
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note
    create_database(app)


    login_manager = LoginManager()
    
    # Khai báo sử dụng hàm này ở module login
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Tải đối tượng người dủng từ ID người dùng được lưu trữ trong session -> Xác thực người dùng khi login
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
