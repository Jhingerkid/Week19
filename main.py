# To use:
# in the terminal type "virtual/Scripts/activate"
# then use py main.py
# PEP8 standards have been maliciously violated, don't tell Alfred

from flask import Flask, render_template, request
import pymysql

def dbGather(query):
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
    return output

def dbInsert(query):
    connect = pymysql.connect(
        host='freetrainer.cryiqqx3x1ub.us-west-2.rds.amazonaws.com',
        user='tom',
        password='changeme',
        db='Tom_Barr',
    )
    cursor = connect.cursor()
    cursor.execute(query)
    connect.commit()
    connect.close()

def cleanUp(string):
    string = string.strip("(")
    string = string.strip(")")
    string = string.strip(",")
    string = string.strip("'")
    return string


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/Dogs", methods=['POST', 'GET'])
def dogs():
    dogListQuery = "SELECT Tom_Barr.animals.*, Tom_Barr.maladies.maladyName, Tom_Barr.doctors.doctorName \
            FROM Tom_Barr.animals \
            LEFT JOIN Tom_Barr.maladies \
            ON Tom_Barr.maladies.maladyId = Tom_Barr.animals.maladyId \
            LEFT JOIN Tom_Barr.doctors \
            ON Tom_Barr.doctors.doctorId = Tom_Barr.animals.doctorId" 
    if request.method == "GET":
        dog = dbGather(dogListQuery)
        return render_template("dogs.html",
        dogInfo=dog
        )
    if request.method == "POST":
        if 'remdog' in request.form:
            remDogId = request.form['remdog']
            dbInsert('DELETE FROM Tom_Barr.animals WHERE animalId = ' + remDogId + ';')
            dog = dbGather(dogListQuery)
            return render_template("dogs.html",
            dogInfo=dog
            )
        elif 'updatedog0' in request.form:
            upDogMID = request.form['updatedog0']
            upDogDID = request.form['updatedog1']
            upDogAID = request.form['updatedog3']
            upDogName = request.form['updatedog2']
            dbInsert('UPDATE Tom_Barr.animals SET maladyId = ' + upDogMID + ', doctorId = ' + upDogDID +', animalName = "' + upDogName + '" WHERE animalId = ' + upDogAID)
            dog = dbGather(dogListQuery)
            return render_template("dogs.html",
            dogInfo=dog
            )
        elif 'searchdog' in request.form:
            userSearch = request.form['searchdog']
            searchQuery = dogListQuery + ' WHERE animalName LIKE "%' + userSearch + '%" OR maladyName LIKE "%' + userSearch + '%" OR doctorName LIKE "%' + userSearch + '%"'
            dog = dbGather(searchQuery)
            return render_template("dogs.html",
            dogInfo=dog
            )
        else: 
            newDog = request.form['adddog']
            newDogDoctor = request.form['adddogdoc']
            newDogMalady = request.form['adddogmal']
            if newDog == "" or newDogMalady == "" or newDogMalady == "":
                dog = dbGather(dogListQuery)
                warning = "Fields cannot be empty"
                return render_template("dogs.html",
                dogInfo=dog,
                warning=warning
                )
            dbInsert('INSERT INTO Tom_Barr.animals (animalName, doctorId, maladyId) VALUES ("' + newDog + '",' + newDogDoctor + ',' + newDogMalady + ');')
            dog = dbGather(dogListQuery)
            return render_template("dogs.html",
            dogInfo=dog,
            newDog=newDog
            )


@app.route("/Doctors", methods=['POST', 'GET'])
def doctors():    
    if request.method == "GET":
        doctor = dbGather('SELECT * FROM Tom_Barr.doctors;')
        return render_template("doctors.html",
        docInfo=doctor
        )
    if request.method == "POST":
        if 'remdoc' in request.form:
            remDocId = request.form['remdoc']
            dbInsert('DELETE FROM Tom_Barr.doctors WHERE doctorId = ' + remDocId + ';')
            doctor = dbGather('SELECT * FROM Tom_Barr.doctors;')
            return render_template("doctors.html",
            docInfo=doctor
            )
        elif 'updatedoctor0' in request.form:
            upDocName = request.form['updatedoctor0']
            upDocID = request.form['updatedoctor1']
            dbInsert('UPDATE Tom_Barr.doctors SET doctorName = "' + upDocName + '" WHERE doctorId = ' + upDocID)
            doctor = dbGather('SELECT * FROM Tom_Barr.doctors;')
            return render_template("doctors.html",
            docInfo=doctor
            )
        else:
            newDoctor = request.form['adddoc']
            dbInsert('INSERT INTO Tom_Barr.doctors (doctorName) VALUES ("' + newDoctor + '");')
            doctor = dbGather('SELECT * FROM Tom_Barr.doctors;')
            return render_template("doctors.html",
            docInfo=doctor,
            newDoctor=newDoctor
            )


@app.route("/Maladies", methods=['POST', 'GET'])
def maladies():    
    if request.method == "GET":
        malady = dbGather('SELECT * FROM Tom_Barr.maladies;')
        return render_template("maladies.html",
        malInfo=malady
        )
    if request.method == "POST":
        if 'remmal' in request.form:
            remMalId = request.form['remmal']
            dbInsert('DELETE FROM Tom_Barr.maladies WHERE maladyId = ' + remMalId + ';')
            malady = dbGather('SELECT * FROM Tom_Barr.maladies;')
            return render_template("maladies.html",
            malInfo=malady
            )
        else:
            newMalady = request.form['addmal']
            dbInsert('INSERT INTO Tom_Barr.maladies (maladyName) VALUES ("' + newMalady + '");')
            malady = dbGather('SELECT * FROM Tom_Barr.maladies;')
            return render_template("maladies.html",
            malInfo=malady,
            newMalady=newMalady
            )


@app.route("/Update", methods=['POST'])
def update():
    updateInfo = request.form['updog']
    updateInfoArr = updateInfo.split()
    updateInfoClean = list(map(cleanUp, updateInfoArr))
    return render_template("update.html",
    updateInfo=updateInfoClean
    )

@app.route("/UpdateDoc", methods=['POST'])
def updateDoc():
    updateInfo = request.form['updoctor']
    updateInfoArr = updateInfo.split()
    updateInfoClean = list(map(cleanUp, updateInfoArr))
    return render_template("updateDoctor.html",
    updateInfo=updateInfoClean
    )


if __name__ == "__main__":
    app.run(debug=True)
