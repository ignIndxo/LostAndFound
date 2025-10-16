import os
import secrets
from datetime import datetime
from dateutil.relativedelta import relativedelta
from flask import render_template, url_for, flash, redirect 
from flaskapp import app, db , bcrypt
from flaskapp.forms import SignupForm, LoginForm, UploadForm, ItemRental, SearchForm
from flaskapp.models import Users, Items, Rentals, Favourites
from flask_login import login_user, current_user, logout_user


# Routes are what are typed into browser to access the web application
@app.route("/")
# Home page can be accessed now from either route
@app.route("/home")
def homePage():
    items = Items.query.all()
    
    return render_template('home.html', items=items)
# This function returns what will be shown on the web application for the specific route "/" 
# Windows command set FLASK_APP=flaskapp.py sets environment variable :D
# Use python -m flask run to run

@app.context_processor
def layout():
    form = SearchForm()
    return dict(form=form)


@app.route("/search", methods=['POST'])
def search():
    form = SearchForm()
    items = Items.query
    colour_list=[]
    brand_list=[]
    typeOfClothing_list=[]
    if form.validate_on_submit():
        item_searched = form.searched.data
        item_words = item_searched.split()
        for i in range(0, len(item_words)):
            word = item_words[i]
            word = word.replace('-', '')
            search = word[0].upper()+word[1:].lower()
            items_colour = Items.query.filter_by(colour=search).all()
            for j in items_colour:
                colour_list.append(j.id)
            items_brand = Items.query.filter_by(brand=search).all()
            for k in items_brand:
                brand_list.append(k.id)
            items_typeOfClothing = Items.query.filter_by(typeOfClothing=search).all()
            for l in items_typeOfClothing:
                typeOfClothing_list.append(l.id)
        all_items = colour_list + brand_list + typeOfClothing_list
        newlist=[]
        duplist=[]
        triplist=[]
        for i in all_items:
            if i not in newlist:
                newlist.append(i)
            elif i not in duplist:
                duplist.append(i)
            else:
                triplist.append(i)
        if len(triplist)>0:
            all_items=triplist
        elif len(duplist)>0:
            all_items=duplist
        
        final_items=Items.query.filter(False)
        for i in all_items:
            specific_item = items.filter(Items.id.like(i))
            final_items = final_items.union(specific_item)
        
        #items = items_brand.union(items_colour, items_typeOfClothing)
        return render_template('search.html', form=form, items=items, final_items=final_items)
    return redirect(url_for('homePage'))


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('homePage'))
    form = SignupForm()
    #If form was validated on submitting it
    if form.validate_on_submit(): 
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #makes it a string
        user = Users(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created you are now able to login!', 'success') 
        # Flash message sends a one time alert
        return redirect(url_for('login'))
    return render_template('signup.html', title='SignUp', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('homePage'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('homePage'))
        else:
            flash('Login Unsuccesful, please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

def save_picture(form_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_fn = random_hex + f_ext
    image_path = os.path.join(app.root_path, 'static/image_pics', image_fn)
    form_image.save(image_path)

    return image_fn

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if current_user.is_authenticated:
        form = UploadForm()
        if form.validate_on_submit():
            corrected_brand=form.brand.data
            corrected_brand = corrected_brand[0].upper()+corrected_brand[1:].lower()
            if form.image.data:
                picture_file = save_picture(form.image.data)
                item = Items(userID=current_user.username, typeOfClothing=form.typeOfClothing.data, image_file=picture_file, brand=corrected_brand, colour=form.colour.data, size=form.size.data, minimumCredits=form.minimumCredits.data)
            db.session.add(item)
            db.session.commit()
            flash('Your item has now been posted!', 'success')
            return redirect(url_for('homePage'))
        return render_template('upload.html', title='Upload', form=form)
    else:
      return redirect(url_for('homePage'))

@app.route("/rent/<int:item_id>", methods=['GET', 'POST'])
def rent(item_id):
    itemFree = True
    recentRentals = []
    daysRented = 0
    additionalCredits = 0
    numOfFavs = 0
    item = Items.query.get_or_404(item_id)
    minCredits = item.minimumCredits
    poster = item.userID
    now = datetime.today().date()
    oldDate = now + relativedelta(months=-6) 
    if current_user.is_authenticated:
        form = ItemRental()
        if form.validate_on_submit():
            allRentals = Rentals.query.filter_by(itemID=item_id).all()
            for i in allRentals:
                if i.startDate>=oldDate:
                    recentRentals.append(i)
            for i in recentRentals:
                numOfDays = i.endDate - i.startDate
                daysRented = daysRented + numOfDays.days
            favourites = Favourites.query.filter_by(itemID=item_id)
            for i in favourites:
                numOfFavs = numOfFavs + 1
            if form.endDate.data <= form.startDate.data:
                flash('Please choose an end date that falls after the chosen start date', 'failure')
            else:
                rentals = Rentals.query.filter_by(itemID=item_id).all()
                for i in rentals:
                    if i.startDate <= form.startDate.data and i.endDate >= form.startDate.data:
                        flash('Item is unavailable on the chosen dates', 'failure')
                        itemFree = False
                        break
                    elif i.startDate <= form.endDate.data and i.endDate >= form.endDate.data:
                        flash('Item is unavailable on the chosen dates', 'failure')
                        itemFree = False
                        break
                    elif i.startDate >= form.startDate.data and i.endDate <= form.endDate.data:
                        flash('Item is unavailable on the chosen dates', 'failure')
                        itemFree = False
                        break
                if itemFree == True:
                    if daysRented >=150:
                        additionalCredits = additionalCredits + 30
                    elif daysRented >=100:
                        additionalCredits = additionalCredits + 20
                    elif daysRented >=50:
                        additionalCredits = additionalCredits + 10
                    elif daysRented >=25:
                        additionalCredits = additionalCredits + 5
                    favCredits = round(numOfFavs/10)
                    additionalCredits = additionalCredits + favCredits
                    days = form.endDate.data - form.startDate.data
                    credsPerDay = days.days * 5
                    additionalCredits = additionalCredits + credsPerDay
                    calcCredits = minCredits + additionalCredits
                    if current_user.credit_balance >= calcCredits:
                        new_balance = current_user.credit_balance - calcCredits
                        current_user.credit_balance = new_balance
                        user = Users.query.filter_by(username=poster).first()
                        postersBalance = user.credit_balance
                        postersBalance = postersBalance + calcCredits
                        user.credit_balance = postersBalance
                        rental = Rentals(userID=current_user.username, itemID=item_id, startDate=form.startDate.data, endDate=form.endDate.data, credit=calcCredits)
                        db.session.add(rental)
                        db.session.commit()
                        flash('Rental successful!', 'success')
                        return redirect(url_for('homePage'))
                    else:
                        flash('Not enough credits', 'failure')
        return render_template('rent.html', title='Rental', form=form, item=item)
    else:
      return redirect(url_for('homePage'))  

@app.route("/favourite/<int:item_id>", methods=['GET', 'POST'])
def favourite(item_id):
    if current_user.is_authenticated:
        duplicate = Favourites.query.filter_by(userID=current_user.id, itemID=item_id).first()
        if duplicate:
            return redirect(url_for('homePage'))
        else:
            favourite = Favourites(userID=current_user.id, itemID=item_id)
            db.session.add(favourite)
            db.session.commit()
            return redirect(url_for('homePage'))
    return redirect(url_for('homePage'))

@app.route("/unfavourite/<int:item_id>", methods=['GET', 'POST'])
def unfavourite(item_id):
    unfavourite = Favourites.query.filter_by(userID=current_user.id, itemID=item_id).delete()
    db.session.commit()
    return redirect(url_for('favourites'))

@app.route("/favourites", methods=['GET', 'POST'])
def favourites():
    if current_user.is_authenticated:
        favs = db.session.query(Favourites, Items).filter(Favourites.userID==current_user.id).join(Items, Items.id==Favourites.itemID).all()
        return render_template('favourites.html', favs=favs)
    return redirect(url_for('homePage'))

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('homePage'))

