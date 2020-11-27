#!/usr/bin/python3

from wsgiref.handlers import CGIHandler
from flask import Flask
from flask import render_template, request

## Libs postgres
import psycopg2
import psycopg2.extras

script = Flask(__name__)

DB_HOST="db.tecnico.ulisboa.pt"
DB_USER="ist192539"
DB_DATABASE=DB_USER
DB_PASSWORD="hrqm0025"
DB_CONNECTION_STRING = "host=%s dbname=%s user=%s password=%s" % (DB_HOST, DB_DATABASE, DB_USER, DB_PASSWORD)

@script.route('/')
def inicio():
  try:
    return render_template("index.html")
  except Exception as e:
    return str(e)

@script.route('/dataInstituicao')
def preencher_dados_instituicao():
  try:
    return render_template("instituicao.html")
  except Exception as e:
    return str(e)

@script.route('/dataAnalise')
def preencher_dados_analise():
  try:
    return render_template("analise.html")
  except Exception as e:
    return str(e)


@script.route('/insertInstituicao', methods=["POST"])
def inserir_instituicao():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "insert into instituicao (nome, tipo, num_concelho, num_regiao) values(%s, %s, %s, %s);" 
    data = (request.form["nome"], request.form["tipo"], request.form["num_concelho"], request.form["num_regiao"])
    cursor.execute(query, data)
    return query
  except Exception as e:
    return str(e) #Renders a page with the error.
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()

@script.route('/insertAnalise', methods=["POST"])
def inserir_analise():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "insert into analise (num_analise, especialidade, num_cedula, num_doente, dia_hora, data_registo, nome, quant, inst) values(%s, %s, %s, %s, %s, %s, %s, %s, %s);" 
    data = (request.form["num_analise"], request.form["especialidade"], request.form["num_cedula"], request.form["num_doente"], request.form["dia_hora"], request.form["data_registo"], request.form["nome"], request.form["quant"], request.form["inst"])
    cursor.execute(query, data)
    return query
  except Exception as e:
    return str(e) #Renders a page with the error.
  finally:
    dbConn.commit()
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

