import os
from flask import Flask,request, jsonify
from flask_cors import CORS
import psycopg2
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
CORS(app)

# Ya mai na likha hai

DATABASE_URL = os.getenv("DATABASE_URL")


def get_db_connection():
    return psycopg2.connect(DATABASE_URL)



# ---------------------------------------------Students Table--------------------------
@app.route('/students',methods=['GET'])
def get_students():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""select id,name,roll_number,course,semester
    from students""")
    students = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify([
        {"id": s[0], "name": s[1], "roll_number": s[2],"course":s[3],"semester":s[4]}
        for s in students
    ])







@app.route('/students',methods=['POST'])
def create_students():
    data = request.json
    name = data.get('name')
    roll_number = data.get('roll_number')
    course = data.get('course')
    semester = data.get('semester')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("insert into students(name,roll_number,course,semester) values( %s,%s,%s,%s,%s) RETURNING id",(name,roll_number,course,semester))

    id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id":id, "name":name, "roll_number":roll_number,"course":course,"semester":semester})







@app.route('/students/<int:user_id>', methods=['PUT'])
def update_students(student_id):
    data = request.json
    name = data.get('name')
    roll_number= data.get('roll_number')
    course=data.get('course')
    semester=data.get('semester')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE student
        SET name = %s, roll_number = %s, course = %s, semester = %s
        WHERE id = %s
        RETURNING id, name,roll_number,course,semester
    """, (name, roll_number,course, semester ,student_id))

    updated_student= cur.fetchone() 
    conn.commit()

    cur.close()
    conn.close()

    if updated_student:
        return jsonify({
            "id": updated_student[0],
            "name": updated_student[1],
            "roll_number": updated_student[2],
            "course": updated_student[3],
            "semester": updated_student[4]
        })
    else:
        return jsonify({"error": "User not found"}), 404
    




@app.route('/students/<int:user_id>', methods=['DELETE'])
def delete_students(student_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM students WHERE id = %s RETURNING id;", (student_id))
    deleted = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    if deleted:
        return jsonify({"message": f"student {student_id} deleted successfully"})
    else:
        return jsonify({"error": "student not found"}), 404
    


#-------------------------------------------Users----------------------------------------
@app.route('/users',methods=['GET'])
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""select id,username,password,role
    from users""")
    users = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify([
        {"id":u[0], "username": u[1], "password": u[2],"role":u[3]}
        for u in users
    ])


@app.route('/users',methods=['POST'])
def create_users():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    role = data.get('role')
    

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("insert into users(username,password,role) values( %s,%s,%s) RETURNING id",(username,password,role))

    id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id":id, "username":username, "password":password,"role":role})






@app.route('/users/<int:user_id>', methods=['PUT'])
def update_users(user_id):
    data = request.json
    username = data.get('username')
    password= data.get('password')
    role=data.get('role')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE users
        SET username = %s, password = %s, role = %s
        WHERE id = %s
        RETURNING id, username,password,role
    """, (username, password,role,user_id))

    updated_users = cur.fetchone() 
    conn.commit()

    cur.close()
    conn.close()

    if updated_users:
        return jsonify({
            "id": updated_users[0],
            "username": updated_users[1],
            "password": updated_users[2],
            "role": updated_users[3]
        })
    else:
        return jsonify({"error": "User not found"}), 404
    





