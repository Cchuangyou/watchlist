import os
import sys
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

WIN = sys.platform.startswith('win')

if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'



# define dataframe
name = 'hllee'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'Leon', 'year': '1994'},
    {'title': 'Mahjong', 'year': '1996'},
    {'title': 'Swallowtail Butterfly', 'year': '1996'},
    {'title': 'King of Comedy', 'year': '1999'},
    {'title': 'Devils on the Doorstep', 'year': '1999'},
    {'title': 'WALL-E', 'year': '2008'},
    {'title': 'The Pork of Music', 'year': '2012'},
]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False # 关闭对模型修改的监控
# loading config
db = SQLAlchemy(app)

# create database model
class User(db.Model):  # 表名: user
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 用户名


class Movie(db.Model):  # 表名: movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份


@app.route('/')
def index():
    return render_template('index.html', name=name, movies=movies)
