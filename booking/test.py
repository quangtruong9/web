import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import datetime
import psycopg2
app = Flask(__name__)
#DATABASE_URL = os.environ["postgres://tncdzhysojhnjn:e07995eb170d7115f2b7c503afa00117cb3319b7980df6654f0583751aebd960@ec2-3-216-129-140.compute-1.amazonaws.com:5432/dcc0kbu8eseuk2"]
engine = create_engine("postgres://tncdzhysojhnjn:e07995eb170d7115f2b7c503afa00117cb3319b7980df6654f0583751aebd960@ec2-3-216-129-140.compute-1.amazonaws.com:5432/dcc0kbu8eseuk2")
db = scoped_session(sessionmaker(bind=engine))
email = "truong@gmail.com"
password = "123123123"
firstname = "truong"
lastname = "nguyen"
phone_number = 12312312
#book_id = 
now = datetime.datetime.now()
today = now.date()
late = db.execute("SELECT booking_id FROM bookings WHERE check_in < :today",{"today":today}).fetchall()
coming = db.execute("SELECT booking_id FROM bookings WHERE check_in >= :today",{"today":today}).fetchall()
print(late)
print(coming)