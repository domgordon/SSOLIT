#!/usr/bin/env python2.7

"""
Columbia's COMS W4111.001 Introduction to Databases
Example Webserver

To run locally:

    python server.py

Go to http://localhost:8111 in your browser.

A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.exc import IntegrityError
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response

global USER

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)


#
# The following is a dummy URI that does not connect to a valid database. You will need to modify it to connect to your Part 2 database in order to use the data.
#
# XXX: The URI should be in the format of: 
#
#     postgresql://USER:PASSWORD@35.227.79.146/proj1part2
#
# For example, if you had username gravano and password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://gravano:foobar@35.227.79.146/proj1part2"
#
DATABASEURI = "postgresql://aa3642:5693@35.227.79.146/proj1part2"


#
# This line creates a database engine that knows how to connect to the URI above.
#
engine = create_engine(DATABASEURI)

#
# Example of running queries in your database
# Note that this will probably not work if you already have a table named 'test' in your database, containing meaningful data. This is only an example showing you how to run queries in your database using SQLAlchemy.
#
engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")
#engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request.

  The variable g is globally accessible.
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't, the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass


#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to, for example, localhost:8111/foobar/ with POST or GET then you could use:
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#

def courselister(query):
  cursor = g.conn.execute(query)
  courses = []
  for result in cursor:
    row = []
    for i in range(0,len(result)):
        row.append(result[i])
    courses.append(row)
  cursor.close()
  return courses
  
@app.route('/allcourses')
def allcourses():
  """
  request is a special object that Flask provides to access web request information:

  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments, e.g., {a:1, b:2} for http://localhost?a=1&b=2

  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print request.args

  #
  # example of a database query
  #
  query = "SELECT DISTINCT C.cid, C.cname, C.credits, C.dname, S.section_n, S.semester, S.days, S.section_time, P.p_last_name FROM courses_offered C, sections_available_taught S, professors_works P WHERE S.cid=C.cid AND S.pid=P.pid"
  courses = courselister(query)

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  context = dict(data = courses)

 #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("allcourses.html", **context)

#
# This is an example of a different path.  You can see it at:
# 
#     localhost:8111/another
#
# Notice that the function name is another() rather than index()
# The functions for each app.route need to have different names
#


@app.route('/profile')
def profile():
  query = "SELECT DISTINCT C.cid, C.cname, C.credits, C.dname, S.section_n, S.semester, S.days, S.section_time, P.p_last_name FROM courses_offered C, sections_available_taught S, professors_works P, enrolled_in E WHERE S.cid=C.cid AND S.pid=P.pid and E.sid='%s' and E.cid=S.cid and E.section_n=S.section_n and E.semester=S.semester" % (USER)
  courses = courselister(query)
  context = dict(data = courses)
  return render_template("profile.html", **context)



@app.route('/filter_sem', methods=['POST'])
def filter_sem():
  sem = request.form['semester']
  print sem
  query = "SELECT DISTINCT C.cid, C.cname, C.credits, C.dname, S.section_n, S.semester, S.days, S.section_time, P.p_last_name FROM courses_offered C, sections_available_taught S, professors_works P WHERE S.cid=C.cid AND S.pid=P.pid AND S.semester='%s'" % (sem)
  
  courses = courselister(query)
  context = dict(data = courses)
  return render_template("allcourses.html", **context)


@app.route('/filter_dept', methods=['POST'])
def filter_dept():
  dept = request.form['department']
  print dept
  query = "SELECT DISTINCT C.cid, C.cname, C.credits, C.dname, S.section_n, S.semester, S.days, S.section_time, P.p_last_name FROM courses_offered C, sections_available_taught S, professors_works P WHERE S.cid=C.cid AND S.pid=P.pid AND C.dname='%s'" % (dept)
  courses = courselister(query)
  context = dict(data = courses)
  return render_template("allcourses.html", **context)


@app.route('/filter_cred', methods=['POST'])
def filter_cred():
  cred = request.form['credits']
  print cred
  query = "SELECT DISTINCT C.cid, C.cname, C.credits, C.dname, S.section_n, S.semester, S.days, S.section_time, P.p_last_name FROM courses_offered C, sections_available_taught S, professors_works P WHERE S.cid=C.cid AND S.pid=P.pid AND C.credits='%s'" % (cred)
  courses = courselister(query)
  context = dict(data = courses)
  return render_template("allcourses.html", **context)

