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
DB_DATABASE=DB_USER
DB_PASSWORD="vgvo0215"
DB_CONNECTION_STRING = "host=%s dbname=%s user=%s password=%s" %(DB_HOST, DB_DATABASE, DB_USER, DB_PASSWORD)

@script.route('/')
def inicio():
  try:
    return render_template("index.html")
  except Exception as e:
    return str(e)

@script.route('/data_inst')
def preencher_dados_inst():
  try:
    return render_template("instituicao.html")
  except Exception as e:
    return str(e)

@script.route('/alterar_inst')
def alterar_dados_inst():
  try:
    return render_template("alterar_inst.html", params=request.args)

@script.route('/data_analise')
def preencher_dados_analise():
  try:
    return render_template("analise.html")
  except Exception as e:
    return str(e)


@script.route('/update_inst', methods=["POST"])
def update_balance():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "update instituicao set nome=%s, tipo=%s, num_concelho=%s, num_regiao=%s where nome=%s;"
    data = (request.form["nome"], request.form["tipo"], request.form["num_concelho"], request.form["num_regiao"], request.form["nome_antigo"])
    cursor.execute(query, data)
    return query
  except Exception as e:
    return str(e)
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()

@script.route('/insert_inst', methods=["POST"])
def inserir_inst():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = """insert into instituicao (nome, tipo, num_concelho, num_regiao) values (%s, %s, %s, %s);"""
    data = (request.form["nome"], request.form["tipo"], request.form["num_concelho"], request.form["num_regiao"])
    cursor.execute(query, data)
    return query
  except Exception as e:
    return str(e) #Renders a page with the error.
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()

@script.route('/remover_inst')
def remover_inst():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "delete from instituicao where nome=%s;"
    data = (request.args["nome"],)
    cursor.execute(query, data)
    return query
  except Exception as e:
    return str(e) #Renders a page with the error.
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()


@script.route('/insert_analise', methods=["POST"])
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
def listar():
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

