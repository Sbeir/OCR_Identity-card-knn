from flask import Flask, render_template, url_for, request, redirect
from flask import flash
import db_utenti 
import os
import main
import csv
from datetime import date
from setup import start_utenti
import sqlite3

app = Flask(__name__, template_folder="webui")
app.static_folder = 'static'
app.secret_key = 'seilasalvezza'


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/', methods=['POST', 'GET'])
def upload_file():
    global nome, cognome
    num = len(os.listdir('card')) + 1
    uploaded_file = request.files['file']
    uploaded_file.filename = f'card_{num}.png'
    if uploaded_file.filename != '':
        uploaded_file.save(os.path.join('card', uploaded_file.filename))
        nome, cognome = main.main() 
    return redirect(url_for('registrazione'))


@app.route('/registrazione')
def registrazione():
    return render_template('registrazione.html', nome=nome, cognome=cognome)
    

#prendere i dati inseriti del form 
@app.route('/registrazione', methods=['POST', 'GET'])
def get_form():
    global tel, ind, email
    start_utenti()
    utente = {}
    utente['nome'] = request.form['nome']
    utente['cognome'] = request.form['cognome']
    today = date.today()
    utente['data_registrazione'] = today.strftime("%Y-%m-%d")
    tel = utente['telefono'] = request.form['tel']
    ind = utente['indirizzo'] = request.form['ind']
    email = utente['email'] = request.form['email']
    
    #check input telefono
    try:
        utente['telefono'] = int(utente['telefono'])
    except:
        flash("Telefono non valido")
        #return redirect(url_for('registrazione'))
        return render_template('registrazione.html', nome=nome, cognome=cognome, ind=ind, email=email)
    utente['telefono'] = str(utente['telefono'])
    #check telefono
    conn = sqlite3.connect('biblioteca.sqlite')
    cur = conn.cursor()
    cur.execute('select telefono from Utenti')
    tel_ut = cur.fetchall()
    tel_check = (utente['telefono'],)
    conn.commit()
    conn.close()  
    if any(i == tel_check for i in tel_ut):
        flash("Telefono già utilizzato")
        #return redirect(url_for('registrazione'))
        return render_template('registrazione.html', nome=nome, cognome=cognome, ind=ind, email=email)

    
    # #check email 
    conn = sqlite3.connect('biblioteca.sqlite')
    cur = conn.cursor()
    cur.execute('select email from Utenti')
    mail_ut = cur.fetchall()
    mail_check = (utente['email'],)
    conn.commit()
    conn.close()  
    if any(m == mail_check for m in mail_ut):
        flash("email già utilizzata")
        #return redirect(url_for('registrazione'))
        return render_template('registrazione.html', nome=nome, cognome=cognome, tel=tel, ind=ind)

    
    with open('utenti.csv', 'a', newline = '') as file:
        headers = ['nome', 'cognome', 'data_registrazione',
                'telefono', 'indirizzo', 'email']
        utenti = csv.DictWriter(file, fieldnames = headers)
        utenti.writerow(utente)
    db_utenti.sql_Utenti()  
    start_utenti()         
       
    return render_template('reg_effettuata.html')


@app.route("/reg_effettuata")
def reg_effettuata():
    return redirect('/')



if __name__ == "__main__":
    app.run()