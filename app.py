from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Creating Model of database
class User(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(80), nullable = False)
    desc = db.Column(db.String(1000), nullable = False)
    time_created = db.Column(db.DateTime , default = datetime.now)

    def __repr__(self):
        return f'{self.sno} - {self.title}'

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        msg = User(title =request.form['title'] , desc = request.form['desc'])
        db.session.add(msg)
        db.session.commit()
    allmsgs = User.query.all()
    return render_template("home.html", allmsgs=allmsgs)
@app.route('/delete/<int:sno>')
def delete(sno):
    msg = User.query.filter_by(sno=sno).first()
    db.session.delete(msg)
    db.session.commit()
    return redirect(url_for("home"))
if __name__ == "__main__":
    app.run(debug=True)
