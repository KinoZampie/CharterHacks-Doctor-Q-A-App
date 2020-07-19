users = \
{
    "username0":{
        "password":"BRO I LOVE STORING PASSWORDS IN PLAIN TEXT",
        "description":"userzero's  bio",
        "is_doctor":True,
        "posts":[12,32,42,2,43], #Post ID's
        "comments":[12, 2, 14, 4] #Comment ID's
    },
    "username1":{
        "password":"I LOVE PLAIN TEXT PASSWORDS",
        "description":"userone's  bio",
        "is_doctor":False,
        "posts":[34, 12, 43, 65],
        "comments":[13, 0, 24, 4]
    }
}


posts = \
{
    "1":{ #Post ID
        "title":"The Post's title",
        "body":"The text of the post goes here",
        "username":"The Post's author",
        "date":"The date of the post",
        "comments":[12, 32, 42] # The children of a post (comment id's)
    }
}

comments = \
{
    "1":{ #Comment ID
        "body":"The text of the comment goes here",
        "username":"The comment's author",
        "date":"The date of the post",
        "comments":[12, 32, 42] # The children of a comment (other comment id's)
    }
}


class Account:
    def __init__(self, username, password, description, is_doctor):
        self.username = username
        self.password = password
        self.description = description
        self.is_doctor = is_doctor

    def __str__(self):
        return "Account(username: '{}', password: '{}', description: '{}', is_doctor: '{}')".format(self.username, self.password, self.description, self.is_doctor)

    @classmethod
    def load_account(cls, username):
        try:
            user = users[username]
            return cls(username, user['password'], user['description'], user['is_doctor'])
        except KeyError:
            print(username + ' is not saved as an account yet!')

    @staticmethod
    def is_saved(username):
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

    def save_account(self):
        users[self.username] = []
        users[self.username].append({
            'password': self.password,
            'description': self.description,
            'is_doctor': self.is_doctor
        })

    def write_post(self, title, body):
        post = Post(Post.new_id(), title, body, self.username, datetime.datetime.now())
        post.save_post()

class Post:
    def __init__(self, post_id, title, body, user, date):
        self.post_id = post_id
        self.title = title
        self.body = body
        self.user = user
        self.date = date
        self.comments = []

    @staticmethod
    def new_id():
        return int(max(posts)) + 1 #Get a new ID for fresh posts

    @classmethod
    def load_post(post_id): #Load post from JSON to object
        try:
            post = posts[post_id]
            return cls(post_id, post["title"], post["body"], post["username"], post["date"])
        except KeyError:
            print('No saved posts have id: ' + post_id)

    def save_post(): #Save a fresh post to JSON
        posts[self.post_id] = []
        posts[self.post_id].append({
            'title': self.title,
            'body': self.body,
            'username': self.user,
            'date' = self.date
        })
        

class Comment:
    def __init__(self, comment_id, post_id, body, user, date):
        self.post_id = post_id
        self.body = body
        self.user = user
        self.date = date

    @staticmethod
    def new_id():
        return int(max(comments)) + 1 # Get a new ID for comments to use

    @classmethod
    def load_comment(coment_id):
        try:
            comment = comments[comment_id]
            return cls(comment_id, comment["body"], post["username"], post["date"])
        except KeyError:

    def save_comment(): #Save a fresh comment to JSON
        comments[self.comment_id] = []
        comments[self.comment_id].append({
            'title': self.title,
            'body': self.body,
            'username': self.user,
            'date' = self.date
        })
            print('No saved comments have id: ' + comment_id)

