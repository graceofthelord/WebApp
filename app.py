from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from config import init_db

app = Flask(__name__)
init_db(app)
mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        department = request.form['department']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students (name, age, gender, department) VALUES (%s, %s, %s, %s)",
                    (name, age, gender, department))
        mysql.connection.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students WHERE id=%s", (id,))
    student = cur.fetchone()
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        department = request.form['department']
        cur.execute("UPDATE students SET name=%s, age=%s, gender=%s, department=%s WHERE id=%s",
                    (name, age, gender, department, id))
        mysql.connection.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', student=student)

@app.route('/delete/<int:id>')
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
