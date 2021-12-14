from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db
from datetime import (date, datetime)
from werkzeug.security import (generate_password_hash, check_password_hash)
import crud
from jinja2 import StrictUndefined
import os 
mapbox = os.environ["mapbox_key"]
app = Flask(__name__)
app.secret_key = 'plantsarethebest'
app.jinja_env.undefined = StrictUndefined
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



# route to homepage
@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')

# display all plants which exist in the database
@app.route("/plants")
def all_plants():
    """View all plants."""

    plants = crud.get_plants()

    return render_template("all_plants.html", plants=plants)

# view plant by plant id 
@app.route("/plants/<plant_id>")
def show_plant(plant_id):
    """Show details on a particular plant."""

    plant = crud.get_plant_by_id(plant_id)
    growths = ["seed", "sprout", "plantlet", "adult plant"]
    conditions = ["healthy", "brown leaves", "black spots", "wilting", "dying"]
    lights = ["Indirect sunlight", "Full sun", "Full sun to part shade", "Part shade", "Part shade to full shade", "Part sun to part shade" ]
    soils = ["Moist", "Well-drained", "Rich, fast-draining", "Sandy, moist, well-drained", "Moist, well-drained", "Sandy, well-drained", "Rich, moist, well-drained", "Rich, moderately moist", "Rich, loamy", "Loamy, sandy", "Rich, well-drained", "Rich, moist", "Sandy", "Loamy, well-drained" ]
    waterneeds = ["Medium", "Low", "Low to medium", "High", "Medium to high"]
    return render_template("plant_details.html", plant=plant, growths=growths, conditions=conditions, lights=lights, soils=soils, waterneeds=waterneeds)

# allow users to enter their plants' data and save plant(s) to user_plants route
@app.route("/plants/<plant_id>/add", methods=["POST"])
def add_plant(plant_id):
    print(plant_id)
    growths = request.form.get("growths")
    lights = request.form.get("lights")
    soils = request.form.get("soils")
    waterneeds = request.form.get("waterneeds")

    email = session["user_email"]
    user= crud.get_user_by_email(email)
    plant = crud.get_plant_by_id(plant_id)
 
    user_plant = crud.create_user_plant(user, plant, plant_life_cycle=growths, date_plant_added=datetime.today(), current_light=lights, soil_status=soils, water_status=waterneeds)
    print(user_plant)
    return redirect("/user_plants")
   

# display all registered users in users route
@app.route("/users")
def all_users():
    """View all users."""

    users = crud.get_users()

    return render_template("all_users.html", users=users)


@app.route("/signup", methods=["GET"])
def show_signup_form():

    return render_template("signup.html")

# creating/registering user by email and password. Directing user to homepage if email or password is incorrect
@app.route("/signup", methods=["POST"])
def register_user():

    email = request.form.get("email")
    password = request.form.get("password")
    user = crud.get_user_by_email(email)

    if user:
        hashed_password = generate_password_hash(user.password, password, method='sha256')
        user = crud.get_user_by_email(email, hashed_password)
        flash("Cannot create an account with that email. Try again.")
    else:
        crud.create_user(email, password)
        flash("Account created! Please log in.")

    return redirect("/")

# displaying user by user id
@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""

    user = crud.get_user_by_id(user_id)

    return render_template("user_details.html", user=user)

# create user login & authenticating username and password
@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        check_password_hash(user.password, password)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
        return redirect("/")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")

        return redirect("/dashboard")

# create user log out, display only when user is logged in
@app.route("/logout")
def logout():
    """User must be logged in."""
    del session["user_email"]
  

    return redirect("/")


# display plant associated with specific user
@app.route("/user_plants")
def user_plants():
    """View all users' plants."""
    email = session["user_email"]
    user = crud.get_user_by_email(email)
    user_plants = crud.find_user_plant(user.user_id)
    print(user_plants)

    return render_template("user_plants.html", user_plants=user_plants)


@app.route("/user_plants/<users_plants_id>")
def user_plants_details(users_plants_id):
    """View all users' plants details."""
    # email = session["user_email"]
    # user = crud.get_user_by_email(email)
    user_plant_notes = crud.get_note_by_user_plant_id(users_plants_id)
    print(user_plant_notes)
    user_plants_details = crud.find_user_plant_details(users_plants_id)
    print(user_plants_details)

    return render_template("user_plants_details.html", user_plant=user_plants_details, user_plant_notes=user_plant_notes
)
@app.route("/user_plants/<users_plants_id>", methods=["POST"])
def user_plant_notes(users_plants_id):

    growths = request.form.get("growths")
    conditions = request.form.get("conditions")
    plant_note = request.form.get("plant_note")
    user_plant = crud.find_user_plant_details(users_plants_id)
    user_plant_notes = crud.create_plant_note(users_plants=user_plant, plant_note=plant_note, form_growth=growths, form_condition=conditions)
    # print(user_plant_notes)

    # return redirect(f"/user_plants/{users_plants_id}")
    return render_template("user_plants_details.html", user_plant=user_plant, user_plant_notes=None)
    #query user plant with plant_note_id, pass this to plant template and loop over it to show all notes in the system

# data for plant condition chart
@app.route("/conditiondata/<users_plants_id>")
def condititiondata(users_plants_id):
    plant_notes = crud.get_note_by_user_plant_id(users_plants_id)
    plant_condition_data = []
    for plant_note in plant_notes:
        date = plant_note.plant_note_date
        plant_condition = plant_note.form_condition
        plant_condition_data.append({'date': date.isoformat(),
                                'plant_condition': plant_condition})


    return jsonify({'data': plant_condition_data})

        
@app.route("/dashboard")
def dashboard():
    """User can view the profile dashboard"""

    return render_template("dashboard.html")

# route to make ajax request for mapbox
@app.route("/mapbox")
def mapboxkey():
    return mapbox


if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)