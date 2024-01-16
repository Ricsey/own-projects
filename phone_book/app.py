from flask import Flask, render_template, session, url_for
from flask_wtf import FlaskForm
import phonenumbers
from sqlalchemy import or_
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Email, Length, ValidationError
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return f'<Contact self.name>'

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('Email address', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    phone_number = StringField('Phone number', validators=[InputRequired()])
    submit = SubmitField('Register')

    def validate_phone_number(self, phone_number):
        try:
            p = phonenumbers.parse(phone_number.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationError('Invalid phone number')

class FindForm(FlaskForm):
    find_for = StringField('Search for')
    submit = SubmitField('Search')

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        contact = Contact(name=form.name.data,
                          email=form.email.data,
                          phone_number=form.phone_number.data)
        db.session.add(contact)
        db.session.commit()

        return render_template('register.html', form=form, registerpage_active=True)
    return render_template('register.html', form=form, registerpage_active=True)

@app.route('/find',  methods=['GET', 'POST'])
def find():
    form = FindForm()
    if form.validate_on_submit():
        found_contacts = Contact.query.filter(or_(Contact.name.like(f'%{form.find_for.data}%'), 
                                              ) )
        return render_template('find.html', form=form, findpage_active=True, founds = found_contacts)
    return render_template('find.html', form=form, findpage_active=True)

@app.route('/phonebook')
def phonebook():
    contacts = Contact.query.all()
    return render_template('phonebook.html', contacts=contacts, fullbook_active=True)

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()