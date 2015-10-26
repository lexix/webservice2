import os
import codecs
import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


app = Flask(__name__)
app.config.from_object(__name__)


app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'flaskr.db'),
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)
    
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    otvet = []
    text = []
    new_text = request.form['text']
    for papka in os.listdir('/Users/aleksej/Desktop/python/lenta/database2')[1:]:
        for name in os.listdir('/Users/aleksej/Desktop/python/lenta/database2/%s'%papka):
            otvet.append(papka)
            text.append(codecs.open('/Users/aleksej/Desktop/python/lenta/database2/%s/%s'%(papka,name),'r').read().decode('koi8_r'))
    text.append(new_text)
    
    from sklearn.feature_extraction.text import CountVectorizer
    count_vect = CountVectorizer()
    X_counts = count_vect.fit_transform(text) 
    
      
    from sklearn.feature_extraction.text import TfidfTransformer
    tfidf_transformer = TfidfTransformer()
    X_tfidf = tfidf_transformer.fit_transform(X_counts)
    
    
    from sklearn.naive_bayes import MultinomialNB
    clf = MultinomialNB().fit(X_tfidf[:-1:], otvet)
    
    predicted = clf.predict(X_tfidf[-1::])
    #a = request.form['text']+predicted[0]
    db.execute('insert into entries (title, text) values (?, ?)',
                [predicted[0].decode('utf-8'),request.form['text']])
                #request.form['text']])
    #print predicted[0].decode('koi8_r')
    db.commit()
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
    app.run()
