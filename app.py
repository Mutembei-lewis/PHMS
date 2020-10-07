import os
from werkzeug.security import generate_password_hash,check_password_hash
from flask import Flask,render_template,redirect,request,flash,url_for
from home import app,db,mail
from home.models import User, PersonalInfo,HealthHistory,Allergies,Immunizations,Medication
from flask_mail import Message
from home.form import RegistrationForm,LoginForm,RequestResetForm,ResetPasswordForm,UpdateProfile
from flask_login import login_user,logout_user,login_required,UserMixin,current_user
from werkzeug.utils import secure_filename
from datetime import datetime

# MAIN ROUTE 

@app.route("/", methods=["GET","POST"])
def index():
    return render_template("index.html")

# SIGN UP SECTION
@app.route("/signup", methods=["GET","POST"])
def signup():
    form = RegistrationForm()
    if  form.validate_on_submit():
        password = generate_password_hash(form.password.data)

        user = User(username=form.username.data,
                    email=form.email.data,
                    password_hash=password)
        db.session.add(user)
        db.session.commit()
        flash('Registration was successfully completed','success')
        return redirect(url_for('login'))
    else:
        return render_template('signup.html', form = form)

# LOGIN SECTION

@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
        next = request.args.get('next')

        if next == None or not next[0]== '/':
            next = url_for('index')
    return render_template('login.html', form=form)

#  LOGOUT CODE 
@app.route('/logout',methods=['GET'])
@login_required
def logout():
    logout_user()
    flash("You are logged out successfully")
    return redirect(url_for('index'))

#  RESET PASSWORD SECTION CODE

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',sender='lewismutembei001@gmail.com',recipients=[user.email])
    msg.body =f''' To reset your password,visit the following link:
{url_for('reset_token', token =token,_external =True)}

If you did not make this request then simply ignore this email and no changes will be made 
'''
    mail.send(msg)
# REQUEST RESET PASSWORD

@app.route('/reset_password',methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RequestResetForm()
    if  form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset  your password ','info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title ="Reset Password", form = form)
# SENDING RESET PASSWORD TOKEN
@app.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That token is invalid or expires','warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data)
        user.password_hash= password_hash
        db.session.commit()
        flash("Your password has been updated! You can now login")
        return redirect(url_for('login'))
    return render_template('reset_token.html', title = "Reset Password",form=form)

@app.route("/actions", methods=["GET","POST"])
@login_required
def actions():
    info = PersonalInfo()
    health = HealthHistory()
    allergic = Allergies()
    immune = Immunizations()
    med = Medication()
    if request.method =="POST":
        if request.form["submit"] == "Submit":
            info.username = current_user.username
            info.age= request.form.get('age')
            date_of_birth = request.form.get("date_of_birth")
            y, m, d = date_of_birth.split('-')
            dob = datetime(int(y), int(m), int(d))
            info.date_of_birth = dob
            info.social_security_number = request.form.get("social_security_number")
            info.emergency_contact = request.form.get("emergency_contact")
            info.blood_group = request.form.get("blood_group")
            info.rhesus_factor= request.form.get('rhesus_factor')
            info.height = request.form.get('height')
            info.eight = request.form.get("weight")
            db.session.add(info)
            db.session.commit()
            flash("Your personal information was added successfully")
            return redirect(url_for("actions"))
        if request.form["submit"] == "Send":

            health.username = current_user.username
            health.health_condition = request.form.get("health_condition")
            health.condition_description = request.form.get("history_description")
            db.session.add(health)
            db.session.commit()
            flash("your health history has been updated successfully")
            return redirect(url_for('actions'))
        if request.form["submit"] == "Add":

            allergic.username = current_user.username
            allergic.category = request.form.get("allergy_classification")
            allergic.allergens = request.form.get("allergy_name")
            db.session.add(allergic)
            db.session.commit()
            flash("Your info has been added ")
            return redirect(url_for("actions"))
        if request.form['submit'] =="Upload":

            immune.username = current_user.username
            immune.vaccine = request.form.get("vaccine")
            immune.date = request.form.get("vaccination_date")
            db.session.add(immune)
            db.session.commit()
            flash("Your info has been updated successfully!!")
            redirect(url_for('actions'))
            return redirect(url_for('actions'))
        if request.form['submit'] == "Prescription_day":
            med.username = current_user.username
            med.med_name = request.form.get("med_name")
            med.dosage_interval = request.form.get("dosage_interval")
            med.prescription_date = request.form.get("prescription_date")
            db.session.add(med)
            db.session.commit()
            flash(" Prescription reminder has been added")
            return redirect(url_for("actions"))

    return render_template("actions.html")
@app.route('/search',methods=["GET","POST"])
def search():
    return render_template('search.html')

@app.route("/userpage", methods=["GET","POST"])
def userpage():
    updateform= UpdateProfile()
    user = User.query.filter_by( email =current_user.email).first()
    if  request.method == "POST" or request.files:
        
        if updateform.validate_on_submit():
             file = request.files["avatar"]
             filename = secure_filename(file.filename)
             user.profile_picture = filename
             db.session.add(user)
             db.session.commit()
             file.save(os.path.join(app.config['IMAGE_UPLOAD_FOLDER'],filename))
             flash("Your profile picture has been updated successfully !!","alert")

        
        user.first_name = request.form.get("first_name")
        user.last_name = request.form.get("last_name")
        
        user.address=  request.form.get("address")
        user.contact = request.form.get("contact")
        db.session.add(user)
        db.session.commit()

        

             
        return redirect(url_for('index'))

    return render_template('userpage.html',updateform=updateform, user=user)

@app.route("/blog", methods=["GET",'POST'])
def blog():
    return render_template('blog.html')

@app.route("/myhealthbank", methods=["GET", "POST"])
def myhealthbank():
    personal_info = PersonalInfo.query.filter_by(username = current_user.username).first()
    health_history = HealthHistory.query.filter_by(username = current_user.username).first()
    allergies = Allergies.query.filter_by(username= current_user.username).first()
    # immunizations = Immunizations.query.filter_by(username=currect_user.username).first()
    return render_template("myhealthbank.html",personal_info=personal_info,health_history=health_history,allergies=allergies)


def searchTerms():
    return "None"

if __name__ == "__main":
    app.run(debug=True)