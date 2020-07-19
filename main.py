from flask import Flask, render_template, request, url_for, redirect
import os
import asclepius

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        image_url = request.form.get("img")
        desc = request.form.get("description")
        is_doctor = bool(request.form.get("role"))
        if not asclepius.Account.is_stored(username):
            user = asclepius.Account(username,password,desc,is_doctor,image_url)
            user.store_account()
            return redirect(url_for("login"))
        
    return render_template('register.html')

@app.route('/login', methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        user=asclepius.Account.load_account(username)
        # print(password)
        # print(user)
        # print(asclepius.Account.is_stored(username))
        if asclepius.Account.is_stored(username):
            real_password=user.password
            if password==real_password:
                return redirect(url_for("posts"))
        else:
            return redirect(url_for("login"))
    return render_template("login.html")
    

@app.route('/posts')
def posts():
    return render_template("posts.html")

@app.route('/posts/<post>')
def view_post():
    return render_template("post.html")

@app.route('/profiles/<profile>')
def profile():
    return render_template("profile.html")

if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0")
