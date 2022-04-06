from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://axelportable:123test@cluster0.523ue.mongodb.net/hw2"
mongo = PyMongo(app)

if mongo.db['hw2_collection'].count_documents({"username" : 'admin'}) == 0:
    mongo.db['hw2_collection'].insert_one({"username":'admin', "password" : generate_password_hash('admin')})

@app.route('/',methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("login.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        user = mongo.db['hw2_collection'].find_one({"username" : username})
        if user and check_password_hash(user['password'], password):
          return render_template('profile.html', username=username, password = password)  
        else:
            return render_template("login.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)