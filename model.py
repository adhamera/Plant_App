from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """User object"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return f'<User user_id={self.user_id} email={self.email}>'
    
class Plant(db.Model):
    """Plant object"""

    __tablename__ = "plants"

    plant_id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    common_name = db.Column(db.String, nullable=False)
    scientific_name = db.Column(db.String(50), nullable=False, unique=True)
    preferred_light = db.Column(db.String, nullable=False)
    watering_needs = db.Column(db.String, nullable=False)
    preferred_soil = db.Column(db.String, nullable=False)
    plant_img = db.Column(db.String)

    # user = db.relationship("User", backref="plants")

    def __repr__(self):
        return f'<Plant plant_id={self.plant_id}, common_name={self.common_name}>'

class User_Plant(db.Model):
    """Plant object belonging to User"""

    __tablename__ = "users_plants"

    users_plants_id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    plant_id = db.Column(db.Integer, db.ForeignKey("plants.plant_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    plant_life_cycle = db.Column(db.String, nullable=False)
    date_plant_added = db.Column(db.DateTime, nullable=False)
    current_light = db.Column(db.String, nullable=False)
    soil_status = db.Column(db.String, nullable=False)
    water_status = db.Column(db.String, nullable=False)

    plant = db.relationship("Plant", backref="users_plants")
    user = db.relationship("User", backref="users_plants")

    def __repr__(self):
        return f'<User_Plant users_plants_id={self.users_plants_id} plant_id={self.plant_id} user_id={self.user_id}>'

class Plant_Note(db.Model):
    """Plant note object belonging to plant"""

    __tablename__ = "plant_notes"

    plant_note_id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    users_plants_id = db.Column(db.Integer, db.ForeignKey("users_plants.users_plants_id"), nullable=False)
    plant_note = db.Column(db.Text, nullable=False)
    plant_note_date = db.Column(db.DateTime, nullable=False)
    form_growth = db.Column(db.Integer, nullable=False)
    form_condition = db.Column(db.Integer, nullable=False)


    users_plants = db.relationship("User_Plant", backref="plant_notes")

    def __repr__(self):
        return f'<Plant_Note plant_note_id{self.plant_note_id} users_plants_id{self.users_plants_id}>'

def connect_to_db(app):
    """Connect the database to Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///plants'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    from server import app
    connect_to_db(app) 