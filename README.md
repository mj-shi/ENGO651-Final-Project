# ENGO651-Final-Project
- Michael Shi (10174675): Developer, Designer, QA
- Omer Babiker (30146533): Presenter, Designer, QA

# Summary
Our final project is a web application called T-Tracker. The website allows users to view traffic incidents and traffic camera feeds across Calgary.
Users can register and login with a username and password (saved to database). After logging in, users can interact with the leaflet map. Traffic Cameras are blue markers, while traffic incidents are red markers. Clicking on each marker will provide detailed information (such as a camera feed image of a traffic camera) through a pop-up.
The map will automatically refresh every 10 minutes to check for new incident updates as well as camera images. The user can also manually refresh by clicking the Refresh Map button. Below the map, there is an update section where users can view and post updates. These updates are saved to the database. The updates are sorted by most recent appearing at the top, and the number of records is limited to 10 so the page doesn't become too long. Users can click "View All Updates" to view all of the updates posted by users sorted by most recent as well. The Post Update area requires the user to enter a location description as well as an incident description. Below the post update area is the Traffic Incident Analytics section. Stats of traffic incidents within the last 24 hours are displayed and are compared to historical data. The analytics currently shows the number of incidents, the number of incidents in each quadrant, and the total increase/decrease in incidents compared to historical data.

# How to set up the web application
- Similar to lab 1, create a heroku app, set up database, run flask and commands

# Commands to run
- pip/pip3 install requests
- set FLASK_APP=app.py
- set FLASK_DEBUG=1
- set DATABASE_URL=###
- python import.py

# Troubleshooting
- If you get a database url error then try changing postgres to postgresql in the DATABASE_URL
- If you continue to get errors then set the database url manually in app.py and import.py

# Datasets used (Traffic Incidents, Traffic Cameras)
- https://data.calgary.ca/Transportation-Transit/Traffic-Incidents/35ra-9556/data
- https://data.calgary.ca/Transportation-Transit/Traffic-Incidents-Archive-2017/himp-urp7/data
- https://data.calgary.ca/Transportation-Transit/Traffic-Cameras/k7p9-kppz/data


# SQL Files
- SQL files in the project starting with d3s### can be used to import the database format