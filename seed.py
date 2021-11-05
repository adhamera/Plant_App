
import os
import model
import server
from csv import DictReader, reader

os.system('dropdb plants')
os.system('createdb plants')

model.connect_to_db(server.app)#, echo=False)
model.db.create_all()

def create_plants():
    """Parse CSV."""

    with open('data/indoor_plants.csv', newline="") as f:
        reader = DictReader(f)
        for row in reader:
            plant = model.Plant(
                scientific_name=row["Scientific_Name"],
                common_name=row["Common_Name"],
                plant_img=row["Img_name"],
                preferred_light=row["Preferred_Light"],
                preferred_soil=row["Preferred_Soil"],
                watering_needs=row["Watering_Needs"]  
            )

            model.db.session.add(plant)

        model.db.session.commit()
create_plants()