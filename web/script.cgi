#!/usr/bin/python3

from wsgiref.handlers import CGIHandler
from flask import Flask
from flask import render_template, request

## Libs postgres
import psycopg2
import psycopg2.extras

script = Flask(__name__)

DB_HOST="db.tecnico.ulisboa.pt"
DB_USER="ist192509"
DB_DATABASE=DB_USER
DB_PASSWORD="dqav4036"
DB_CONNECTION_STRING = "host=%s dbname=%s user=%s password=%s" %(DB_HOST, DB_DATABASE, DB_USER, DB_PASSWORD)

@script.route('/')
def inicio():
  try:
    return render_template("index.html")
  except Exception as e:
    return str(e)

#instituicao

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
  except Exception as e:
    return str(e)

@script.route('/update_inst', methods=["POST"])
def update_inst():
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

@script.route('/list_inst')
def listar_inst():
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

#analise

@script.route('/data_analise')
def preencher_dados_analise():
  try:
    return render_template("analise.html")
  except Exception as e:
    return str(e)

@script.route('/insert_analise', methods=["POST"])
def inserir_analise():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query1 = "insert into analise (num_analise, especialidade, num_cedula, num_doente, dia_hora, data_registo, nome, quant, inst) values(%s, %s, %s, %s, %s, %s, %s, %s, %s);" 
    query2 = "select max(num_analise) FROM analise;"
    last_num_analise = cursor.execute(query2);
    data = (last_num_analise+1, request.form["especialidade"], request.form["num_cedula"], request.form["num_doente"], request.form["dia_hora"], request.form["data_registo"], request.form["nome"], request.form["quant"], request.form["inst"])
    cursor.execute(query1, data)
    return query
  except Exception as e:
    return str(e) #Renders a page with the error.
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()

@script.route('/list_analises')
def listar_analises():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "SELECT * FROM analise;"
    cursor.execute(query)
    return render_template("listar_analises.html", cursor=cursor)
  except Exception as e:
    return str(e) #Renders a page with the error.
  finally:
    cursor.close()
    dbConn.close()

@script.route('/alterar_analise')
def alterar_dados_analise():
  try:
    return render_template("alterar_analise.html", params=request.args)
  except Exception as e:
    return str(e)

@script.route('/update_analise', methods=["POST"])
def update_analise():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "update analise set num_analise=%s, especialidade=%s, num_cedula=%s, dia_hora=%s, data_registo=%s, nome=%s, quant=%s, inst=%s where num_analise=%s;"
    data = (request.form["num_analise"], request.form["especialidade"], request.form["num_cedula"], request.form["num_doente"], request.form["dia_hora"], request.form["data_registo"], request.form["nome"], request.form["quant"], request.form["inst"], request.form["num_analise"])
    cursor.execute(query, data)
    return query
  except Exception as e:
    return str(e)
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()

@script.route('/remover_analise')
def remover_analise():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "delete from analise where num_analise=%s;"
    data = (request.args["num_analise"],)
    cursor.execute(query, data)
    return query
  except Exception as e:
    return str(e) #Renders a page with the error.
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()

#medico

@script.route('/data_medico')
def preencher_dados_medico():
  try:
    return render_template("medico.html")
  except Exception as e:
    return str(e)

@script.route('/insert_medico', methods=["POST"])
def inserir_medico():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "insert into medico (num_cedula, nome, especialidade) values(%s %s, %s);" 
    data = (last_num_cedula, request.form["nome"], request.form["especialidade"])
    last_num_cedula += 1
    cursor.execute(query, data)
    return query
  except Exception as e:
    return str(e) #Renders a page with the error.
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()

@script.route('/alterar_medico')
def alterar_dados_medico():
  try:
    return render_template("alterar_medico.html", params=request.args)
  except Exception as e:
    return str(e)

@script.route('/update_medico', methods=["POST"])
def update_medico():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "update medico set nome=%s, especialidade=%s where num_cedula=%s;"
    data = (request.form["nome"], request.form["especialidade"], request.form["num_cedula"])
    cursor.execute(query, data)
    return query
  except Exception as e:
    return str(e)
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()

@script.route('/list_medicos')
def listar_medicos():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "SELECT * FROM medico;"
    cursor.execute(query)
    return render_template("listar_medicos.html", cursor=cursor)
  except Exception as e:
    return str(e) #Renders a page with the error.
  finally:
    cursor.close()
    dbConn.close()
    
    
@script.route('/remover_medico')
def remover_medico():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "delete from medico where num_cedula=%s;"
    data = (request.args["num_cedula"],)
    cursor.execute(query, data)
    return query
  except Exception as e:
    return str(e) #Renders a page with the error.
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()
  
#prescricao

@script.route('/data_prescricao')
def preencher_dados_prescricao():
  try:
    return render_template("prescricao.html")
  except Exception as e:
    return str(e)

@script.route('/insert_prescricao', methods=["POST"])
def inserir_prescricao():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = """insert into prescricao (num_cedula, num_doente, data, substancia, num_venda) values (%s, %s, %s, %s, %s);"""
    data = (request.form["num_cedula"], request.form["num_doente"], request.form["data"], request.form["substancia"], request.form["num_venda"])
    cursor.execute(query, data)
    return query
  except Exception as e:
    return str(e) #Renders a page with the error.
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()

@script.route('/alterar_prescricao')
def alterar_dados_prescricao():
  try:
    return render_template("alterar_prescricao.html", params=request.args)
  except Exception as e:
    return str(e)


@script.route('/update_prescricao', methods=["POST"])
def update_prescricao():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "update prescricao set num_cedula=%s, num_doente=%s, data=%s, substancia=%s, quant=%s where num_cedula=%s and num_doente=%s and data=%s and substancia=%s;"
    data = (request.form["nova_cedula"], request.form["novo_doente"], request.form["nova_data"], request.form["nova_substancia"], request.form["nova_quant"], request.form["num_cedula"], request.form["num_doente"], request.form["data"], request.form["substancia"])
    cursor.execute(query, data)
    return query
  except Exception as e:
    return str(e)
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()

@script.route('/list_prescricoes')
def listar_prescricao():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "SELECT * FROM prescricao;"
    cursor.execute(query)
    return render_template("listar_prescricoes.html", cursor=cursor)
  except Exception as e:
    return str(e) #Renders a page with the error.
  finally:
    cursor.close()
    dbConn.close()

@script.route('/remover_prescricao')
def remover_prescricao():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "delete from prescricao where num_cedula=%s and num_doente=%s and dia_hora=%s and substancia=%s;"
    data = (request.args["num_cedula"], request.args["num_doente"], request.args["dia_ho"], request.args["substancia"])
    cursor.execute(query, data)
    return query
  except Exception as e:
    return str(e) #Renders a page with the error.
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()


CGIHandler().run(script)