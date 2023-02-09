from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI']= r'sqlite:///C:\Users\prakhar.rastogi1\PycharmProjects\KM_Flask\KM.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['SECRET_KEY']= 'mykey'

db = SQLAlchemy(app)

print(db.Model)

class KM(db.Model):
    __tablename__= 'KM'

    Id= db.Column(db.Integer(), primay_key = True)
    Geography = db.Column(db.String(47))
    Sector = db.Column(db.String(47))
    Subsector= db.Column(db.String(47))
    Segments= db.Column(db.String(47))
    Year = db.Column(db.String(47))


