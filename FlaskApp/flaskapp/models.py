from flask import Flask
from datetime import datetime
from flaskapp import db, app, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

#with app.app_context():
class Users(db.Model, UserMixin):

    __tablename__ = 'Users'

    # userID will be the primary key for this table 
    id = db.Column(db.Integer, unique=True, primary_key=True)
    # The max amount of characters username can be is 16 characters and usernames have the attribute unique. It also cant have a null value
    username = db.Column(db.String(16), unique=True, nullable=False) 
    # Cant have a null value, the hashed password will be less then 60 characters long
    password = db.Column(db.String(60), nullable=False)
    credit_balance = db.Column(db.Integer, default=500)
    #items = db.relationship('Items', backref='userID', lazy=True)
    #rentals = db.relationship('Rentals', backref='userID', lazy=True)
    #favourites = db.relationship('Favourites', backref='userID', lazy=True)

    def __repr__(self):
        return f"Users('{self.id}','{self.username}')"

class Items(db.Model):

    __tablename__ = 'Items'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    image_file = db.Column(db.String(16), nullable=False, default='default.png')
    brand = db.Column(db.String(20), default='n/a')
    colour = db.Column(db.String(20))
    typeOfClothing = db.Column(db.String(50))
    size = db.Column(db.String(5))
    minimumCredits = db.Column(db.Integer, nullable=False)
    #rentals = db.relationship('Rentals', backref='itemID', lazy=True)
    #favourites = db.relationship('Favourites',backref='itemID', lazy=True)

    def __repr__(self):
        return f"Items('{self.brand}', '{self.colour}', '{self.typeOfClothing}', '{self.size}', '{self.minimumCredits}', '{self.image_file}')"

class Rentals(db.Model):

    __tablename__ = 'Rentals'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    itemID = db.Column(db.Integer, db.ForeignKey('Items.id'), nullable=False)
    startDate = db.Column(db.Date, nullable=False)
    endDate = db.Column(db.Date, nullable=False)
    credit = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Rentals('{self.startDate}', '{self.endDate}', '{self.credit}')"


class Favourites(db.Model):

    __tablename__ = 'Favourites'

    id = db.Column(db.Integer, unique=True, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    itemID = db.Column(db.Integer, db.ForeignKey('Items.id'), nullable=False)

    def __repr__(self):
        return f"Favourites('{self.userID}', '{self.itemID}')"

    #db.create_all()

#with app.app_context():
    #db.create_all()
# from flaskapp import db, app
# app.app_context().push()
# db.create_all()
