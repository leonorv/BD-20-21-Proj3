#!/usr/bin/python3

from wsgiref.handlers import CGIHandler
from flask import Flask
from flask import render_template, request

## Libs postgres
import psycopg2
import psycopg2.extras

script = Flask(__name__)

DB_HOST="db.tecnico.ulisboa.pt"
DB_USER="ist192557"
DB_DATABASE="DB_USER"
DB_PASSWORD="vgvo0215"
DB_CONNECTION_STRING = "host=%s dbname=%s user=%s password=%s" % (DB_HOST, DB_DATABASE, DB_USER, DB_PASSWORD)

@script.route('/')
def inicio():
  try:
    return render_template("index.html")
  except Exception as e:
    return str(e)

@script.route('/data')
def preencher_dados():
  try:
    return render_template("instituicao.html")
  except Exception as e:
    return str(e)

@script.route('/insert', methods=["POST"])
def inserir():
  dbConn=None
  cursor=None
  print("hello";)
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "insert into instituicao values(%s, %s, %s, %s);" 
    data = (request.form["nome"], request.form["tipo"], request.form["num_regiao"], request.form["num_concelho"])
    cursor.execute(query, data)
    return query
  except Exception as e:
    print("entrou");
    return str(e) #Renders a page with the error.
  finally:
    ddConn.commit()
    cursor.close()
    dbConn.close()

@script.route('/list')
def listar_instituicoes():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "SELECT * FROM instituicao;"
    cursor.execute(query)
    return render_template("listar_instituicoes.html", cursor=cursor)
  except Exception as e:
    return str(e) #Renders a page with the error.
  finally:
    cursor.close()
    dbConn.close()

CGIHandler().run(script)

