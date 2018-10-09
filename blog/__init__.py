from flask import Flask,render_template,url_for,redirect,request,session,jsonify,flash
from flask_pymongo import PyMongo
from pymongo import MongoClient
import datetime
import re

app=Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'

admin = MongoClient('mongodb://Chirag:chirag123456789@ds121413.mlab.com:21413/app')
db = admin['app']

posts=db.posts
month = {'1':'Jan' , '2':'Feb' , '3':'Mar' , '4':'Apr' , '5':'May' , '6':'Jun','7':'Jul','8':'Aug',
'9':'Sep','10':'Oct','11':'Nov','12':'Dec'}

@app.route('/',methods=['GET', 'POST'])
def index():
	entertainment = 0
	movies = 0
	technology = 0
	sports = 0
	facts = 0
	others = 0
	find = posts.find()
	blogs = []

	for blog in find:
		blogs.append(blog)

		if blog['tag'] == 'Entertainment':
			entertainment += 1
		elif blog['tag'] == 'Movies':
			movies += 1
		elif blog['tag'] == 'Technology':
			technology += 1
		elif blog['tag'] == 'Sports':
			sports += 1
		elif blog['tag'] == 'Facts':
			facts += 1
		elif blog['tag'] == 'Others':
			others += 1
	tags = {'entertain': entertainment, 'mov': movies,'tech': technology, 'spo': sports,'fact': facts,  'oth': others}
	search = []
	while blogs:
		search.append(blogs.pop())
	return render_template('home.html' ,posts=posts, search=search, tags=tags)

@app.route('/admin', methods=['POST','GET'])
def login():
	if request.method == 'POST':
		if request.form['username'] == 'Chirag Narang' and request.form['password'] == 'chirag':
			session['username'] = 'Chirag Narang'
			return redirect(url_for('add'))
		else:
			flash('Invalid Username or Password' , 'danger')
			return render_template('login.html')

	return render_template('login.html')

@app.route("/post/<l>", methods=['POST','GET'])
def post(l):
	document = posts.find_one({"title":str(l)})
	return render_template('full_post.html', document=document)


@app.route('/add_new_post', methods=['POST','GET'])
def add():
	if session['username']:
		da_te = datetime.date.today()
		date = month[str(da_te.month)]+" "+str(da_te.day)+","+str(da_te.year)
		if request.method == 'POST':
			posts =db.posts
			posts.insert_one({'title':request.form['title'],
				'content': request.form['content'],
				'date':date,
				'image': request.form['image'],
				'url': request.form['link'],
				'tag': request.form['tag']})
			flash('Added Successfully!' , 'success')
			return render_template('post_add.html')

		return render_template('post_add.html')

	flash('You need to login first !!!', 'warning')
	return redirect(url_for('login'))

@app.route('/logout')
def logout():
	session['username'] = None
	return redirect(url_for('login'))

@app.route('/tags/<tag>')
def tags(tag):
	search = posts.find()
	tags =[]
	for item in search:
		if item['tag'] == tag:
			tags.append(i)
	return render_template('tags.html', tags=tags)

@app.route('/<d>')
def date(d):
	tags =[]
	search = posts.find()
	for item in search:
		if item['date'] == d:
			doc.append(i)
	return render_template('date.html', tags=tags)


@app.route('/search/', methods=['POST','GET'])
def search():
	if request.method == 'POST':
		data = request.form['search']
		a = re.compile(str(request.form['search']), re.IGNORECASE)
		search = posts.find()
		tags = []
		for item in search:
			b = a.findall(item['title'])
			for j in b:
				tags.append(item)

		return render_template('tags.html', tags=tags)

	return redirect(url_for('index'))

if __name__ == '__main__':
	app.run(debug=True)
