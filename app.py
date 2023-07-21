from flask import Flask , render_template, request
from data import Articles
from models import MyMongo
from config import MONGODB_URL


app = Flask(__name__)

mymongo = MyMongo(MONGODB_URL, 'os')

@app.route('/', methods=['GET','POST'])
def index():
    data = Articles()
    return render_template('index.html', data = data)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":

        username = request.form.get("username")
        # form[], form.get()
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")
        
        result = mymongo.user_insert(username, email, phone, password)
        print(result)
        return str(result)




if __name__ == '__main__':
    app.run(debug=True, port=9999)