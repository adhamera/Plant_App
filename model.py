from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User object"""
    # set table name as `users` for User objects
    __tablename__ = "users"

    # create table column for user_id as integer and set as the primary key
    user_id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    # create table column for email as a string
    email = db.Column(db.String(50), unique=True)
    # create table column for password as a string
    password = db.Column(db.String(30), nullable=False)

    # Method to identify each User instance by user_id
    def __repr__(self):
        return f'<User user_id={self.user_id}>'
    
class Plant(db.Model):
    """Plant object"""

    # set table name as `plants` for Plant objects
    __tablename__ = "plants"

    # create table column for plant_id as integer and set as the primary key
    plant_id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    # create table column for common_name as a string
    common_name = db.Column(db.String, nullable=False)
    # create table column for scientific_name as a string
    scientific_name = db.Column(db.String(50), nullable=False, unique=True)
    # create table column for preferred_light as a string
    preferred_light = db.Column(db.String, nullable=False)
    # create table column for watering_needs as a string
    watering_needs = db.Column(db.String, nullable=False)
    # create table column for preferred_soil as a string
    preferred_soil = db.Column(db.String, nullable=False)
    # create table column for plant_img as a string
    plant_img = db.Column(db.String)

    # user = db.relationship("User", backref="plants")

    # Method to identify each Plant instance by plant_id and common_name
    def __repr__(self):
        return f'<Plant plant_id={self.plant_id}, common_name={self.common_name}>'

class User_Plant(db.Model):
    """Plant object belonging to User"""

    # set table name as `users_plants` for Plant objects
    __tablename__ = "users_plants"

    # create table column for users_plants_id as integer and set as the primary key
    users_plants_id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    # create table column for plant_id as integer and set as foreign key
    plant_id = db.Column(db.Integer, db.ForeignKey("plants.plant_id"), nullable=False)
    # create table column for user_id as integer and set as foreign key
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    # create table column for plant_life_cycle as a string
    plant_life_cycle = db.Column(db.String, nullable=False)
    # create table column for date_plant_added as a string
    date_plant_added = db.Column(db.DateTime, nullable=False)
    # create table column for current_light as a string
    current_light = db.Column(db.String, nullable=False)
    # create table column for soil_status as a string
    soil_status = db.Column(db.String, nullable=False)
    # create table column for water_status as a string
    water_status = db.Column(db.String, nullable=False)

    # Create SQLAlchemy relationship between plants and users
    plant = db.relationship("Plant", backref="users_plants")
    user = db.relationship("User", backref="users_plants")

    # Method to identify each User_Plant instance by users_plants_id, plant_id and user_id
    def __repr__(self):
        return f'<User_Plant users_plants_id={self.users_plants_id} plant_id={self.plant_id} user_id={self.user_id}>'

class Plant_Note(db.Model):
    """Plant note object belonging to plant"""

    # set table name as `plant_notes` for Plant_Note objects
    __tablename__ = "plant_notes"

    # create table column for plant_note_id as integer and set as the primary key
    plant_note_id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    # create table column for users_plants_id as integer and set as foreign key
    users_plants_id = db.Column(db.Integer, db.ForeignKey("users_plants.users_plants_id"), nullable=False)
    # create table column for plant_note as a string
    plant_note = db.Column(db.Text, nullable=False)
    # create table column for plant_note_date as a string
    plant_note_date = db.Column(db.DateTime, nullable=False)
    # create table column for form_growth as a string
    form_growth = db.Column(db.String, nullable=False)
    # create table column for form_condition as a string
    form_condition = db.Column(db.String, nullable=False)

    # Create SQLAlchemy relationship between user_plants and plant_notes
    users_plants = db.relationship("User_Plant", backref="plant_notes")

    # Method to identify each Plant_Note instance by users_plants_id, plant_note_id 
    def __repr__(self):
        return f'<Plant_Note plant_note_id{self.plant_note_id} users_plants_id{self.users_plants_id}>'

def connect_to_db(app, db_uri="postgresql:///plants"):
    """Connect the database to Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

def example_data():
    """Create some sample data."""

    # In case this is run more than once, empty out existing data
    User.query.delete()
    Plant.query.delete()

    # Example data for users, plants, and user plants
    test_user = User(user_id=1, 
            email="user1@test.com",
            password="testing",)

    areca_palm = Plant(plant_id=1, 
                    common_name="Areca Palm", 
                    scientific_name="Dypsis lutescens", 
                    plant_img="areca_palm.png",
                    preferred_soil= "moist",
                    preferred_light="part sun",
                    watering_needs= "low" )
    
    new_plant  = Plant(plant_id=2, 
                    common_name="Aloe Vera", 
                    scientific_name="Aloe Vera", 
                    plant_img="aloe_vera.png",
                    preferred_soil= "moist",
                    preferred_light="full sun",
                    watering_needs= "medium" )

    jade = Plant(plant_id=3, 
                    common_name="Jade Plant", 
                    scientific_name="Crassula ovata", 
                    plant_img="jade_plant.png",
                    preferred_soil= "rich, well-drained",
                    preferred_light="full sun",
                    watering_needs= "medium" )
    
    zebra_plant = Plant(plant_id=4, 
                    common_name="Zebra Plant", 
                    scientific_name="Aphelandra squarrosa", 
                    plant_img="zebra_plant.png",
                    preferred_soil= "rich, well-drained",
                    preferred_light="part sun",
                    watering_needs= "high" )
    
    user_plant1 = User_Plant(users_plants_id = 1,
                    plant_id = 1, 
                    user_id = 1, 
                    plant_life_cycle = "plantlet",
                    date_plant_added = "2021-11-24",
                    current_light = "full sun",
                    soil_status = "moist",
                    water_status = "low")

    user_plant2 = User_Plant(users_plants_id = 2,
                    plant_id = 2, 
                    user_id = 1, 
                    plant_life_cycle = "adult plant",
                    date_plant_added = "2021-11-23",
                    current_light = "full sun",
                    soil_status = "sandy",
                    water_status = "medium")



    db.session.add_all([test_user, new_plant, user_plant1, user_plant2, zebra_plant, jade, areca_palm])
    db.session.commit()

if __name__ == "__main__":
    from server import app
    connect_to_db(app) 