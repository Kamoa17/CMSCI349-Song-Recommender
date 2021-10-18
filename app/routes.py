from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import Login


@app.route('/')


@app.route('/start')
def start():
    return render_template('start.html', title='Start')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()  # instantiate object
    if form.validate_on_submit():
        flash('User ID: {} | Password: {}'.format(form.username.data, form.password.data))
        # flash to display messages for prototype, driver
        return redirect(url_for('home'))  # navigation when complete
    return render_template('login.html', title='Log In', form=form)  # pass form


@app.route('/home')
def home():
    return render_template('home.html', title='Home')
