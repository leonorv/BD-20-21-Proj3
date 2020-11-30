#!/usr/bin/python3

from wsgiref.handlers import CGIHandler
from flask import Flask
from flask import render_template, request
from datetime import date

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
    query2 = "select max(num_analise) from analise;"
    cursor.execute(query2)
    records = cursor.fetchall()
    last_num_analise = records[0][0]
    current_date = date.today()
    if len(request.form["num_cedula"])==0 and len(request.form["num_doente"])==0 and len(request.form["dia_hora"])==0:
      data = (last_num_analise+1, request.form["especialidade"], None, None, None, current_date.strftime("%y-%m-%d"), request.form["nome"], request.form["quant"], request.form["inst"])
    else:
      data = (last_num_analise+1, request.form["especialidade"], request.form["num_cedula"], request.form["num_doente"], request.form["dia_hora"], current_date.strftime("%y-%m-%d"), request.form["nome"], request.form["quant"], request.form["inst"])
  
    cursor.execute(query1, data)
    return query1
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
    query = "update analise set especialidade=%s, num_cedula=%s, num_doente=%s, dia_hora=%s, data_registo=%s, nome=%s, quant=%s, inst=%s where num_analise=%s;"
    data = (request.form["especialidade"], request.form["num_cedula"], request.form["num_doente"], request.form["dia_hora"], request.form["data_registo"], request.form["nome"], request.form["quant"], request.form["inst"], request.form["num_analise"])
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
    query1 = "insert into medico (num_cedula, nome, especialidade) values(%s, %s, %s);" 
    query2 = "select max(num_cedula) from medico;"
    cursor.execute(query2)
    records = cursor.fetchall()
    last_num_cedula = records[0][0]
    data = (last_num_cedula+1, request.form["nome"], request.form["especialidade"])
    cursor.execute(query1, data)
    return query1
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
    query = """insert into prescricao (num_cedula, num_doente, dia_hora, substancia, quant) values (%s, %s, %s, %s, %s);"""
    data = (request.form["num_cedula"], request.form["num_doente"], request.form["dia_hora"], request.form["substancia"], request.form["quant"])
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
    query = "update prescricao set num_cedula=%s, num_doente=%s, dia_hora=%s, substancia=%s, quant=%s where num_cedula=%s and num_doente=%s and data=%s and substancia=%s;"
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
    data = (request.args["num_cedula"], request.args["num_doente"], request.args["dia_hora"], request.args["substancia"])
    cursor.execute(query, data)
    return query
  except Exception as e:
    return str(e) #Renders a page with the error.
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()



#venda farmacia sem prescricao
@script.route('/data_venda_farmacia_sem_prescricao')
def preencher_dados_venda_farmacia_sem_prescricao():
  try:
    return render_template("venda_farmacia_sem_prescricao.html")
  except Exception as e:
    return str(e)

@script.route('/insert_venda_farmacia_sem_prescricao', methods=["POST"])
def inserir_venda_farmacia_sem_prescricao():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query1 = """insert into VendaFarmacia (num_venda, inst, data_registo, substancia, quant, preco) values (%s, %s, %s, %s, %s, %s);"""
    query2 = "select max(num_venda) from VendaFarmacia;"
    cursor.execute(query2)
    records = cursor.fetchall()
    last_num_venda = records[0][0]
    current_date = date.today()
    data = (last_num_venda+1, request.form["num_doente"], current_date.strftime("%y-%m-%d"), request.form["substancia"], request.form["quant"])
    cursor.execute(query1, data)
    return query1
  except Exception as e:
    return str(e) #Renders a page with the error.
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()

#venda farmacia com prescricao
@script.route('/data_venda_farmacia_com_prescricao')
def preencher_dados_venda_farmacia_com_prescricao():
  try:
    return render_template("venda_farmacia_com_prescricao.html")
  except Exception as e:
    return str(e)

@script.route('/insert_venda_farmacia_com_prescricao', methods=["POST"])
def inserir_venda_farmacia_com_prescricao():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)

    query3 = "select max(num_venda) from VendaFarmacia;"
    cursor.execute(query3)
    records = cursor.fetchall()
    last_num_venda = records[0][0]
    current_date = date.today()

    query2 = """insert into VendaFarmacia (num_venda, inst, data_registo, substancia, quant, preco) values (%s, %s, %s, %s, %s, %s);"""
    data2 = (last_num_venda+1, request.form["inst"], current_date.strftime("%y-%m-%d"), request.form["substancia"], request.form["quant"], request.form["preco"])
    cursor.execute(query2,data2)

    query1 = """insert into PrescricaoVenda (num_cedula, num_doente, dia_hora, substancia, num_venda) values (%s, %s, %s, %s, %s);"""
    data1 = (request.form["num_cedula"], request.form["num_doente"], request.form["dia_hora"], request.form["substancia"], last_num_venda+1)
    cursor.execute(query1, data1)
    return query2
  except Exception as e:
    return str(e) #Renders a page with the error.
  finally:
    dbConn.commit()
    cursor.close()
    dbConn.close()


#listar substancias
@script.route('/data_substancia')
def escolher_dados_substancia():
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "select * from medico;"
    cursor.execute(query)
    return render_template("escolher_substancia.html", cursor = cursor)
  except Exception as e:
    return str(e)

@script.route('/listar_substancias', methods=["POST"])
def listar_substancias():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    
    query = "select distinct substancia from prescricao where num_cedula=%s and extract(month from dia_hora)=%s and extract(year from dia_hora)=%s;"
    data = (request.form["num_cedula"], request.form["mes"][5:7], request.form["mes"][0:4])
    cursor.execute(query, data)
    return render_template("listar_substancias.html", cursor = cursor)
  except Exception as e:
    return str(e) #Renders a page with the error.
  finally:
    cursor.close()
    dbConn.close()

#listar valores de glicemia
@script.route('/data_glicemia')
def listar_glicemia():
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor1 = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    cursor2 = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    cursor = [cursor1, cursor2]
    query1 = "select c.nome, a.num_doente, a.quant from analise as a, instituicao as i, concelho as c \
              where a.nome = 'Glicémia' and a.inst = i.nome and i.num_concelho = c.num_concelho and a.quant >= ALL (select a.quant from analise as a, instituicao as i, concelho as c1 \
              where a.nome = 'Glicémia' and a.inst = i.nome and i.num_concelho = c1.num_concelho and c1.num_concelho = c.num_concelho);"
            
    query2 = "select c.nome, a.num_doente, a.quant from analise as a, instituicao as i, concelho as c \
              where a.nome = 'Glicémia' and a.inst = i.nome and i.num_concelho = c.num_concelho and a.quant <= ALL (select a.quant from analise as a, instituicao as i, concelho as c1 \
              where a.nome = 'Glicémia' and a.inst = i.nome and i.num_concelho = c1.num_concelho and c1.num_concelho = c.num_concelho);"

    cursor[0].execute(query1)
    cursor[1].execute(query2)
    return render_template("listar_glicemia.html", cursor = cursor)
  except Exception as e:
    return str(e)








CGIHandler().run(script)
