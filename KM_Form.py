from flask import Flask, render_template, session,url_for,redirect,flash
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,BooleanField,RadioField,SelectField,DateTimeField,TextField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY']= 'mykey'


class Infoform(FlaskForm):

    Geography = SelectField(u'Geography',choices=[('us', 'US'), ('uk', 'UK')])
    Sector = SelectField(u'Sector', choices=[('C', 'CPR')])
    Sub_Sector = SelectField(u'Sub-Sector',choices=[('re', 'Retail'), ('fnb', 'F&B'),('hpc','HPC')])
    Segments = SelectField(u'Segments',choices=[('ec', 'E-Commerce'), ('cs', 'Convenience Store'),('f','Food'),('b','Bags'),('dp','Disinfectants and Pet Hygiene')])
    Year = SelectField(u'Year',choices=[('y1', '2013-2023'), ('y2', '2018'),('y3','2013-2018'),('y4','2016-2022'),('y5','2015-2020')])

    feedback = TextAreaField()
    submit = SubmitField('Click Me')


@app.route('/',methods = ['GET', 'POST'])
def index():
    form =  Infoform()
    if form.validate_on_submit():
        flash('you just clicked the button')
        session['Geography']= form.Geography.data
        session['Sector']= form.Sector.data
        session['Sub_Sector']= form.Sub_Sector.data
        session['Segments']= form.Segments.data
        session['Year']= form.Year.data
        session['feedback'] = form.feedback.data
        session['submit'] = form.submit.data

        return redirect(url_for('thankyou'))

    return render_template('forms.html', form = form)

@app.route('/thankyou')
def thankyou():
    return render_template('datafilled.html')

if __name__=='__main__':
    app.run(debug=True)