@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_users(user_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM users WHERE id = %s RETURNING id;", (user_id))
    deleted = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    if deleted:
        return jsonify({"message": f"users {user_id} deleted successfully"})
    else:
        return jsonify({"error": "users not found"}), 404


#----------------------------------------------------------------- subject------------
@app.route('/subjects',methods=['GET'])
def get_subjects():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""select id,subject_name
    from subjects""")
    subjects = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify([
        {"id":g[0], "subject_name": g[1]}
        for g in subjects
    ])









@app.route('/subjects',methods=['POST'])
def create_subjects():
    data = request.json
    subject_name = data.get('subject_name')
    

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("insert into subjects(subject_name) values(%s) RETURNING id",(subject_name))

    id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id":id,"subject_name":subject_name})

@app.route('/subjects/<int:user_id>', methods=['PUT'])
def update_subjects(user_id):
    data = request.json
    subject_name = data.get('subject_name')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE subjects
        SET subject_name = %s
        WHERE id = %s
        RETURNING id, subject_name
    """, (subject_name,user_id))

    updated_subjects = cur.fetchone() 
    conn.commit()

    cur.close()
    conn.close()

    if updated_subjects:
        return jsonify({
            "id": updated_subjects[0],
            "subject_name": updated_subjects[1]
        })
    else:
        return jsonify({"error": "User not found"}), 404
    
@app.route('/subjects/<int:user_id>', methods=['DELETE'])
def delete_subjects(subject_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM subjects  WHERE id = %s RETURNING id;", (subject_id))
    deleted = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()


    if deleted:
        return jsonify({"message": f"subject {subject_id}  deleted successfully"})
    else:
        return jsonify({"error": "users not found"}), 404

# -------------------------------------------------mark-------------------------------------

@app.route('/marks',methods=['GET'])
def get_marks():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""select id,student_id,subject_id,internal_marks,assignment_marks,final_exam_marks
    from marks""")
    marks = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify([
        {"id":m[0], "student_id": m[1], "subject_id": m[2], "internal_marks": m[3], "assignment_mark": m[4], "final_exam_marks": m[5]}
        for m in marks
    ])

@app.route('/marks',methods=['POST'])
def create_marks():
    data = request.json
    student_id = data.get('student_id')
    subject_id = data.get('subject_id')
    internal_marks = data.get('internal_marks')
    assignment_marks = data.get('assignment_marks')
    final_exam_marks = data.get('final_exam_marks')
    

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("insert into marks(student_id,subject_id,internal_marks,assignment_marks,final_exam_marks) values( %s,%s,%s,%s,%s) RETURNING id",(student_id,subject_id,internal_marks,assignment_marks,final_exam_marks))

    id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id":id, "student_id":student_id, "subject_id":subject_id,"internal_marks":internal_marks,"assignment_marks":assignment_marks,"final_exam_marks":final_exam_marks})

@app.route('/marks/<int:user_id>', methods=['PUT'])
def update_marks(marks_id):
    data = request.json
    student_id = data.get('student_id')
    subject_id= data.get('subject_id')
    internal_marks=data.get('internal_marks')
    assignment_marks=data.get('assignment_marks')
    final_exam_marks=data.get('final_exam_marks')


    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE marks
        SET  student_id= %s, subject_id = %s, internal_marks = %s, assignment_marks = %s,  final_exam_marks= %s
        WHERE id = %s
        RETURNING id, student_id,subject_id,internal_marks,assignment_marks,final_exam_marks
    """, (student_id, subject_id,internal_marks,assignment_marks,final_exam_marks,marks_id))

    updated_marks = cur.fetchone() 
    conn.commit()

    cur.close()
    conn.close()

    if updated_marks:
        return jsonify({
            "id": updated_marks[0],
            "student_id": updated_marks[1],
            "subject_id": updated_marks[2],
            "internal_marks": updated_marks[3],
            "assignment_marks": updated_marks[4],
            "final_exam_marks": updated_marks[5]
        })
    else:
        return jsonify({"error": "User not found"}), 404


