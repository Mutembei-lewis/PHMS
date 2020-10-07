from home import db,app,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User (UserMixin,db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(128),nullable=False)
    profile_picture = db.Column(db.String(40),default="default.png")
    first_name =db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    address = db.Column(db.String(20))
    contact = db.Column(db.Integer())

    
    
    

    def get_reset_token(self,expires_sec = 1800):
            s=  Serializer(app.config['SECRET_KEY'],expires_sec)
            return s.dumps({'user_id': self.id}).decode('utf-8')

    def check_password(self,password):
            return check_password_hash(self.password_hash,password )
   
    

    @staticmethod
    def verify_reset_token(token):
            s= Serializer(app.config['SECRET_KEY'])
            try:
                user_id = s.loads(token)['user_id']
            except:
                return None
            return User.query.get(user_id)
     ### REPRESENTATION METHOD CODE GOES HERE ###
     
    def __repr__(self):
            return f"User('{self.username}', '{self.email}')"

class PersonalInfo(db.Model):
    __tablename__ = "personal_Info"
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(64), nullable=False)
    age = db.Column(db.Integer())
    date_of_birth= db.Column(db.DateTime, default=datetime.now())
    social_security_number = db.Column(db.Integer)
    emergency_contact=db.Column(db.Integer())
    blood_group = db.Column(db.String(20))
    rhesus_factor = db.Column(db.String(20))
    height = db.Column(db.Integer())
    weight = db.Column(db.Integer())


class HealthHistory(db.Model):
    __tablename__ = "Health_History"
    id =db.Column(db.Integer, primary_key =True)
    username = db.Column(db.String(30),nullable=False)
    health_condition = db.Column(db.String(50))
    condition_description = db.Column(db.String(300))

class Allergies(db.Model):
    __tablename__ = 'Allergies'
    id = db.Column(db.Integer, primary_key= True)
    username =db.Column(db.String(30))
    category =db.Column(db.String(30))
    allergens =db.Column(db.String(200))

class Immunizations(db.Model):
    __tablename__ = "Vaccines"
    id =db.Column(db.Integer,primary_key= True)
    username =db.Column(db.String(30))
    vaccine = db.Column(db.String(30))
    date = db.Column(db.DateTime, default=datetime.now())
class Medication(db.Model):
    __tablename = "Medication"
    id= db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(40))
    med_name = db.Column(db.String(50))
    dosage_interval = db.Column(db.String())
    prescription_date = db.Column(db.DateTime(), default= datetime.utcnow())

