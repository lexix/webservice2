# This Python file uses the following encoding: utf-8,ascii
import os
import codecs
import sqlite3
import os
from sklearn.externals import joblib
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
    
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

@app.route('/')
def show_entries():
    if os.path.exists('text.txt'):
        a = open('otvet.txt','r')
        b = open('text.txt','r')
        otvet = a.read()
        text = b.read()
    else:
        otvet = "Here you will see the news' type"
        text = 0
    if os.path.exists('text.txt'):
        os.remove('otvet.txt')
        os.remove('text.txt')
    return render_template('show_entries.html', otvet=otvet,text=' ')
    
@app.route('/add', methods=['POST'])
def add_entry():
    
    if not session.get('logged_in'):
        abort(401) 
    if os.path.exists('text.txt'):
        os.remove('otvet.txt')
        os.remove('text.txt')
    new_text = request.form['text']
    a = open('otvet.txt','w')
    b = open('text.txt','w')
    otvet = []
    text = []
    for papka in os.listdir('/Users/aleksej/Desktop/python/lenta/database2')[1:]:
        for name in os.listdir('/Users/aleksej/Desktop/python/lenta/database2/%s'%papka):
            otvet.append(papka)
            text.append(codecs.open('/Users/aleksej/Desktop/python/lenta/database2/%s/%s'%(papka,name),'r').read().decode('koi8_r'))
    
    new_text = new_text.encode('utf-8')
    b.write(new_text)
    new_text = new_text.decode('koi8_r')
    text.append(new_text)
    #b.write(new_text)
    clf = joblib.load('classifier.pkl') 
    
    from sklearn.feature_extraction.text import CountVectorizer
    count_vect = CountVectorizer()
    X_counts = count_vect.fit_transform(text) 
    from sklearn.feature_extraction.text import TfidfTransformer
    tfidf_transformer = TfidfTransformer()
    X_tfidf = tfidf_transformer.fit_transform(X_counts)
    try:
        predicted = clf.predict(X_tfidf)[-1:]
    except BaseException:
        predicted = 'the classification cannot be done'
    predicted = clf.predict(X_tfidf)[-1:][0]        
    if predicted == 'Россия':
        predicted = 'Russia'
    elif predicted == 'Мир':
        predicted = 'World'
    elif predicted == 'Бывший СССР':
        predicted = 'USSR'
    elif predicted == 'Спорт':
        predicted = 'Sport'
    elif predicted == 'Бизнес':
        predicted = 'Business'
    elif predicted == 'Культура':
        predicted = 'Culture'
    elif predicted == 'Наука и техника':
        predicted = 'Science'
    elif predicted == 'Силовые структуры':
        predicted = 'Military'
    elif predicted == 'Интернет и СМИ':
        predicted = 'Internet'
    elif predicted == 'Из жизни':
        predicted = 'From life'
    elif predicted == 'Финансы':
        predicted = 'Finance'
    else:
        predicted = 'the classification cannot be done'
    
    #new_text = '23'
    #a = request.form['text']+predicted[0]
    a.write(predicted)
    a.close()
    b.close()
                #request.form['text']])
    #print predicted[0].decode('koi8_r')
    flash("Now you can see the news' type")
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
    app.run(debug=True)
