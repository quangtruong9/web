import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime
import psycopg2
app = Flask(__name__)
#DATABASE_URL = os.environ["postgres://tncdzhysojhnjn:e07995eb170d7115f2b7c503afa00117cb3319b7980df6654f0583751aebd960@ec2-3-216-129-140.compute-1.amazonaws.com:5432/dcc0kbu8eseuk2"]
engine = create_engine("postgres://tncdzhysojhnjn:e07995eb170d7115f2b7c503afa00117cb3319b7980df6654f0583751aebd960@ec2-3-216-129-140.compute-1.amazonaws.com:5432/dcc0kbu8eseuk2")
db = scoped_session(sessionmaker(bind=engine))
email = "nguyentruog@gmail.com"
password = "123123123"
firstname = "truong"
lastname = "nguyen"
phone_number = 12312312
db.execute("INSERT INTO customers (email,password,firstname,lastname,phone_number) VALUES (:email,:password,:firstname,:lastname,:phone_number)",
            {"email":email,"password":password,"firstname":firstname,"lastname":lastname,"phone_number":phone_number})
db.commit()
