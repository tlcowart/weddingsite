from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from datetime import datetime
import credentials

app = Flask(__name__)

db = SQLAlchemy(app)


#This allows switching between the different databases, currently using sqlite locally for dev. 
ENV = 'dev'
if ENV == 'dev':
    app.debug = True
    #Simply using an sqlite db locally to test out the RSVP portion
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wedding.db'
else:
    app.debug = False
    #Will add a postgres URI below once Heroku is setup
    password = credentials.login['password']
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:' + password + '@localhost/WeddingSite'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class WeddingSite(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50), nullable=False, default="Unknown", unique=True)
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

@app.route('/Events')
def Events():
    return render_template('Events.html')

@app.route('/rsvp', methods=['GET', 'POST'])
def posts():

    
        
    if request.method == 'POST':
        post_name = request.form['name']
        post_guests = request.form['guests']
        post_message = request.form['message']

        #This will be removed in the final vesrion, but if the count of the name used in the form is 0, add to the database.
        if db.session.query(WeddingSite).filter(WeddingSite.name == post_name).count()==0:
            new_post = WeddingSite(name=post_name, guests=post_guests, message=post_message)		
            db.session.add(new_post)
            db.session.commit()
            print('user added')
            return render_template('/submitted.html')

        #If the name is found in the database, update the fields of the database to indicate RSVP submission
        elif db.session.query(WeddingSite).filter(WeddingSite.name == post_name).count()==1:
            updated_post = WeddingSite.query.filter_by(name = request.form['name']).first()
            updated_post.guests = post_guests
            updated_post.message = post_message
            db.session.commit()
            print('user updated')
            return render_template('/submitted.html')
            
    else:
        return render_template('rsvp.html')


if __name__ == "__main__":
    app.run(debug=True)
