from flask import Flask, render_template
import pymysql

def dbConnect(query):
    connect = pymysql.connect(
        host='freetrainer.cryiqqx3x1ub.us-west-2.rds.amazonaws.com',
        user='tom',
        password='changeme',
        db='Tom_Barr',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = connect.cursor()
    cursor.execute(query)
    output = cursor.fetchall()
    connect.close()
    print(output[0]['doctorId'])
    return output

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/Dogs")
def dogs():
    return render_template("dogs.html")


@app.route("/Doctors")
def doctors():
    doctor = dbConnect('SELECT doctorId FROM Tom_Barr.doctors where doctorName = "Jim";')
    return render_template("doctors.html",
        doctor=doctor
    )


@app.route("/Maladies")
def maladies():
    return render_template("maladies.html")


if __name__ == "__main__":
    app.run(debug=True)
