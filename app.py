from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///root.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class Contact(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    message = db.Column(db.String(400), nullable=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __contactList__(self):
        return '<Entry %r>' & self.id


@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.route("/home")
def default():
    return render_template('index.html')


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':

        contact = Contact(fname=request.form['fname'], lname=request.form['lname'],
                          email=request.form['email'], message=request.form['message'])

        try:

            db.session.add(contact)
            db.session.commit()
            return redirect('/')
        except:
            return "Error creating contact"

    else:
        return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=True)
