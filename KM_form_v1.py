from flask import Flask, render_template, session,url_for,redirect,flash,jsonify,request
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,BooleanField,RadioField,SelectField,DateTimeField,TextField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI']= r'sqlite:///C:\Users\prakhar.rastogi1\PycharmProjects\KM_Flask\KM.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
app.config['SECRET_KEY']= 'mykey'

db = SQLAlchemy(app)

class KM(db.Model):
    __tablename__= 'KM'
    Id= db.Column(db.Integer(), primary_key = True)
    Geography = db.Column(db.String(47))
    Sector = db.Column(db.String(47))
    Subsector= db.Column(db.String(47))
    Segments= db.Column(db.String(47))
    Year = db.Column(db.String(47))

class Infoform(FlaskForm):
    Geography = SelectField(u'Geography',choices=[('US', 'US'), ('UK', 'UK'),('GSA','GSA')])
    Sector = SelectField(u'Sector', choices=[('CPR','CPR')])
    Subsector = SelectField(u'Subsector',choices=[])
    Segments = SelectField(u'Segments',choices=[])
    Year = SelectField(u'Year',choices=[])

    feedback = TextAreaField()
    submit = SubmitField('Submit')

@app.route('/')
def index1():
    form =  Infoform()
    form.Subsector.choices = [(Subsector.Id,Subsector.Subsector) for Subsector in KM.query.filter_by(Geography='US').all()]
    #form.Segments.choices = [(seg.Id, seg.Segments) for seg in KM.query.filter_by(Subsector='HPC').all()]
    #form.Subsector.choices = [(Subsector.Id, Subsector.Subsector) for Subsector in
                             # KM.query.filter_by(Geography='US').distinct()]

    if request.method == 'POST':
        #Id= KM.query.filter_by(id=form.)
        Geography = KM.query.filter_by(Id=form.Geography.data).first()
        Subsector = KM.query.filter_by(Id=form.Subsector.data).first()
        Segments = KM.query.filter_by(Id=form.Segments.data).first()
        Year = KM.query.filter_by(Id=form.Year.data).first()
        return '<h1>Subsector : {}, Segments: {}, Year: {}</h1>'.format(form.Subsector.data, form.Segments.data, form.Year.data)

    return render_template('index1.html', form = form)

@app.route('/Subsector/<Geography>')
def subsector(Geography):
    #sub_sector = Geography.query.filter_by(Geography=Geography).all()
    sub_sectors = KM.query.filter_by(Geography=Geography).all()
    subsectorArray = []

    for i in sub_sectors:
        subsectObj = {}
        subsectObj['Id'] = i.Id
        subsectObj['Subsector'] = i.Subsector
        subsectorArray.append(subsectObj)

    return jsonify({'sub_sectors':subsectorArray})

if __name__=='__main__':
    app.run(debug=True)