@app.route('/marks/<int:user_id>', methods=['DELETE'])
def delete_marks(mark_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM marks  WHERE id = %s RETURNING id;", (mark_id))
    deleted = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    if deleted:
        return jsonify({"message": f"marks  {mark_id} deleted successfully"})
    else:
        return jsonify({"error": "users not found"}), 404

# -------------------------------------------------------------------attendance


@app.route('/attendance',methods=['GET'])
def get_attendance():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""select id,student_id,subject_id,total_classes,attended_classes
    from attendance""")
    attendance = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify([
        {"id":o[0], "student_id": o[1], "subject_id": o[2], "total_classes": o[3], "attended_classes": o[4]}
        for o in attendance
    ])

@app.route('/attendance',methods=['POST'])
def create_attendance():
    data = request.json
    student_id = data.get('student_id')
    subject_id = data.get('subject_id')
    total_classes = data.get('total_classes')
    attended_classes = data.get('attended_classes')
    

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("insert into attendance(student_id,subject_id,total_classes,attended_classes) values( %s,%s,%s,%s) RETURNING id",(student_id,subject_id,total_classes,attended_classes))

    id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id":id, "student_id":student_id, "subject_id":subject_id,"total_classes":total_classes,"attended_classes":attended_classes})


@app.route('/attendance/<int:user_id>', methods=['PUT'])
def update_attendance(attendance_id):
    data = request.json
    student_id = data.get('student_id')
    subject_id= data.get('subject_id')
    total_classes=data.get('total_classes')
    attended_classes=data.get('attended_classes')


    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE attendance
        SET  student_id= %s, subject_id = %s, total_classes = %s, attended_classes = %s
        WHERE id = %s
        RETURNING id, student_id,subject_id,total_classes,attended_classes
    """, (student_id, subject_id,total_classes,attended_classes ,attendance_id))

    updated_attendance = cur.fetchone() 
    conn.commit()

    cur.close()
    conn.close()

    if updated_attendance:
        return jsonify({
            "id": updated_attendance[0],
            "student_id": updated_attendance[1],
            "subject_id": updated_attendance[2],
            "total_classes": updated_attendance[3],
            "attended_classes": updated_attendance[4]
        })
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/attendance/<int:user_id>', methods=['DELETE'])
def delete_attendance(attendance_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM attendance WHERE id = %s RETURNING id;", (attendance_id))
    deleted = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    if deleted:
        return jsonify({"message": f"attendance  {attendance_id} deleted successfully"})
    else:
        return jsonify({"error": "users not found"}), 404
# ----------------------------------------------------------------------------------assignments
@app.route('/assignments',methods=['GET'])
def get_assignments():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""select id,student_id,title,submission_date,status,feedback
    from assignments""")
    assignments = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify([
        {"id":l[0], "student_id": l[1], "title": l[2], "submission_date": l[3], "status": l[4],"feedback":l[5]}
        for l in assignments
    ])

@app.route('/assignments',methods=['POST'])
def create_assignments():
    data = request.json
    student_id = data.get('student_id')
    title = data.get('title')
    submission_date = data.get('submission_date')
    status = data.get('status')
    feedback = data.get('feedback')
    

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("insert into assignments(student_id,title,submission_date,status,feedback) values( %s,%s,%s,%s,%s) RETURNING id",(student_id,title,submission_date,status,feedback))

    id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id":id, "student_id":student_id, "title":title,"submission_date":submission_date,"status":status,"feedback":feedback})

@app.route('/assignments/<int:user_id>', methods=['PUT'])
def update_assignments(assignment_id):
    data = request.json
    student_id = data.get('student_id')
    title= data.get('title')
    submission_date=data.get('submission_date')
    status=data.get('status')
    feedback=data.get('feedback')


    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE assignments
        SET  student_id= %s, title = %s, submission_date = %s, status = %s, feedback = %s
        WHERE id = %s
        RETURNING id, student_id,title,submission_date,status,feedback
    """, (student_id, title,submission_date,status,feedback,assignment_id))

    updated_assignments = cur.fetchone() 
    conn.commit()

    cur.close()
    conn.close()

    if updated_assignments:
        return jsonify({
            "id": updated_assignments[0],
            "student_id": updated_assignments[1],
            "title": updated_assignments[2],
            "submission_date": updated_assignments[3],
            "status": updated_assignments[4],
            "feedback": updated_assignments[5]
        })
    else:
        return jsonify({"error": "User not found"}), 404


