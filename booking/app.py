import os
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime
app = Flask(__name__)
#trc khi chạy, tạo trong postgres database của khách hàng 
# CREATE TABLE customers (
# email VARCHAR PRIMARY KEY, 
# password VARCHAR NOT NULL, 
# firstname VARCHAR NOT NULL,
# lastname VARCHAR NOT NULL.
# phone_number INTERGER NOT NULL );

#mỗi máy dòng trong ngoặc sẽ khác nhau,thay 123456789 thành  password của postgres của mấy ô 
engine = create_engine("postgres://postgres:123456789@localhost:5432") 
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
        emails = db.execute("SELECT email , password , firstname FROM customers").fetchall()
        for i in emails:
            if email == i[0]:
                if i[1] ==password:
                    return render_template("main.html",customer = i)
        return render_template("error.html")
    
@app.route("/user/<email>")
#hiển thị trang cá nhân của khách hàng
def user(email):
    booking = db.execute("SELECT * FROM bookings WHERE email = :email",{"email":email}).fetchone()
    return render_template("user.html",booking=booking)

@app.route("/user/<email>",methods=['POST'])
def cancel(email):
    if request.method =='POST':
        db.execute("DELETE FROM bookings WHERE email = :email",{"email":email})
        db.commit()  
        return redirect(url_for('user',email=email))
    

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

