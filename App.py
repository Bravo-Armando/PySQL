from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

import sqlite3
connection = sqlite3.connect("flaskcontact.db") 

app = Flask(__name__)

# Mysql Connection 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'armando'
app.config['MYSQL_DB'] = 'flaskcontact'
mysql = MySQL(app)

# iniciar sesion (settings)
app.secret_key='mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)',
        (fullname, phone, email))
        mysql.connection.commit()
        flash('contact aded')
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def  delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id ={0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))


@app.route('/edit/<string:id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    # concatenacion (seleccionamos todo desde contacts donde id es= le ponemos aqui)
    # cur.execute("SELECT * FROM contacts WHERE id =" + id)
    cur.execute("SELECT * FROM contacts WHERE id = %s" % (id))
    data = cur.fetchall()
    return render_template('edit-contact.html', contact = data[0])


@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
    cur = mysql.connection.cursor()
    cur.execute("""UPDATE contacts SET fullname = %s, email = %s, phone = %s WHERE id = %s""" % (fullname, email, phone, id))
    mysql.connection.commit()
    flash('Contact Updated Succesfully')
    return redirect(url_for('Index'))

#@app.route('/update/<id>', methods = ['POST'])
#def update_contact(id):
#  if request.method == 'POST':
#      fullname = request.form['fullname']
#    cur = mysql.connection.cursor()
#    cur.execute("UPDATE contacts SET fullname = %s" % (fullname)")
#    mysql.connection.commit()
#    flash('Contact Updated Successfully')
#    return redirect(url_for('Index'))

# @app.route('/edit/<id>')
# def get_contact(id):
#    cur = mysql.connection.cursor()
 #   cur.execute('SELECT FROM contacts WHERE id = {0}', (id))
  #  data = cur.fetchall()
   # print(data)
    #return 'Recieved'


if __name__=='__main__':
    app.run(port=8000, debug=True)
