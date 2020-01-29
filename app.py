from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime


app = Flask(__name__)

db = SQLAlchemy(app)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wedding.db'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class WeddingSite(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable=False, default="Unknown")
    guests = db.Column(db.Integer, nullable=False, default=0)
    message = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, name, guests, message):
        self.name = name
        self.guests = guests
        self.message = message
     


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/submitted')
def submitted():
    return render_template('submitted.html')

@app.route('/story')
def story():
    return render_template('story.html')

@app.route('/rsvp', methods=['GET', 'POST'])
def posts():

    if request.method == 'POST':
        post_name = request.form['name']
        post_guests = request.form['guests']
        post_message = request.form['message']
        new_post = WeddingSite(name=post_name, guests=post_guests, message=post_message)		
        db.session.add(new_post)
        db.session.commit()
        return redirect('/submitted')
    else:
        return render_template('rsvp.html')


##@app.route('/user/<name>')
##def user(name):
##    return render_template('user.html', name=name)  #name=name (left side goes with template username and right side goes with whats in app.route)


if __name__ == "__main__":
    app.run(debug=True)
