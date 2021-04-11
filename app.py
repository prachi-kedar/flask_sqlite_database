from flask import Flask, render_template, request, jsonify
import sqlite3 as sql

app = Flask(__name__)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/enternew')
def new_student():
    return render_template('student.html')


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['add']

            with sql.connect("database.db") as con:
                cur = con.cursor()

                cur.execute("INSERT INTO students (id,occupancy)VALUES(?, ?)", (nm, addr))

                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "error in insert operation"

        finally:
            return render_template("result.html", msg=msg)
            con.close()


@app.route('/list')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from students")

    rows = cur.fetchall();
    return render_template("list.html", rows=rows)


@app.route('/api/all', methods=['GET'])
def api_all():
    conn = sql.connect('database.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    all_records = cur.execute("SELECT * FROM students").fetchall()

    return jsonify(all_records)


@app.route('/api/books', methods=['GET'])
def api_filter():
    conn = sql.connect('database.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    query_parameters = request.args

    id = query_parameters.get('id')

    if int(id) < 0:
        return "<h1>Page Not Found</h1>"

    records = cur.execute("SELECT * FROM students WHERE id = ?", (id,)).fetchall()

    return jsonify(records)


if __name__ == '__main__':
    app.run(debug=True)
