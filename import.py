import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# engine = create_engine(os.getenv("DATABASE_URL"))

# Manually set up DATABASE_URL
engine = create_engine("DATABASE_URL")

db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("Traffic_Incidents_Archive_2017.csv")
    reader = csv.reader(f)
    
    for incident_info, description, start_dt, modified_dt, quadrant, longitude, latitude in reader:
        db.execute("INSERT INTO accidents2017 (incident_info, description, start_dt, modified_dt, quadrant, longitude, latitude) VALUES (:incident_info, :description, :start_dt, :modified_dt, :quadrant, :longitude, :latitude)",
        {
            "incident_info": incident_info, "description": description, "start_dt": start_dt, "modified_dt": modified_dt, "quadrant": quadrant, "longitude": longitude, "latitude": latitude 
        })
        print(f"Added accident record: {incident_info}, {description}, {start_dt}, {modified_dt}, {quadrant}, {longitude}, {latitude}")
    db.commit()

if __name__ == "__main__":
    main()