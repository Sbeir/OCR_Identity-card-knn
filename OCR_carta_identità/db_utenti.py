import sqlite3
import csv

def sql_Utenti():

    conn = sqlite3.connect('biblioteca.sqlite')
    cur = conn.cursor()
    utenti = open('utenti.csv', 'r')
    utenti = tuple(csv.reader(utenti, delimiter = ','))
    utenti = tuple(utenti[-1])
    query = ('insert or replace into Utenti values (null,?,?,?,?,?,?)')
    cur.execute(query, utenti)
    conn.commit()
    conn.close()
    