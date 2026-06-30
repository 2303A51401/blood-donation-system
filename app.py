from flask import Flask, render_template, request, redirect
from database import mysql
import os


app = Flask(__name__)


# Railway MySQL Connection

app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')
app.config['MYSQL_PORT'] = os.environ.get('MYSQL_PORT')


mysql.init_app(app)



@app.route('/')
def home():
    return render_template("index.html")



# REGISTER

@app.route('/register', methods=['GET','POST'])
def register():

    if request.method == "POST":

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']


        cur = mysql.connection.cursor()


        cur.execute(
            "INSERT INTO users(name,email,password,role) VALUES(%s,%s,%s,%s)",
            (name,email,password,role)
        )


        mysql.connection.commit()


        return redirect('/login')


    return render_template("register.html")





# LOGIN

@app.route('/login', methods=['GET','POST'])
def login():


    if request.method == "POST":


        email = request.form['email']
        password = request.form['password']


        cur = mysql.connection.cursor()


        cur.execute(
            "SELECT * FROM users WHERE email=%s AND password=%s",
            (email,password)
        )


        user = cur.fetchone()



        if user:

            return redirect('/dashboard')


        else:

            return "Invalid Email or Password"



    return render_template("login.html")






# DASHBOARD

@app.route('/dashboard')
def dashboard():

    return render_template("dashboard.html")





# ADMIN

@app.route('/admin')
def admin():

    return render_template("admin.html")







# DONATE BLOOD

@app.route('/donate', methods=['GET','POST'])
def donate():


    if request.method == "POST":


        name = request.form['name']
        blood_group = request.form['blood_group']
        age = request.form['age']
        phone = request.form['phone']



        cur = mysql.connection.cursor()



        cur.execute(
        "INSERT INTO donations(name,blood_group,age,phone) VALUES(%s,%s,%s,%s)",
        (name,blood_group,age,phone)
        )



        # update stock

        cur.execute(
        "UPDATE blood_stock SET units = units + 1 WHERE blood_group=%s",
        (blood_group,)
        )


        mysql.connection.commit()



        return "Donation Submitted Successfully"



    return render_template("donate.html")








# REQUEST BLOOD


@app.route('/request', methods=['GET','POST'])
def blood_request():


    if request.method == "POST":


        name = request.form['name']
        blood_group = request.form['blood_group']
        units = request.form['units']
        phone = request.form['phone']



        cur = mysql.connection.cursor()



        cur.execute(
        "INSERT INTO requests(name,blood_group,units,phone,status) VALUES(%s,%s,%s,%s,%s)",
        (name,blood_group,units,phone,"Pending")
        )



        mysql.connection.commit()



        return "Blood Request Submitted Successfully"



    return render_template("request.html")








# VIEW DONORS


@app.route('/donors')
def donors():


    cur = mysql.connection.cursor()


    cur.execute("SELECT * FROM donations")


    donors = cur.fetchall()



    return render_template("donors.html", donors=donors)









# VIEW REQUESTS


@app.route('/requests')
def view_requests():


    cur = mysql.connection.cursor()


    cur.execute("SELECT * FROM requests")


    requests = cur.fetchall()



    return render_template("requests.html", requests=requests)








# APPROVE REQUEST


@app.route('/approve/<int:id>')
def approve(id):


    cur = mysql.connection.cursor()



    cur.execute(
        "SELECT blood_group,units FROM requests WHERE id=%s",
        (id,)
    )


    data = cur.fetchone()



    if data:


        blood_group = data[0]
        units = data[1]



        cur.execute(
        "UPDATE blood_stock SET units = units - %s WHERE blood_group=%s",
        (units,blood_group)
        )



        cur.execute(
        "UPDATE requests SET status=%s WHERE id=%s",
        ("Approved",id)
        )



        mysql.connection.commit()



    return redirect('/requests')








# REJECT REQUEST


@app.route('/reject/<int:id>')
def reject(id):


    cur = mysql.connection.cursor()



    cur.execute(
        "UPDATE requests SET status=%s WHERE id=%s",
        ("Rejected",id)
    )


    mysql.connection.commit()



    return redirect('/requests')








# BLOOD STOCK


@app.route('/stock')
def stock():


    cur = mysql.connection.cursor()


    cur.execute("SELECT * FROM blood_stock")


    stock = cur.fetchall()



    return render_template("stock.html", stock=stock)








if __name__ == "__main__":

    app.run(debug=True)