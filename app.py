from flask import Flask, render_template, request
# import sqlalchemy
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Set app to use a sqlalchemy database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sampledb.db'
db = SQLAlchemy(app)


# Set up a simple database
class Visitor(db.Model):
    username = db.Column(db.String(100), primary_key=True)
    numVisits = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f"{self.username} - {self.numVisits}"


# Create tables in Database
with app.app_context():
    db.create_all()


# Make a homepage
@app.route('/')
def homepage():
    return render_template('homepage.html')


@app.route('/hello/<name>')
def hello(name):
    listOfNames = [name, "Yoyo", "Yennifer"]
    return render_template('name.html', Sname=name, nameList=listOfNames)


@app.route('/form', methods=['GET', 'POST'])
def formDemo(name=None):
    if request.method == 'POST':
        name = request.form['name']
        # add Visitor to the database
        visitor = Visitor (username=name)
        db.session.add(visitor)

    db.session.commit()
    return render_template('form.html', name=name)

@app.route('/visitors')
def visitors():
    # Query the database to find all the visitors
    people = Visitor.query.all()
    return render_template('visitors.html', people=people)

# Add the option to run this file directly
if __name__ == "__main__":
    app.run(debug=True)
