from flask import Flask, render_template
import json, os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
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
    app.run(debug=False, host="0.0.0.0")

# Sample Json docs
# Saving them 
sample_users = \
{
    "username0":{
        "password":"imagine storing passwords in plaintext",
        "description":"userzero's  bio",
        "is_doctor":True,
        "posts":[12,32,42,2,43], #Post IDs i guess?
        "comments":[[12,2],[44,4]] #Post ID, then comment ID
    },
    "username1":{
        "password":"imagine storing passwords in plaintext",
        "description":"userone's  bio",
        "is_doctor":False,
        "posts":[34,12,43,65],
        "comments":[[13,0],[24,4]]
    }
}
sample_posts = \
{
    "1":{ #Post ID
        "title":"The Post's title",
        "description":"The Post's description",
        "username":"The Post's author",
        "comments":[
            ["username", "Lol that's dumb"],
            ["username1", "Drink Bleach"],
            ["username2", "Have you tried nuzzling your muzzle uwu?"]
        ]
    }
}

# BEGINNING OF CLASSES
class Account:
    # Create object then store to JSON
    def __init__(self, username, password, description, is_doctor):
        self.username = username
        self.password = password
        self.description = description
        self.is_doctor = is_doctor
        self.save_account(username, password, description, is_doctor)

    # Load values from JSON
    @classmethod
    def load_account(cls, username):
        pass

    # Save values to JSON
    def save_account(username, password, description, is_doctor):
        pass

    # Return string of comment given index
    def get_comment(index):
        pass

    # Return title of a post
    def get_post_title(index):
        pass

    #Return body of a post
    def get_post_body(index):
        pass
