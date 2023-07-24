from flask import Flask , render_template, request, redirect, session
from data import Articles
from models import MyMongo
from config import MONGODB_URL
from datetime import timedelta
from functools import wraps

app = Flask(__name__)

app.secret_key = "a"


mymongo = MyMongo(MONGODB_URL, 'os')

app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=5)
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'

# 로그인 유지
def is_loged(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'is_loged' in session:
            return func(*args, **kwargs)
        else:
            return redirect('/login')
    return wrap

def is_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['username'] == "admin":
            return f(*args, **kwargs)
        else:
            return redirect('/login')
    return wrap

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
@is_loged
@is_admin
def admin():
    return render_template('admin.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":

        username = request.form.get("username")
        # form[], form.get()
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")

        user = mymongo.find_user(email)    
        if user:
            return redirect('/register')
        else:
            if username == "admin":
                return redirect('/register')
            
            else:
                result = mymongo.user_insert(username, email, phone, password)
                return redirect('/login')
        
    elif request.method == "GET":
        return render_template('register.html')
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    
    elif request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        result = mymongo.verify_password(password, email)
        user = mymongo.find_user(email)
        if result == "1":
            session['is_loged'] = True
            session['username'] = user['username']
            return render_template('index.html', message = user)          
        
        elif result == "2":
            return render_template('login.html', message = "Wrong")
        
        elif result == "3":
            return render_template('register.html', message = "None")
        
        return result 
        
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
    
@app.route('/list', methods=['GET','POST'])
def list():
    data = mymongo.find_data()
    # for i in data:
    #     print(i)
    return render_template('list.html', data = data)

@app.route('/create', methods=['GET','POST'])
@is_loged
def create():
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["desc"]
        author = request.form["author"]
        result = mymongo.insert_list(title, desc, author)
        print(result)
        return redirect('/list')
    elif request.method == "GET":
        return render_template('create.html')

# @app.route('/edit/<ids>' , methods=['GET', 'POST'])
# def edit(ids):
#     data = mymongo.find_data()
#     if request.method == 'GET':
#         return render_template('list_edit.html', data = data)
    
#     elif request.method == 'POST':
#         title = request.form['title']
#         desc = request.form['desc']
#         author = request.form['author']
        
#         result = mymongo.update_list(ids, title, desc, author)
#         print(result)
#         return redirect('/list')

# @app.route('/delete/<ids>')
# def delete(ids):
#     result = mymongo.delete_list(ids)
#     print(result)
#     return redirect('/list')

if __name__ == '__main__':
    app.run(debug=True, port=9999)