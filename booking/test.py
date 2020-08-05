import os
import datetime
from passlib.hash import sha256_crypt
from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
engine = create_engine("postgres://tncdzhysojhnjn:e07995eb170d7115f2b7c503afa00117cb3319b7980df6654f0583751aebd960@ec2-3-216-129-140.compute-1.amazonaws.com:5432/dcc0kbu8eseuk2")
db = scoped_session(sessionmaker(bind=engine))

email = 'quangkhoi@gmail.com'
password = '123456'
#password = sha256_crypt.encrypt(password)
emails = db.execute("SELECT email , password FROM customers WHERE email= :email ",{"email":email}).fetchone()

print(sha256_crypt.encrypt(password))
#print(sha256_crypt.verify(password,emails.password))