from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Post %r>' % self.id


@app.route('/posts')
@app.route('/index')
@app.route('/index.html')
@app.route('/')
def index():
    posts = Post.query.order_by(Post.date.desc()).all()
    return render_template("index.html", posts=posts)


@app.route('/new_post', methods=['POST','GET'])
def newPost():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        post = Post(title=title, intro=intro, text=text)

        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/posts')
        except:
            return "Error adding post"
    else:
        return render_template("new_post.html")


@app.route('/posts/<int:id>/update', methods=['POST','GET'])
def post_update(id):
    post = Post.query.get(id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.intro = request.form['intro']
        post.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return "Error editing post"
    else:

        return render_template("post_update.html", post=post)


@app.route('/posts/<int:id>')
def post_detail(id):
    post = Post.query.get(id)
    return render_template("post_detail.html", post=post)


@app.route('/posts/<int:id>/del')
def post_delete(id):
    post = Post.query.get_or_404(id)
    try:
        db.session.delete(post)
        db.session.commit()
        return redirect('/posts')
    except:
        return "Post deletion error"


@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