@app.route('/search', methods=['POST'])
def search():
  term = request.form['searchterm']
  print term
  query = "SELECT DISTINCT C.cid, C.cname, C.credits, C.dname, S.section_n, S.semester, S.days, S.section_time, P.p_last_name FROM courses_offered C, sections_available_taught S, professors_works P WHERE S.cid=C.cid AND S.pid=P.pid AND C.cid='%s'" % (term)
  courses = courselister(query)
  context = dict(data = courses)
  return render_template("allcourses.html", **context)

@app.route('/')
def index():
  return render_template("index.html")


@app.route('/new_user')
def new_user():
  return render_template("new_user.html")


@app.route('/add_user', methods=['POST'])
def add_user():
  sid = request.form['sid']
  global USER
  USER = sid
  s_first_name = request.form['firstname']
  s_last_name = request.form['lastname']
  sname = request.form['sname']
  g.conn.execute('INSERT INTO students_attends VALUES (%s, %s, %s, %s)', sid, s_first_name, s_last_name, sname)
  return redirect('/profile')


@app.route('/existing_user')
def existing_user():
  return render_template("existing_user.html")


@app.route('/check_user', methods=['POST'])
def check_user():
  sid = request.form['sid']
  result = g.conn.execute("SELECT * FROM students_attends S WHERE S.sid=%s", sid)
  for row in result:
    if row['sid'] == sid:
      global USER
      USER = sid
      url = '/profile?user=' + sid
      return redirect(url)
  print "nah not there"
  return render_template("existing_user.html")


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  cname = request.form['course']
  g.conn.execute('INSERT INTO courses_offered(cname) VALUES (%s)', cname)
  return redirect('/')


@app.route('/enroll', methods=['POST'])
def enroll():
  print "HERE"
  response = request.form['submit']
  resp = response.split(",")
  cnum = resp[0]
  snum = resp[1]
  sem = resp[2]
  uni = USER
  query = """INSERT INTO enrolled_in VALUES ('%s','%s','%s','%s')""" % (uni, cnum, snum, sem)
  try:
    g.conn.execute(query)
  except IntegrityError:
    print "ALREADY ENROLLED"
  return redirect('/profile')

@app.route('/enroll2', methods=['POST'])
def enroll2():
  print "HERE!!!!!"
  response = request.form['optradio']
  resp = response.split(",")
  cnum = resp[0]
  snum = resp[1]
  sem = resp[2]
  uni = USER
  if request.form['submit'] == "Enroll in this course":
    query = """INSERT INTO enrolled_in VALUES ('%s','%s','%s','%s')""" % (uni, cnum, snum, sem)
    try:
      g.conn.execute(query)
    except IntegrityError:
      print "ALREADY ENROLLED"
    return redirect('/profile')
  else:
    return more(cnum,snum,sem)

@app.route('/more', methods=['POST'])
def more(cnum,snum,sem):
  query1 = "SELECT * from sections_available_taught S, courses_offered C WHERE S.cid=C.cid AND C.cid='%s' AND S.section_n='%s' AND S.semester='%s'" %(cnum,snum,sem)
  info = courselister(query1)
  query2 = "SELECT St.s_first_name, St.s_last_name, St.sid FROM students_attends St, enrolled_in E WHERE E.cid='%s' AND E.section_n='%s' AND E.semester='%s' AND E.sid=St.sid" %(cnum,snum,sem)
  students = courselister(query2)
  fin = [info,students]
  #fin = students
  context = dict(data = fin)
  return render_template("more.html", **context)


#@app.route('/filter')
#def filter():
 # dept = request.form['department']
 # print dept
 # cursor = g.conn.execute("SELECT C.cid, C.cname, C.credits, C.dname, S.semester, S.days, S.section_time, P.p_last_name FROM courses_offered C, sections_available_taught S, professors_works P WHERE S.cid=C.cid AND S.pid=P.pid AND C.dname='Computer Science'")
#  courses = []
  #i=0
#  for result in cursor:
#    row = []
#    for i in range(0,len(result)):
        #courses.append(result[i])
#        row.append(result[i])
#    courses.append(row)
    #courses.append(result['cname'])  # can also be accessed using result[0]
    #i+=1
#  cursor.close()
#  return render_template("index.html", **context)
  
@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using:

        python server.py

    Show the help text using:

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)


  run()
