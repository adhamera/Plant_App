from model import db, User, Plant, Plant_Note, User_Plant, connect_to_db

def create_user(email, password):

    user = User(email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user

def get_users():
    """Return all users."""

    return User.query.all()

def get_user_by_email(email):

    return User.query.filter(User.email == email).first()

def create_plant(common_name, scientific_name, preferred_light, watering_needs, preferred_soil, plant_img):

    plant = Plant(common_name=common_name,scientific_name=scientific_name, preferred_light=preferred_light, watering_needs=watering_needs, preferred_soil=preferred_soil, plant_img=plant_img)

    db.session.add(plant)
    db.session.commit()

    return plant

def get_plants():
    """Return all plants."""

    return Plant.query.all()

def get_plant_by_id(plant_id):

    return Plant.query.get(plant_id)

def create_plant_note(users_plants, plant_note, form_growth, form_condition):

    plant_note = Plant_Note(users_plants=users_plants, plant_note=plant_note, plant_note_date="2021-11-10", form_growth=form_growth, form_condition=form_condition)

    db.session.add(plant_note)
    db.session.commit()

    return plant_note 

def get_plant_notes():  #unsure if I need these functions
    """Return all plant notes."""

    return Plant_Note.query.all() 

def get_plant_note_by_id(plant_note_id):

    return Plant_Note.query.get(plant_note_id)

def create_user_plant(user, plant, plant_life_cycle, date_plant_added, current_light, soil_status, water_status):

    user_plant = User_Plant(user=user, plant=plant, plant_life_cycle=plant_life_cycle, date_plant_added=date_plant_added, current_light=current_light, soil_status=soil_status, water_status=water_status)
    
    db.session.add(user_plant)
    db.session.commit()

    return user_plant

def find_user_plant(user_id):

    return User_Plant.query.filter(User_Plant.user_id == user_id).all()

def find_user_plant_details(users_plants_id):

    return User_Plant.query.filter(User_Plant.users_plants_id == users_plants_id).first()

def find_user_plant_note(plant_note_id):

    return Plant_Note.query.filter(Plant_Note.plant_note_id == plant_note_id).first()

if __name__ == '__main__':
    from server import app
    connect_to_db(app)