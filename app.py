import os
import sys
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import click

WIN = sys.platform.startswith('win')

if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False # close the supervise of the model changing.
# loading config
db = SQLAlchemy(app)

# create database model
class User(db.Model):  # list name: user
    id = db.Column(db.Integer, primary_key=True)  # subject
    name = db.Column(db.String(20))  # user name


class Movie(db.Model):  # list name: movie
    id = db.Column(db.Integer, primary_key=True)  # subject
    title = db.Column(db.String(60))  # movie title
    year = db.Column(db.String(4))  # movie years

@app.cli.command()
def forge():
    """Generate dummy data."""
    db.create_all()

    # global variables
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

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    if drop:
        db.drop_all()
        click.echo('Droping former database.')
    db.create_all()
    click.echo('Initialising database.')

@app.context_processor
def nameinfo():
    user = User.query.first()
    return dict(user=user)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


