from flask import render_template
from professor_http import professor
from app import mysql

import MySQLdb


@professor.route('/list', methods=['GET'])
def view_list_professor():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM professor')
    data = cursor.fetchall()
    return render_template('list.html', professors=data)


@professor.route('/create', methods=['GET'])
def view_create_professor():
    return render_template('create_professor.html')


@professor.route('/update/<int:id>', methods=['GET'])
def view_update_professor(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM professor WHERE id=%i" % id)
    data = cursor.fetchone()
    return render_template('update_professor.html', professor=data)

