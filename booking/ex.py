import os
from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

engine = create_engine("postgres://postgres:123456789@localhost:5432")
db = scoped_session(sessionmaker(bind=engine))

email = "truong@gmail.com"
    
count = db.execute("SELECT email, password FROM customers").fetchall()


print(count)

for i in count:
    if (email==i[0]):
        print("yes")
        break
    else:
        continue
