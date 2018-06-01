# encoding:utf-8

from flask import Flask,render_template,request,redirect,url_for,session
import config
from models import User
from exts import db
from functools import wraps


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


# 登录限制的装饰器
def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return func(*args,**kwargs)
        else:
            return redirect('login')
    return wrapper


@app.route('/index/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.username == username, User.password == password).first()
        if user:
            session['user_id'] = user.id
            session.permanent = True
            #return render_template('index.html', username=user.username)
            return redirect(url_for('index'))
        else:
            message = 'Login Failed'
            return render_template('login.html', message=message)


@app.route('/registered/', methods=['GET', 'POST'])
@login_required
def registered():
    if request.method == 'GET':
        return render_template('registered.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        # 验证输入框不能为空
        message = [u'手机号码不能为空', u'用户名不能为空', u'密码不能为空', u'该用户已经被注册', u'两次输入的密码不一样']
        if not telephone:
            return render_template('registered.html', message=message[0])
        if not username:
            return render_template('registered.html', message=message[1])
        if not password1:
            return render_template('registered.html', message=message[2])
        if not password2:
            return render_template('registered.html', message=message[2])
        # 验证用户名是否被注册，如果用户被注册了，就提示该用户已经被注册过
        user = User.query.filter(User.username == username).first()
        if user:
            return render_template('registered.html', message=message[3])
        else:
            #
            if password1 != password2:
                return render_template('registered.html', message=message[4])
            else:
                user = User(username=username, telephone=telephone, password=password1)
                db.session.add(user)
                db.session.commit()
                # 如果注册成功，就跳转到登录页
                return redirect('login')


# 清除session退出登录
@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))


# 上下文处理器钩子函数,返回的字典中键的可以在模版上下文中用
@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    # 即使没有登录,也要必须返回一个空的字典。
    return {}


if __name__ == '__main__':
    app.run()
