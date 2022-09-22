from flask import Blueprint, request, redirect, url_for
from app import mysql

import flask
import MySQLdb.cursors
import json
import decimal_encoder as de

professor = Blueprint("professors", __name__)

@professor.route('/', methods=['GET'])
def get_professors_list():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM professor')
    data = cursor.fetchall()
    resp = flask.Response(json.dumps(data, cls=de.DecimalEncoder))
    resp.headers['Content-Type'] = 'application/json'
    return resp


@professor.route('/', methods=['POST'])
def add_professor():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    data = request.form
    cursor.execute("INSERT INTO professor (first_name, last_name, city, address, salary) VALUES ('%s', '%s', '%s', '%s', %s)" % 
                   (data['first_name'], data['last_name'], data['city'], data['address'], data['salary']))
    mysql.connection.commit()
    resp = flask.Response(json.dumps({'result': 'ok'}))
    resp.headers['Content-Type'] = 'application/json'
    return redirect(url_for('.view_list_professor'))


@professor.route('/', methods=['PUT'])
def update_professor():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    data = request.json
    cursor.execute("UPDATE professor SET first_name='%s', last_name='%s', city='%s', address='%s', salary=%f WHERE id=%i" % 
                   (data['first_name'], data['last_name'], data['city'], data['address'], data['salary'], data['id']))
    
    mysql.connection.commit()
    resp = flask.Response(json.dumps({'result': 'ok'}))
    resp.headers['Content-Type'] = 'application/json'
    return resp


@professor.route('/', methods=['DELETE'])
def delete_professor():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    data = request.json
    cursor.execute("DELETE FROM professor WHERE id=%i" % (data['id']))
    mysql.connection.commit()
    resp = flask.Response(json.dumps({'result': 'ok'}))
    resp.headers['Content-Type'] = 'application/json'
    return resp