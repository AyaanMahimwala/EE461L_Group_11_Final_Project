"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, render_template, request
from datetime import datetime

app = Flask(__name__)

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route('/', methods=['GET'])
def home():
    """Renders a home page."""
    return render_template(
            "index.html",
            flask_token = "home",
            title = "home",
            year = datetime.now().year,
        )

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Renders a contact page."""
    request_method = request.method
    if request_method == 'POST':
        request_user = request.form
    return render_template(
            "contact.html",
            flask_token = "contact",
            year = datetime.now().year,
        )

@app.route('/about', methods=['GET'])
def about():
    """Renders a about page."""
    return render_template(
            "about.html",
            flask_token = "about",
            year = datetime.now().year,
        )

@app.route('/tiers', methods=['GET'])
def tiers():
    """Renders a tiers page."""
    return render_template(
            "tiers.html",
            flask_token = "tiers",
            year = datetime.now().year,
        )

@app.route('/login', methods=['GET', 'POST'])
def contact():
    """Renders a login page. If form submited validates or returns error"""
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/data_set/<page>', methods=['GET'])
def get_data_sets(page):
    """Gets requested dataset whether it be the example dataset or a certain page 
    of the user's dataset. Return error message if page number is invalid"""
    page_size = 10
    if(page == 'example'):
        return db['Data_Sets'].find().skip(0).limit(page_size)
    try:
        page = int(page)
    except:
        return "Invalid page number."
    return selected_pages(page_size, page)

def selected_pages(page_size, page):
    """Returns all documents in a certain page of the user data sets"""
    skip_num = page_size * (page - 1) # find how many documents to skip
    cursor = db['Data_Sets'].find().skip(skip_num).limit(page_size) # narrow down which documents to include
    return [i for i in cursor] # return all included documents

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    # Need to change this to enviorment based so the mongo class can read it
    #app.config['MONGO_DB_URI'] = "mongodb://mongo_super:mongo_secret@0.0.0.0:27017"
    os.environ["MONGO_DB_URI"] = "mongodb://mongo_super:mongo_secret@0.0.0.0:27017"
    app.run(HOST, PORT)
