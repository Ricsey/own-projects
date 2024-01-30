from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from wtforms import StringField, SubmitField
from check_discounts import run

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
Bootstrap(app)


class SearchForm(FlaskForm):
  search_for = StringField()
  add = SubmitField()
  search = SubmitField()

@app.route('/')
def index():
  form = SearchForm()
  if form.validate_on_submit():
    print()
  return render_template('index.html', form=form)

def main():
  app.run(debug=True)

if __name__ == '__main__':
  main()