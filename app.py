from flask import Flask, render_template, request, redirect
import smtplib
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from werkzeug.utils import redirect



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'

# Initialize the database
db = SQLAlchemy(app)

# Create db model
class Videogames(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    

# Create a function to return a string when we add something

    def __repr__(self):
        return '<Name &r>' % self.id

db.create_all()
db.session.commit()

subscribers =[]

@app.route('/delete/<int:id>')
def delete(id):
    friend_to_delete = Videogames.query.get_or_404(id)

    try:
        db.session.delete(friend_to_delete)
        db.session.commit()
        return redirect('/videogamepage')
    except:
        return "There was a problem deleting that video"


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    friend_to_update = Videogames.query.get_or_404(id)
    if request.method == "POST":
        friend_to_update.name = request.form['name']
        try:
            db.session.commit()
            return redirect('/videogamepage')
        except:
            return "There was a problem updating your video"
    else:
        return render_template('update.html', friend_to_update=friend_to_update )


@app.route('/videogamepage', methods=['POST', 'GET'])
def videogamepage():
    title = "My Friend List"

    if request.method == "POST":
        friend_name = request.form['name']
        new_friend = Videogames(name=friend_name)

        # Push to Database
        try:
            db.session.add(new_friend)
            db.session.commit()
            return redirect('/videogamepage')
        except:
            return "There was an error adding your friend, please try again!"

    else:
        videogames = Videogames.query.order_by(Videogames.name)
        return render_template("videogamepage.html", title=title, videogames=videogames)

@app.route('/')
def index():
    title = "Angelos's Blog"
    return render_template("index.html", title=title)
    
@app.route('/about')
def about():
    title = "About Angelos!"
    names = ["Angelos", "Mary", "Wes", "Sally"]
    return render_template("about.html", names=names, title=title)

@app.route('/subscribe')
def subscribe():
    title = "Subscribe My Email Newsletter"
    return render_template("subscribe.html", title=title)

@app.route('/form', methods=["POST"])
def form():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email =  request.form.get("email")

    # message = "You have been subscribed to my email newsletter"
    # server = smtplib.SMTP("smpt.gmail.com", 587)
    # server.starttls()
    # server.login("aggoup05@gmail.com", "PASSWORD") #this is where the password goes, leave it black for now
    # server.sendmail("aggoup05@gmail.com", email, message)



    if not first_name or not last_name or not email:
        error_statement = "All Form Fields Required, Please Make Sure You Fill Out All The Boxes!"
        return render_template("subscribe.html", error_statement=error_statement, first_name=first_name, last_name=last_name, email=email)

    subscribers.append(f"{first_name} {last_name} | {email}")
    title = "Thank you!"
    return render_template("form.html", title=title, subscribers=subscribers)

    #test