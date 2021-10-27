from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import Login, SignUp


@app.route('/')


@app.route('/start')
def start():
    return render_template('start.html', title='Start')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUp()  # instantiate object
    if form.validate_on_submit():
        flash('Email: {} | User ID: {} | Password: {}' .format(form.email.data, form.username.data, form.password.data))
        # flash to display messages for prototype, driver
        return redirect(url_for('home'))  # navigation when complete
    return render_template('signup.html', title='Sign Up', form=form)  # pass form


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()  # instantiate object
    if form.validate_on_submit():
        flash('User ID: {} | Password: {}'.format(form.username.data, form.password.data))
        # flash to display messages for prototype, driver
        return redirect(url_for('home'))  # navigation when complete
    return render_template('login.html', title='Log In', form=form)  # pass form

@app.route('/logout')
def logout():
    return render_template('logout.html', title='Log Out')



@app.route('/home')
def home():
    return render_template('home.html', title='Home')
