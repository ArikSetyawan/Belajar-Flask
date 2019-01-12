from flask import Flask, render_template, url_for, request, redirect, session, escape
import pymysql
import datetime
import socket

app = Flask(__name__)

db = pymysql.connect("localhost","root","","arik")
cursor = db.cursor()

@app.route('/')
def home():
	act = "/"
	ipaddress = socket.gethostbyname(socket.gethostname())
	waktu = datetime.datetime.now()
	if not session.get('logged_in'):
		username = "GUEST"
		cursor.execute("INSERT INTO loguser(namauser,waktu,ipaddress,activity)VALUES(%s,%s,%s,%s)",(username,waktu,ipaddress,act))
		db.commit()
		return render_template('index.html')
	else:
		cursor.execute("SELECT * FROM pesan")
		data = cursor.fetchall()
		print data[0]
		sesi_user = escape(session['username']).capitalize()
		cursor.execute("INSERT INTO loguser (namauser,waktu,ipaddress,activity) VALUES(%s,%s,%s,%s)",(sesi_user,waktu,ipaddress,act))
		db.commit()
		return render_template('menu.html', pesan = data, nama_user = sesi_user)

@app.route('/login', methods=["GET","POST"])
def login():
	if request.method == 'POST':
		waktu = datetime.datetime.now()
		username = request.form['username']
		password = request.form['password']
		ipaddress = socket.gethostbyname(socket.gethostname())
		pesan = None
		user = cursor.execute("SELECT * FROM user WHERE username=%s and password=%s",(username,password))
		if user is not 0:
			session['logged_in'] = True
			session['username'] = request.form['username']
			act = "/login"
			cursor.execute("INSERT INTO loguser (namauser, waktu, ipaddress, activity)VALUES (%s,%s,%s,%s)",(username,waktu,ipaddress,act))
			db.commit()
			return redirect(url_for('home'))
		else:
			pesan = "username / password Gk coocok"
			return render_template('login.html', pesan = pesan)
	else:
		return render_template('login.html')

@app.route('/daftar/', methods=["GET","POST"])
def daftar():
	if request.method == 'GET':
		waktu = datetime.datetime.now()
		act = "/daftar/"
		username = "GUEST"
		ipaddress = socket.gethostbyname(socket.gethostname())
		cursor.execute("INSERT INTO loguser (namauser,waktu,ipaddress,activity)VALUES(%s,%s,%s,%s)",(username,waktu,ipaddress,act))
		db.commit()
		return render_template("daftar.html")
	else:
		nama = request.form['nama']
		username = request.form['username']
		email = request.form['email']
		password = request.form['password']

		cursor.execute("INSERT INTO user (nama,username,email,password)VALUES (%s,%s,%s,%s)",(nama,username,email,password))
		db.commit()
		return render_template('login.html')

@app.route('/logout')
def logout():
	username = escape(session['username']).capitalize()
	act = "/logout"
	waktu = datetime.datetime.now()
	ipaddress = socket.gethostbyname(socket.gethostname())
	cursor.execute("INSERT INTO loguser (namauser, waktu, ipaddress, activity)VALUES (%s,%s,%s,%s)",(username,waktu,ipaddress,act))
	db.commit()
	session['logged_in']=False
	return redirect(url_for('home'))

@app.route('/tambahbarang/', methods=["GET","POST"])
def tambahbarang():
	if request.method == 'GET':
		return render_template('tbhData.html')
	else:
		waktu = datetime.datetime.now()
		pesan = request.form['pesan']
		usrnama = request.form['usrnama']
		act = "/tambahbarang/"
		ipaddress = socket.gethostbyname(socket.gethostname())
		cursor.execute("INSERT INTO loguser (namauser, waktu, ipaddress, activity)VALUES (%s,%s,%s,%s)",(usrnama,waktu,ipaddress,act))
		cursor.execute("INSERT INTO pesan (namauser,pesan,waktu)VALUES(%s,%s,%s)",(usrnama,pesan,waktu))
		db.commit()
		return redirect(url_for('home'))

@app.route('/log')
def log():
	waktu = datetime.datetime.now()
	act = "/log"
	ipaddress = socket.gethostbyname(socket.gethostname())
	if not session.get('logged_in'):
		username = "GUEST"
		cursor.execute("INSERT INTO loguser (namauser,waktu,ipaddress,activity)VALUES(%s,%s,%s,%s)",(username,waktu,ipaddress,act))
		db.commit()
		cursor.execute("SELECT * FROM loguser order by id desc")
		datalog = cursor.fetchall()
		return render_template("log.html", datalog = datalog)
	else:	
		username = escape(session['username']).capitalize()
		cursor.execute("INSERT INTO loguser (namauser,waktu,ipaddress,activity)VALUES(%s,%s,%s,%s)",(username,waktu,ipaddress,act))
		db.commit()
		cursor.execute("SELECT * FROM loguser order by id desc")
		datalog = cursor.fetchall()
		return render_template("log.html", datalog = datalog)

@app.route('/loginv2')
def loginv2():
	return render_template('loginv2.html')

@app.route('/daftarv2')
def daftarv2():
	return render_template('daftarv2.html')
"""
@app.route('/editbarang/', methods=["GET","POST"])
def editbarang():
	if request.method == 'GET':
		brglama = request.args.get('brglama').encode('utf-8')
		types = type(brglama)
		pesan = brglama

		#datas = cursor.execute("SELECT * FROM barang WHERE nama_barang=%s",(brglama))		
		return render_template('editbrg.html', pesan=pesan,typed=types)
	else:
		nama_brg = request.form['namabrg']
		jumlah_brg = request.form['jumlahbrg']
		harga_brg = request.form['hargabrg']

		cursor.execute("UPDATE barang SET namabrg=%s, jumlahbrg=%s, hargabrg=%s",(nama_brg,jumlah_brg,harga_brg))
		db.commit()
		return redirect(url_for('home'))


@app.route('/deletebarang/', methods=["POST"])
def deletebarang():
	return "barang Delete" """ 

if __name__ == '__main__':
	app.secret_key = "arik212"
	app.run(debug = True)