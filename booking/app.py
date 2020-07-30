import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
#trc khi chạy, tạo trong postgres database của khách hàng 
# CREATE TABLE customers (
# email VARCHAR PRIMARY KEY, 
# password VARCHAR NOT NULL, 
# firstname VARCHAR NOT NULL,
# lastname VARCHAR NOT NULL.
# phone_number INTERGER NOT NULL );

#mỗi máy dòng trong ngoặc sẽ khác nhau,thay 123456789 thành  password của postgres của mấy ô 

engine = create_engine("postgres://tncdzhysojhnjn:e07995eb170d7115f2b7c503afa00117cb3319b7980df6654f0583751aebd960@ec2-3-216-129-140.compute-1.amazonaws.com:5432/dcc0kbu8eseuk2")
db = scoped_session(sessionmaker(bind=engine))


@app.route("/",methods=['POST','GET'])
def index():
    #sau khi register xong, thì info của khách sẽ bỏ vào database
    if request.method =='POST':
        email = request.form.get("email")
        password = request.form.get("password")
        firstname = request.form.get("fname")
        lastname = request.form.get("lname")
        phone_number = request.form.get("pnumber")
        db.execute("INSERT INTO customers (email,password,firstname,lastname,phone_number) VALUES (:email,:password,:firstname,:lastname,:phone_number)",
            {"email":email,"password":password,"firstname":firstname,"lastname":lastname,"phone_number":phone_number})
        db.commit()
        
    return render_template("index.html")


@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/main", methods=['POST','GET'])
def main():
    #kiểm tra email với password có giống nhau ko, nếu giống thì mới vào đc trang main 
    if request.method =='POST':
        email = request.form.get("signin_email")
        password = request.form.get("signin_pass")
        emails = db.execute("SELECT email , password , firstname FROM customers WHERE email= :email AND password = :password",
            {"email":email,"password":password}).fetchone()
        if emails != None:
            return render_template("main.html",customer = emails)
        else:
            return render_template("index.html")

