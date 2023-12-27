from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['SECRET_KEY'] = "<Your secret key>"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['MAIL_PASSWORD'] = "<google-app-password>"
app.config['MAIL_USERNAME'] = "<Sender Email>"
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True

db = SQLAlchemy(app)

mail = Mail(app)


class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    occupation = db.Column(db.String(80))
    date = db.Column(db.Date)


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date = request.form['date']
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        email = request.form['email']
        occupation = request.form['occupation']

        form = Form(first_name=first_name,
                    last_name=last_name,
                    email=email,
                    date=date_obj,
                    occupation=occupation)

        db.session.add(form)
        db.session.commit()

        message_body = f"Thank for your submission, {first_name}.\n" \
                       f"Here is your data:\nFirst Name: {first_name}\nLast Name: {last_name}\nAvailable Start Date: {date}\n" \
                       f"Thank You!"

        message = Message(subject="New Form Submission",
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[email, ],
                          body=message_body)

        mail.send(message)

        flash(f"{first_name}, your form was submitted successfully!", "success")

    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5001)
