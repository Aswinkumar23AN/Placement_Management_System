from flask import Flask, render_template, request, redirect, url_for
from dotenv import load_dotenv
from database import connect_database

load_dotenv()  # loads DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME from .env locally

app = Flask(__name__)


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- ADD STUDENT ----------------
@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        rollno = request.form["rollno"]
        name = request.form["name"]
        department = request.form["department"]
        cgpa = request.form["cgpa"]
        skills = request.form["skills"]
        placement_status = request.form["placement_status"]

        connection = connect_database()
        cursor = connection.cursor()

        query = """
        INSERT INTO students
        (rollno, name, department, cgpa, skills, placement_status)
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            rollno,
            name,
            department,
            cgpa,
            skills,
            placement_status,
        )

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("view_students"))

    return render_template("add_student.html")


# ---------------- VIEW STUDENTS ----------------
@app.route("/view")
def view_students():

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM students")

    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("view_students.html", students=students)


# ---------------- SEARCH STUDENT ----------------
@app.route("/search", methods=["GET", "POST"])
def search_student():

    student = None

    if request.method == "POST":

        rollno = request.form["rollno"]

        connection = connect_database()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT * FROM students WHERE rollno=%s",
            (rollno,)
        )

        student = cursor.fetchone()

        cursor.close()
        connection.close()

    return render_template(
        "search_student.html",
        student=student
    )


# ---------------- UPDATE STUDENT ----------------
@app.route("/update", methods=["GET", "POST"])
def update_student():

    if request.method == "POST":

        rollno = request.form["rollno"]
        name = request.form["name"]
        department = request.form["department"]
        cgpa = request.form["cgpa"]
        skills = request.form["skills"]
        placement_status = request.form["placement_status"]

        connection = connect_database()
        cursor = connection.cursor()

        query = """
        UPDATE students
        SET
            name=%s,
            department=%s,
            cgpa=%s,
            skills=%s,
            placement_status=%s
        WHERE rollno=%s
        """

        values = (
            name,
            department,
            cgpa,
            skills,
            placement_status,
            rollno,
        )

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("view_students"))

    return render_template("update_student.html")


# ---------------- DELETE STUDENT ----------------
@app.route("/delete", methods=["GET", "POST"])
def delete_student():

    if request.method == "POST":

        rollno = request.form["rollno"]

        connection = connect_database()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM students WHERE rollno=%s",
            (rollno,)
        )

        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for("view_students"))

    return render_template("delete_student.html")


# ---------------- ELIGIBLE STUDENTS ----------------
@app.route("/eligible")
def eligible_students():

    connection = connect_database()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM students WHERE cgpa >= 7.5"
    )

    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "eligible_student.html",
        students=students
    )


# ---------------- RUN APPLICATION ----------------
if __name__ == "__main__":
    app.run(debug=True)