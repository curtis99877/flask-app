import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
        render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'main.db'),
    SECRET_KEY='secret key',
    USERNAME='admin',
    PASSWORD='password'
))
app.config.from_envvar('FS_SETTINGS', silent=True)

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print 'Initialized the database.'

@app.route('/')
def index():
    context = {
        "title": "Hello World!"
        }
    return render_template('index.html', context=context)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    session['logged_in'] = True
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('index'))
