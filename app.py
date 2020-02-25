from flask import Flask, redirect, request, url_for, session, flash, render_template
from flask_mysqldb import MySQL
from functools import wraps
from wtforms import Form, StringField, BooleanField, validators

app = Flask(__name__)

# config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'todo'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

class TodoForm(Form):
    text = StringField('text', [validators.Length(min=1, max=255)])
    complete = BooleanField('complete')


@app.route('/', methods=['GET', 'POST'])
def index():
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM todo")
    todo_list = cur.fetchall()

    form = TodoForm(request.form)
    if request.method == 'POST':
        text = form.text.data

        # add todo to database
        cur.execute("INSERT INTO todo(text) VALUES(%s)", [text])

        # commit to db
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('index'))
    return render_template('index.html', todo_list=todo_list, form=form)


@app.route('/complete_todo/<string:id>', methods=['POST', 'GET'])
def complete_todo(id):
    cur = mysql.connection.cursor()

    cur.execute('UPDATE todo SET complete=1 WHERE id = %s', [id])
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('index'))


@app.route('/uncomplete_todo/<string:id>', methods=['POST', 'GET'])
def uncomplete_todo(id):
    cur = mysql.connection.cursor()

    cur.execute('UPDATE todo SET complete=0 WHERE id = %s', [id])
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('index'))


@app.route('/delete_complete', methods=['POST', 'GET'])
def delete_complete():
    cur = mysql.connection.cursor()

    cur.execute("DELETE FROM todo WHERE complete=1")

    # commit to db
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('index'))

@app.route('/delete_all', methods=['POST', 'GET'])
def delete_all():
    # create connection
    cur = mysql.connection.cursor()
    cur.execute('TRUNCATE TABLE todo')
    mysql.connection.cursor()
    
    cur.close()

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)