@app.route("/login",methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    emails = db.execute("SELECT email , password FROM customers WHERE email= :email AND password = :password",
            {"email":email,"password":password}).fetchone()
    if emails != None:
        return jsonify({"success":True})
    else:
        return jsonify({"success":False})


@app.route("/main/<email>")
def home(email):
    customer = db.execute("SELECT * FROM customers WHERE email=:email",{"email":email}).fetchone()
    return render_template("main.html",customer=customer)



@app.route("/myinfo/<email>", methods=['POST','GET'])
def myinfo(email):
    if request.method == 'POST':
        new_email = request.form.get("email")
        firstname = request.form.get("fname")
        lastname = request.form.get("lname")
        phone_number = request.form.get("pnumber")
        if firstname != '':
            db.execute("UPDATE customers SET firstname = :firstname WHERE email = :email",{"firstname":firstname,"email":email})
        if lastname != '':
            db.execute("UPDATE customers SET lastname = :lastname WHERE email = :email",{"lastname":lastname,"email":email})
        if phone_number != '':
            db.execute("UPDATE customers SET phone_number = :phone_number WHERE email = :email",{"phone_number":phone_number,"email":email})
        if new_email != '':
            db.execute("UPDATE customers SET email = :new_email WHERE email = :email",{"new_email":new_email,"email":email})
            email = new_email
        db.commit()
    customer = db.execute("SELECT * FROM customers WHERE email = :email",{"email":email}).fetchone()
    return render_template("myinfo.html",customer = customer)

@app.route("/update/<email>",methods=['POST'])
def update(email):
    customer = db.execute("SELECT * FROM customers WHERE email = :email",{"email":email}).fetchone()
    return render_template("update.html",customer = customer)

#hiển thị trang cá nhân của khách hàng   
@app.route("/user/<email>")
def user(email):
    if (email == "admin@admin"):
        booking = db.execute("SELECT * FROM bookings").fetchall()
    else:
        booking = db.execute("SELECT * FROM bookings WHERE email = :email",{"email":email}).fetchall()
    return render_template("user.html",email=email,booking=booking)

@app.route("/user/<email>/<book_id>",methods=['POST'])
def cancel(email,book_id):
    if request.method =='POST':
        db.execute("DELETE FROM bookings WHERE booking_id = :book_id",{"book_id":book_id})
        db.commit()
        if (email == "admin@admin"):
            booking = db.execute("SELECT * FROM bookings").fetchall()
        else:
            booking = db.execute("SELECT * FROM bookings WHERE email = :email",{"email":email}).fetchall()

        return render_template("user.html",email=email,booking=booking)
        



@app.route("/booking/<email>",methods=['POST'])
def booking(email):
    if request.method=='POST':
        check_in = request.form.get("inputCheckIn")
        check_out = request.form.get("inputCheckOut")
        adult = request.form.get("adult")  
        children = request.form.get("children")
        capacity = int(adult) + int(children)
        bed = request.form.get("bed")
        room_list = db.execute("SELECT * FROM rooms").fetchall()
        rooms = []
        for room in room_list:
            if room[1] > capacity:
                rooms.append(room)
        customer = db.execute("SELECT * FROM customers WHERE email = :email",{"email":email}).fetchone()
        return render_template("booking.html",customer = customer,check_in = check_in,check_out=check_out,rooms=rooms)

@app.route("/booking/<email>/<room_id>/<check_in>/<check_out>")
def bookings(email,room_id,check_in,check_out):
    db.execute("INSERT INTO bookings (room_id,email,check_in,check_out) VALUES (:room_id,:email,:check_in,:check_out)",
                {"room_id":room_id,"email":email,"check_in":check_in,"check_out":check_out})
    db.commit()
    return render_template("bookings.html",email=email,room_id=room_id)

@app.route("/manage")
def manage():
    now = datetime.datetime.now()
    today = now.date()
    late = db.execute("SELECT * FROM bookings WHERE check_in < :today",{"today":today}).fetchall()
    thisday = db.execute("SELECT * FROM bookings WHERE check_in = :today",{"today":today}).fetchall()
    coming = db.execute("SELECT * FROM bookings WHERE check_in > :today",{"today":today}).fetchall()
    current = db.execute("SELECT * FROM checkin_success").fetchall()
    return render_template("manage.html",lates = late,thisday= thisday,coming = coming, current = current)

@app.route("/manage/cancel/<book_id>")
def admin_cancel(book_id):
    db.execute("DELETE FROM bookings WHERE booking_id = :book_id",{"book_id":book_id})
    db.commit()
    now = datetime.datetime.now()
    today = now.date()
    late = db.execute("SELECT * FROM bookings WHERE check_in < :today",{"today":today}).fetchall()
    thisday = db.execute("SELECT * FROM bookings WHERE check_in = :today",{"today":today}).fetchall()
    coming = db.execute("SELECT * FROM bookings WHERE check_in > :today",{"today":today}).fetchall()
    current = db.execute("SELECT * FROM checkin_success").fetchall()
    return render_template("manage.html",lates = late,thisday= thisday,coming = coming, current = current)

@app.route("/manage/checkin/<book_id>",methods=['POST'])
def checkin(book_id):
    if request.method == 'POST':
        db.execute("INSERT INTO checkin_success SELECT * FROM bookings WHERE booking_id = :book_id",{"book_id":book_id})
        db.execute("DELETE FROM bookings WHERE booking_id = :book_id",{"book_id":book_id})
        db.commit()
        now = datetime.datetime.now()
        today = now.date()
        late = db.execute("SELECT * FROM bookings WHERE check_in < :today",{"today":today}).fetchall()
        thisday = db.execute("SELECT * FROM bookings WHERE check_in = :today",{"today":today}).fetchall()
        coming = db.execute("SELECT * FROM bookings WHERE check_in > :today",{"today":today}).fetchall()
        current = db.execute("SELECT * FROM checkin_success").fetchall()
        return render_template("manage.html",lates = late,thisday= thisday,coming = coming, current = current)


@app.route("/manage/checkout/<book_id>",methods=['POST'])
def checkout(book_id):
    if request.method == 'POST':
        now = datetime.datetime.now()
        check_out = now.date()
        check_in = db.execute("SELECT check_in FROM checkin_success WHERE booking_id = :book_id",{"book_id":book_id}).fetchone()
        cus_email = db.execute("SELECT email FROM checkin_success WHERE booking_id = :book_id",{"book_id":book_id}).fetchone()
        room_id = db.execute("SELECT room_id FROM checkin_success WHERE booking_id = :book_id",{"book_id":book_id}).fetchone()
        price = db.execute("SELECT price FROM rooms WHERE id = :room_id ",{"room_id":room_id[0]}).fetchone()
        date = check_out - check_in[0]
        if date.days == 0:
            total_date = 1
        else:
            total_date = date.days
        cost = int(price[0]) * total_date
        db.execute("INSERT INTO checkout_success (booking_id,room_id,email,check_in,check_out,price) VALUES (:booking_id,:room_id,:email,:check_in,:check_out,:price)",
            {"booking_id":book_id,"room_id":room_id[0],"email":cus_email[0],"check_in":check_in[0],"check_out":check_out,"price":cost})
        db.execute("DELETE FROM checkin_success WHERE booking_id = :book_id",{"book_id":book_id})
        db.commit()
        now = datetime.datetime.now()
        today = now.date()
        late = db.execute("SELECT * FROM bookings WHERE check_in < :today",{"today":today}).fetchall()
        thisday = db.execute("SELECT * FROM bookings WHERE check_in = :today",{"today":today}).fetchall()
        coming = db.execute("SELECT * FROM bookings WHERE check_in > :today",{"today":today}).fetchall()
        current = db.execute("SELECT * FROM checkin_success").fetchall()
        return render_template("manage.html",lates = late,thisday= thisday,coming = coming, current = current)
