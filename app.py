from flask import Flask , render_template , request , session
import sqlite3

app = Flask("__name__")
app.secret_key = "LOL"
con = sqlite3.connect("users.db",check_same_thread=False)
c = con.cursor()

c.execute("CREATE TABLE IF NOT EXISTS Users(email TEXT , password TEXT)") #Users table which contains email and password
c.execute("CREATE TABLE IF NOT EXISTS Notes(note TEXT , email TEXT)") #Notes table which contains note and emails

@app.route("/")
def index():
	try:
		if session['email']:
			c.execute("SELECT note FROM Notes WHERE email = (?)",(session['email'],))
			return render_template("index.html",notes=c.fetchall(),session=session['email'])
	except:
		0
	
	return render_template("index.html",session="")

@app.route("/register",methods=['POST','GET'])
def register():
	email = request.form.get("email")
	password = request.form.get("password")
	if email and password:
		c.execute("INSERT INTO Users VALUES(?,?)",(email,password))
		session['email'] = email
	else:
		return render_template("index.html",error="Email or Password is empty",session="")
	con.commit();c.execute("SELECT note FROM Notes WHERE email = session['email']")
	return render_template("index.html",session=session['email'],notes=c.fetchall())

@app.route("/login",methods=['POST','GET'])
def login():
  email = request.form.get("email")
  password = request.form.get('password')
  c.execute("SELECT * FROM Users")
  for db_email,db_password in c.fetchall():
    if email == db_email and password == db_password:
      session['email'] = email
      c.execute("SELECT note FROM Notes WHERE email = (?)",(email,))
      return render_template("index.html",notes=c.fetchall(),session=session['email'])
  return render_template("index.html",session="")

@app.route("/logout",methods=['POST','GET'])
def logout():
  session['email'] = ""
  return render_template("index.html",session="")
  

@app.route("/add",methods=['POST','GET'])
def add():
	note = request.form.get("note")
	email = session['email']
	c.execute("INSERT INTO Notes VALUES(?,?)",(note,email))
	c.execute("SELECT note FROM Notes WHERE email = (?)",(email,))
	con.commit()
	return render_template("index.html",notes=c.fetchall(),session=session['email'])

@app.route("/remove",methods=['POST','GET'])
def remove():
  note = request.form.get("note")
  email = session["email"]
  c.execute("SELECT note FROM Notes WHERE note = (?)",(note,))
  print(c.fetchall())
  c.execute("DELETE FROM Notes WHERE note = (?) LIMIT 1",(note,))
  c.execute("SELECT note FROM Notes WHERE email = email")
  con.commit()
  return render_template("index.html",session=session['email'],notes=c.fetchall())


app.run(host="0.0.0.0",port=80,debug=False)
