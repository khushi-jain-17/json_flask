import psycopg2
from flask import Flask, request, jsonify  

app = Flask(__name__)

def db_conn():
    conn = psycopg2.connect(database="flask_pg", host="localhost", user="postgres", password="1719", port="5432")
    return conn


@app.route('/courses',methods=['GET'])
def all_course():
    conn = db_conn()
    cur = conn.cursor()
    
    cur.execute(''' SELECT * FROM courses ORDER BY id''')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@app.route('/courses/<int:id>',methods=['GET'])
def index(id):
    conn = db_conn()
    cur = conn.cursor()

    cur.execute('''SELECT * FROM courses where id=%s''',(id,))
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@app.route('/create', methods=['POST'])
def create():
    conn = db_conn()
    cur = conn.cursor()
    data=request.json
    name=data.get("name")
    fee=data.get("fee")
    duration=data.get("duration")
    
    cur.execute('''INSERT INTO courses (name,fee,duration) VALUES(%s,%s,%s)''',(name,fee,duration))
    conn.commit()
    cur.close()
    conn.close()
 
    return jsonify(data)

@app.route('/update/<int:id>', methods=['PUT'])
def update(id):
    conn = db_conn()
    cur = conn.cursor()
    data=request.json
    name=data.get("name")
    fee=data.get("fee")
    duration=data.get("duration")
    
    cur.execute(
        '''UPDATE courses SET name=%s, fee=%s, duration=%s WHERE id=%s''', (name, fee, duration, id,)
    )
    conn.commit()
    cur.close()
    conn.close()
    return "course updated successfully"

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    conn = db_conn()
    cur = conn.cursor()
    cur.execute('''DELETE FROM courses where id=%s''',(id,))
    conn.commit()
    cur.close()
    conn.close()
    return "course deleted successfully"

    
    
    