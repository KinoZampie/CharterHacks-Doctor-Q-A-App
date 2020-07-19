import datetime
import json

users = {}
posts = {}
comments = {}

class Account:
    def __init__(self, username, password, description, is_doctor, image_url):
        self.username = username
        self.password = password
        self.description = description
        self.is_doctor = is_doctor
        self.image_url = image_url
        self.posts = []
        self.comments = []

    def __str__(self):
        return "Account(username: '{}', password: '{}', description: '{}', is_doctor: '{}')".format(self.username, self.password, self.description, self.is_doctor)

    @staticmethod
    def load_all():
        global users
        with open("json/users.json") as user_data:
            users = json.load(user_data)
        
    @classmethod
    def load_account(cls, username):
        try:
            user = users[username]
            return cls(username, user['password'], user['description'], user['is_doctor'], user['image_url'])
        except KeyError:
            print('No stored accounts named: ' + username)

    @staticmethod
    def is_stored(username):
        if username in users:
            return True
        else:
            return False

    @staticmethod
    def user_list():
        user_list = []
        for user in users:
            user_list.append(user)
        return user_list

    def store_account(self):
        users[self.username] = {
            'password': self.password,
            'description': self.description,
            'is_doctor': self.is_doctor,
            'image_url': self.image_url,
            'posts': self.posts,
            'comments': self.comments
        }
        with open("json/users.json","w") as user_data:
            user_data.write(json.dumps(users, indent=2))


    def write_post(self, title, body):
        post_id = Post.new_id()
        post = Post(post_id, title, body, self.username, datetime.datetime.now())

        self.posts.append(post_id)
        self.store_account()
        post.store_post()
        

class Post:
    def __init__(self, post_id, title, body, user, date, comments=[]):
        self.post_id = post_id
        self.title = title
        self.body = body
        self.user = user
        self.date = date
        self.comments = comments

    @staticmethod
    def new_id():
        return int(max(posts)) + 1 #Get a new ID for fresh posts

    @staticmethod
    def load_all():
        global posts
        with open("json/posts.json") as post_data:
            posts = json.load(post_data)
        return posts
    @classmethod
    def load_post(cls, post_id): #Load post from JSON to object
        try:
            post = posts[post_id]
            return cls(post_id, post["title"], post["body"], post["username"], post["date"],post["comments"])
        except KeyError:
            print('No stored posts have id: ' + post_id)

    #USE USER OBJECT AS ARGUMENT
    def write_comment(self, body, user):    
        comment_id = Comment.new_id() #Generate ID

        comment = Comment(comment_id, body, user.username, datetime.datetime.now())

        user.comments.append(comment_id)
        self.comments.append(comment_id)

        #Update JSON of post and comment
        comment.store_comment()
        self.store_post()
        user.store_account()


    def store_post(self): #Store a post to JSON
        posts[self.post_id] = {
            'title': self.title,
            'body': self.body,
            'username': self.user,
            'date': self.date,
            'comments': self.comments
        }
        with open("json/users.json","w") as post_data:
            post_data.write(json.dumps(posts,indent=2))
        postids=open("postids.txt", "a")
        postids.write(self.title)
        postids.close()


class Comment:
    def __init__(self, comment_id, body, user, date):
        self.comment_id = comment_id
        self.body = body
        self.user = user
        self.date = date
        self.comments = [] #List for storing child comments

    @staticmethod
    def load_all():
        global comments
        with open("json/comments.json") as comment_data:
            comments = json.load(comment_data)

    @staticmethod
    def new_id():
        return int(max(comments)) + 1 #Get a new ID for comments to use

    @classmethod
    def load_comment(cls, comment_id):
        global comments
        with open("json/comments.json","r") as comment_data:
            comments = json.load(comment_data)
        try:
            comment = comments[comment_id]
            return cls(comment_id, comment["body"], comment["username"], comment["date"])
        except KeyError:
            print('No stored comments have id: ' + comment_id)

    def store_comment(self): #Store a fresh comment to JSON
        comments[self.comment_id] = {
            'body': self.body,
            'username': self.user,
            'date': self.date,
            'comments': self.comments
        }
        with open("json/comments.json","w") as comment_data:
            comment_data.write(json.dumps(comments,indent=2))

    def write_comment(self, body, user):
        comment_id = Comment.new_id()
        comment = Comment(comment_id, body, user.username, datetime.datetime.now())

        user.comments.append(comment_id)
        self.comments.append(comment_id)

        #Update JSON of parent and child comment
        user.store_account()
        self.store_comment()
        comment.store_comment()


#Load data from json
Account.load_all()
Post.load_all()
Comment.load_all()
