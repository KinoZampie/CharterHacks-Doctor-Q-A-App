from flask import Flask, render_template, request, url_for, redirect, make_response, request
import os
import asclepius
import json
import jsonlines

cookie=None

app = Flask(__name__)
@app.route('/')

def index():
    cookie=request.cookies.get("username")
    if cookie is not None:
        return redirect(url_for("posts"))
    return render_template('index.html')

@app.route('/register',methods=["GET","POST"])
def register():
    cookie=request.cookies.get("username")
    if cookie is not None:
        return redirect(url_for("posts"))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        image_url = request.form.get("img")
        desc = request.form.get("description")
        is_doctor = bool(request.form.get("role"))
        if not asclepius.Account.is_stored(username):
            user = asclepius.Account(username,password,desc,is_doctor,image_url)
            user.store_account()
            resp=make_response(render_template("posts.html"))
            resp.set_cookie("username",username)
            return resp
        
    return render_template('register.html')

@app.route('/login', methods=["GET","POST"])
def login():
    cookie=request.cookies.get("username")
    if cookie is not None:
        return redirect(url_for("posts"))
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        user=asclepius.Account.load_account(username)
        if asclepius.Account.is_stored(username):
            real_password=user.password
            if password==real_password:
                resp=make_response(render_template("posts.html"))
                resp.set_cookie("username",username)
                return resp
        else:
            user=None
            return redirect(url_for("login"))
    return render_template("login.html")
    

@app.route('/posts', methods=["GET","POST"])
def posts():
    cookie=request.cookies.get("username")
    if cookie is None:
        return redirect(url_for("index"))
    # with open('postids.txt') as f:
    #     users=f.read().splitlines()
    posts = asclepius.Post.load_all()
    if request.method=="POST":
        title=request.form.get("the_title")
        description=request.form.get("the_description")
        the_user=asclepius.Account.load_account(request.cookies.get("username"))
        user.asclepius.write_post(title, description)
        
    return render_template("posts.html", posts=posts)

@app.route("/posts/<post_id>", methods=["GET","POST"])
def post(post_id):
    return render_template("post.html")

@app.route('/profiles/<profile>')
def profile():
    return render_template("profile.html")


if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0")
