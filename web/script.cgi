 #!/usr/bin/python3

from wsgiref.handlers import CGIHandler
from flask import Flask
from flask import render_template, request

## Libs postgres
import psycopg2
import psycopg2.extras

app = Flask(__name__)

DB_HOST="db.tecnico.ulisboa.pt"
DB_USER="ist192539"
DB_DATABASE=DB_USER
DB_PASSWORD="dqav4036"
DB_CONNECTION_STRING = "host=%s dbname=%s user=%s password=%s" % (DB_HOST, DB_DATABASE, DB_USER, DB_PASSWORD)

@app.route('/')
def inserir_instituicao():
  dbConn=None
  cursor=None
  try:
    dbConn = psycopg2.connect(DB_CONNECTION_STRING)
    cursor = dbConn.cursor(cursor_factory = psycopg2.extras.DictCursor)
    query = "INSERT INTO instituicao (nome, tipo, num_regiao, num_concelho) VALUES (%s, %s, %s, %s);"
    data = (request.form["nome"], request.form["tipo"], request.form["num_regiao"], request.form["num_concelho"]) 
    cursor.execute(query, data)
    return render_template("index.html", cursor=cursor)
  except Exception as e:
    return str(e) #Renders a page with the error.
  finally:
    cursor.close()
    dbConn.close()

CGIHandler().run(app)