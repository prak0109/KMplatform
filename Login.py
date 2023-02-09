from flask import Flask, render_template,redirect, url_for, request
from flask_wtf import FlaskForm,Form
from wtforms import StringField, SubmitField,PasswordField
from wtforms.validators import InputRequired

app = Flask(__name__)
app.config['SECRET_KEY']= 'KM_Platform'
class LoginForm(Form):

	username = StringField('username', validators=[InputRequired()])
	password = PasswordField('password', validators=[InputRequired()])

@app.route('/', methods=['GET', 'POST'])
def index():
	form = LoginForm()
	if form.validate_on_submit():

		return 'Form Successfully Submitted!'
	return render_template('index.html', form=form)

if __name__ == '__main__':
	app.run(debug=True)
