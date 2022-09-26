from flask import Flask, request, redirect, url_for, render_template
from flask_mysqldb import MySQL

import flask
import MySQLdb.cursors
import json
import decimal_encoder as de

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'web-db-service'
app.config['MYSQL_USER'] = 'professorDB_user'
app.config['MYSQL_PASSWORD'] = 'mysql'
app.config['MYSQL_DB'] = 'professorDB'
app.config['MYSQL_PORT'] = 3306


mysql = MySQL(app)


@app.route('/', methods=['GET'])
@app.route('/professors/list', methods=['GET'])
def professor_list():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM professor')
    data = cursor.fetchall()
    return render_template('index.html', professors=data)


@app.route('/professors/create', methods=['GET'])
def view_create_professor():
    return render_template('create_professor.html')


@app.route('/professors/update/<int:id>', methods=['GET'])
def view_update_professor(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM professor WHERE id=%i" % id)
    data = cursor.fetchone()
    return render_template('update_professor.html', professor=data)


@app.route('/professors', methods=['GET'])
def get_professors_list():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM professor')
    data = cursor.fetchall()
    resp = flask.Response(json.dumps(data, cls=de.DecimalEncoder))
    resp.headers['Content-Type'] = 'application/json'
    return resp


@app.route('/professors', methods=['POST'])
def add_and_update_professor():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    data = request.form

    if 'id' in data:
        cursor.execute("UPDATE professor SET first_name='%s', last_name='%s', city='%s', address='%s', salary=%f WHERE id=%i" % 
                   (data['first_name'], data['last_name'], data['city'], data['address'], float(data['salary']), int(data['id'])))
    else:
        cursor.execute("INSERT INTO professor (first_name, last_name, city, address, salary) VALUES ('%s', '%s', '%s', '%s', %s)" % 
                    (data['first_name'], data['last_name'], data['city'], data['address'], data['salary']))

    mysql.connection.commit()
    resp = flask.Response(json.dumps({'result': 'ok'}))
    resp.headers['Content-Type'] = 'application/json'
    return redirect(url_for('professor_list'))


@app.route('/professors', methods=['DELETE'])
def delete_professor():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    data = request.json
    cursor.execute("DELETE FROM professor WHERE id=%i" % (data['id']))
    mysql.connection.commit()
    resp = flask.Response(json.dumps({'result': 'ok'}))
    resp.headers['Content-Type'] = 'application/json'
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)
