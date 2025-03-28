from flask import Flask, request, render_template, redirect, url_for
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
app = Flask(__name__)

db = sqlite3.connect('login_password.db')
sql = db.cursor()


sql.execute("""CREATE TABLE IF NOT EXISTS users(
    vards TEXT,
    title TEXT, 
    article TEXT
)""")

sql.execute('''CREATE TABLE IF NOT EXISTS passwords(
id_user INTEGER PRIMARY KEY AUTOINCREMENT,
login TEXT,
parole TEXT);''')
db.commit()

sql.close()
db.close()

    
@app.route('/')
def ieeja():
  return render_template("ieeja.html")

@app.route('/reg_bad')
def reg_bad():
  return render_template("reg_bad.html")

@app.route('/kontakti')
def kontakti():
  return render_template("kontakti.html")

@app.route('/index_start')
def index_stat():
  return render_template("index_start.html")

@app.route('/authorization', methods=['GET', 'POST'])
def form_authorization():
    if request.method == 'POST':
      login = request.form.get('Login')
      parole = request.form.get('Password')
      db = sqlite3.connect('login_password.db')
      sql = db.cursor()
      info = sql.execute(('''SELECT login FROM passwords WHERE login = '{}';''').format(login)).fetchone()
      if info is None:
        return render_template ("auth_bad.html")
      sql.execute(('''SELECT parole FROM passwords WHERE login = '{}';''').format(login))
      pwd = sql.fetchone()
      print(pwd)
      sql.close()
      pwd=pwd[0]  
      p = check_password_hash(pwd,parole)
      if not p:
        return render_template('auth_bad.html')
      return render_template('index_start.html')
    return render_template('authorization.html')

@app.route('/pass_generator')
def pass_generator():
    return render_template("pass_generator.html")


@app.route('/registration', methods=['GET', 'POST'])
def form_registration():
   if request.method == 'POST':
       login = request.form.get('Login')
       parole = request.form.get('Password')
       parole2 = request.form.get('Password2')
       if parole != parole2:
        return redirect(url_for("reg_bad"))      
       rez = [login,generate_password_hash(parole)]
       db = sqlite3.connect('login_password.db')
       sql = db.cursor()
       info = sql.execute(('''SELECT login FROM passwords WHERE login = '{}';''').format(login)).fetchone()
       if info is None:
           sql.execute("INSERT INTO passwords(login,parole) VALUES(?,?)",rez)
           sql.close()
           db.commit()
           db.close()
           return render_template('successfulregis.html')
       info=info[0]
       if login == info:
            return redirect(url_for("reg_bad"))    
   return render_template('registration.html')

@app.route('/palidziba',methods=['POST','GET'])
def palidziba():
  if request.method == "POST":
        vards = request.form["vards"]
        title = request.form["title"]
        article = request.form["article"]
        rez = [vards,title,article]
        db = sqlite3.connect('login_password.db')
        sql = db.cursor()
        sql.execute("INSERT INTO users VALUES(?,?,?)",rez)
        db.commit()
        db.close()
  return render_template('palidziba.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)