@app.route('/assignment/<int:user_id>', methods=['DELETE'])
def delete_assignment(assignment_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM assignment WHERE id = %s RETURNING id;", (assignment_id))
    deleted = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    if deleted:
        return jsonify({"message": f"assignment{assignment_id} deleted successfully"})
    else:
        return jsonify({"error": "users not found"}), 404
# -------------------------------------------------------------------------------activity_log


@app.route('/activity_logs',methods=['GET'])
def get_activity_logs():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""select id,student_id,activity,created_at
    from activity_logs""")
    activity_logs = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify([
        {"id":a[0], "student_id": a[1],"c": a[1],"created_at": a[1]}
        for a in activity_logs
    ])

@app.route('/activity_logs',methods=['POST'])
def post_activity_logs():
    data = request.json
    student_id = data.get('student_id')
    activity = data.get('activity')
    created_at = data.get('created_at')

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("insert into activity_logs(student_id,activity,created_at) values( %s,%s,%s) RETURNING id",(student_id,activity,created_at))

    id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id":id, "student_id":student_id, "activity":activity,"created_at":created_at})


@app.route('/activity_logs/<int:user_id>', methods=['PUT'])
def update_activity_logs(activity_log_id):
    data = request.json
    student_id = data.get('student_id')
    activity= data.get('activity')
    created_at=data.get('created_at')


    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE activity_logs
        SET  student_id= %s,  activity= %s, created_at = %s
        WHERE id = %s
        RETURNING id, student_id,activity,created_at
    """, (student_id, activity,created_at,activity_log_id))

    updated_activity_logs = cur.fetchone() 
    conn.commit()

    cur.close()
    conn.close()

    if updated_activity_logs:
        return jsonify({
            "id": updated_activity_logs[0],
            "student_id": updated_activity_logs[1],
            "activity": updated_activity_logs[2],
            "created_at": updated_activity_logs[3]
        })
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/activity_logs/<int:user_id>', methods=['DELETE'])
def delete_activity_logs(activity_logs_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("DELETE FROM activity_logs  WHERE id = %s RETURNING id;", (activity_logs__id))
    deleted = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    if deleted:
        return jsonify({"message": f"activity_logs {activity_logs_id} deleted successfully"})
    else:
        return jsonify({"error": "users not found"}), 404

# ---------------------------------AUTH API---------------------------
# =========================================
# 1. USER REGISTRATION API
# =========================================
@app.route('/api/auth/register', methods=['POST'])
def register():
    if request.method == 'OPTIONS':
        return jsonify({"status": "OK"}), 200

    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid or missing JSON payload"}), 400
        
        username = data.get('username')
        password = data.get('password')
        role = data.get('role', 'student') # Defaults to student

        # Email check yahan se hata diya gaya hai
        if not username or not password:
            return jsonify({"error": "Missing required fields"}), 400

        # Password ko securely hash karein
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cur = conn.cursor()
        
        try:
            # SQL Query se bhi email column hata diya gaya hai
            cur.execute(
                """
                INSERT INTO users (username, password, role) 
                VALUES (%s, %s, %s) RETURNING id;
                """,
                (username, hashed_password, role)
            )
            user_id = cur.fetchone()[0]
            conn.commit()
            return jsonify({"message": "User registered successfully", "user_id": user_id}), 201
            
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            return jsonify({"error": "Username already exists"}), 409
        finally:
            cur.close()
            conn.close()

    except Exception as e:
        print("CRITICAL BACKEND ERROR:", str(e))
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

# =========================================
# 2. USER LOGIN API
# =========================================
@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Missing username or password"}), 400

        conn = get_db_connection()
        cur = conn.cursor()
        
        # Username ke zariye user fetch karein
        cur.execute("SELECT id, username, password, role FROM users WHERE username = %s;", (username,))
        user = cur.fetchone()
        
        cur.close()
        conn.close()

        # Password hash match check karein
        if user and check_password_hash(user[2], password):
            return jsonify({
                "message": "Login successful",
                "user": {
                    "id": user[0],
                    "username": user[1],
                    "role": user[3]
                }
            }), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401
            
    except Exception as e:
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=3000)