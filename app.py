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
        entry_fname = request.form['fname']
        new_fname = Contact(fname=entry_fname)

        entry_lname = request.form['lname']
        new_lname = Contact(lname=entry_lname)

        entry_email = request.form['email']
        new_email = Contact(email=entry_email)

        entry_message = request.form['message']
        new_message = Contact(message=entry_message)

        try:
            db.session.add(new_fname)
            db.session.add(new_lname)
            db.session.add(new_email)
            db.session.add(new_message)
            db.session.commit()
            return redirect('/')
        except:
            return "Error creating contact"

    else:
        entries = Contact.query.order_by(Contact.date_added).all()
        return render_template('contact.html', entries=entries)


if __name__ == "__main__":
    app.run(debug=True)
