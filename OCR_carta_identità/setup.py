import sqlite3
import csv

def create():
    """
    Crea il database "biblioteca" e le tabelle
    "Prestiti", "Libri", "Utenti", "Categorie"
    e "Autori" in sqlite3
    """
    
    db_biblioteca = 'biblioteca.sqlite'
    conn = sqlite3.connect(db_biblioteca)
    conn.close()
    
    
    conn = sqlite3.connect('file:biblioteca.sqlite?mode=rw', uri=True)
    conn.execute("pragma foreign_keys = 1") # Rimedio a malfunzionamento foreign keys
    cur = conn.cursor()
    
    Utenti_sql = """
        create table if not exists Utenti (
            tessera        integer primary key autoincrement,
            nome           varchar(255) not null,
            cognome        varchar(255) not null,
            data_reg       date not null,
            telefono       varchar(255) not null,
            indirizzo      varchar(255) not null,
            email          varchar(255));"""
    cur.execute(Utenti_sql)
    conn.commit()
    conn.close()
    
def start_utenti():
    """
    Carica i dati della tabella "Utenti"
    nel rispettivo csv.
    """
    utenti = open('utenti.csv', 'w+')
    utenti.close()
    with open('utenti.csv', 'w', newline = '') as utenti:
        headers = ['tessera', 'nome', 'cognome', 'data_registrazione',
                   'telefono', 'indirizzo', 'email']
        writer = csv.DictWriter(utenti, fieldnames = headers)
        writer.writeheader()
    conn = sqlite3.connect('biblioteca.sqlite')
    cur = conn.cursor()
    cur.execute('select * from Utenti')
    utenti = csv.writer(open('utenti.csv', 'a', newline = ''))
    rows = cur.fetchall()
    utenti.writerows(rows)
    conn.commit()
    conn.close()
    
def popola_utenti():
    """
    Popola la tabella "Utenti" con 3 entries.
    """
    start_utenti()
    ut_1 = {
        'nome': 'Ugo',
        'cognome': 'Fantozzi',
        'data_registrazione': '2021-03-27',
        'telefono': 3428765645,
        'indirizzo': 'Roma, Via Giovanni Battista Bodoni 79',
        'email': 'ugo.fantozzi@gmail.com'}
    ut_2 = {
        'nome': 'Piero',
        'cognome': 'Scotti',
        'data_registrazione': '2021-02-21',
        'telefono': 3489991717,
        'indirizzo': 'Miradolo, Via Franco 17',
        'email': 'pierscott@hotmail.com'}
    ut_3 = {
        'nome': 'Guida',
        'cognome': 'Lavespa',
        'data_registrazione': '2021-04-01',
        'telefono': 3474511910,
        'indirizzo': 'Milano, Via Piaggio 90',
        'email': 'guida.50special@tiscali.com'}
    with open('utenti.csv', 'a', newline = '') as file:
        headers = ['nome', 'cognome', 'data_registrazione',
                   'telefono', 'indirizzo', 'email']
        utenti = csv.DictWriter(file, fieldnames = headers)
        utenti.writerow(ut_1)
        utenti.writerow(ut_2)
        utenti.writerow(ut_3)
    conn = sqlite3.connect('biblioteca.sqlite')
    cur = conn.cursor()
    utenti = open('utenti.csv', 'r')
    next(utenti)
    utenti = tuple(csv.reader(utenti, delimiter = ','))
    query = ('insert or replace into Utenti values (null,?,?,?,?,?,?)')
    cur.executemany(query, utenti)
    conn.commit()
    conn.close()
    start_utenti()


if __name__ == "__main__":
    create()
    popola_utenti()
    