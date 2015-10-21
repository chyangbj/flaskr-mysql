from __future__ import with_statement
import MySQLdb
from MySQLdb.cursors import DictCursor
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
from contextlib import closing

DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    connect =  MySQLdb.connect(host='mysql', user='root', passwd='123abc,.', db='flaskr')
    return connect

@app.before_request
def before_request():
    g.db = connect_db()

@app.after_request
def after_request(response):
    """Closes the database again at the end of the request."""
    g.db.close()
    return response

@app.route('/')
def show_entries():
    cur = g.db.cursor(DictCursor)
    cur.execute('select title, text from entries order by id desc')
    entries = [dict(title=row['title'].decode('utf-8'), text=row['text'].decode('utf-8')) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    cur = g.db.cursor()
    cur.execute('insert into entries (title, text) values (%s, %s)',
                 [request.form['title'].encode('utf-8'), request.form['text'].encode('utf-8')])
    cur.close()
    g.db.commit()

    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
