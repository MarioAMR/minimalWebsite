import functools
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from minimal.models import User
from . import db
from flask import (
    Blueprint, g, current_app, session, render_template, request, flash, redirect, url_for
)
from .layoutUtils import *
import os

auth = Blueprint('auth', __name__, url_prefix='/auth')


#IMPORTANT! Called for every request
@auth.before_app_request
def pre_operations(): 

    #ALL STATIC REQUESTS BYPASS!!!
    #if request.endpoint == 'static':
        #return

    #REDIRECT http -> https
    
    if 'DYNO' in os.environ:
        current_app.logger.critical("DYNO ENV !!!!")
        if request.url.startswith('http://'):
            url = request.url.replace('http://', 'https://', 1)
            code = 301
            return redirect(url, code=code)
            
    g.policyCode = 0 #SET DEFAULT INDEPENDENTLY TO WRAPPER

#WRAPPER FOR COOKIE SETTINGS 
def manage_cookie_policy(view):

    @functools.wraps(view)
    def wrapped_view(**kwargs):

        if request.method == 'POST':
            if 'btnAgreeAll' in request.form:
                session['cookie-policy'] = 3
            elif 'btnAgreeEssential' in request.form:
                session['cookie-policy'] = 0
            elif 'btnSaveCookieSettings' in request.form:
                session['cookie-policy'] = 0 #default
                if 'checkboxAnalysis' in request.form:
                    session['cookie-policy'] = 1
                if 'checkboxPersonalization' in request.form:
                    session['cookie-policy'] = 2
                if 'checkboxPersonalization' in request.form and 'checkboxAnalysis' in request.form:
                    session['cookie-policy'] = 3

        policyCode = session.get("cookie-policy")
        #possible values Null -> no info, 0 -> minimal, 1 -> Analysis, 
        #                                 2 -> Personalization, 3 -> All
        g.policyCode = 0
        if policyCode !=None:
            g.policyCode = policyCode

        g.showCookieAlert = False #DEFAULT
        if policyCode == None:
            g.showCookieAlert = True


        return view(**kwargs)

    return wrapped_view

@auth.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('bl_home.index'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
            
    mc = set_menu("login") #to highlight menu option
    return render_template("login.html",mc=mc, user=current_user, show_footer=False)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup',methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email)<5:
            flash("E-mail must be greater than 5 characters", category='error')
        elif len(first_name)<2:
            flash("First name must be greater than 1 characters", category='error')
        elif len(password1)<7:
            flash("Password must be greater than 6 characters", category='error')
        elif password1!=password2:
            flash("Passwords don\'t match", category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("Account created!", category='success')
            return redirect(url_for('bl_home.index'))
    mc = set_menu("signup") #to highlight menu option
    return render_template("sign_up.html",mc=mc,user=current_user,show_footer=False)