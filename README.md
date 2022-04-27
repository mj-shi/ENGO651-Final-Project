# ENGO651-Final-Project
- Michael Shi (10174675): Developer, Designer, QA
- Omer Babiker (30146533): Presenter, Designer, QA

# Summary
Our final project is a web application called T-Tracker. The website allows users to view traffic incidents and traffic camera feeds across Calgary.
Users can register and login with a username and password (saved to database). After logging in, users can interact with the leaflet map. Traffic Cameras are blue markers, while traffic incidents are red markers. Clicking on each marker will provide detailed information (such as a camera feed image of a traffic camera) through a pop-up.
The map will automatically refresh every 10 minutes to check for new incident updates as well as camera images. The user can also manually refresh by clicking the Refresh Map button. Below the map, there is an update section where users can view and post updates. These updates are saved to the database. The updates are sorted by most recent appearing at the top, and the number of records is limited to 10 so the page doesn't become too long. Users can click "View All Updates" to view all of the updates posted by users sorted by most recent as well. The Post Update area requires the user to enter a location description as well as an incident description. Below the post update area is the Traffic Incident Analytics section. Stats of traffic incidents within the last 24 hours are displayed and are compared to historical data. The analytics currently shows the number of incidents, the number of incidents in each quadrant, and the total increase/decrease in incidents compared to historical data.

# Restful API Backend
- Login Page: Post request to authenticate user and check credentials in database / Get request to render template
- Register Page: Post request to add new user record to database / Get request to render template
- Home Page: Post request to add update to update list / Get request to render template and get list of updates from database
- Updates Page: Get request to render template

# Example Use Cases
- User wants to check for recent incidents as well as updates, they can use our map as our references and check the updates list for any new user updates.
- User sees incident and wishes to post their own update of the situation. They can post a user update with the location and incident description in the update section.
- User wants to view the roads and traffic status before leaving his house. He can view the traffic cameras on the path of his drive.
- User can compare today's incident data and historical data by looking at the analytics section.

# Program-related Files
- mapScripts.js - contains logic for home page including map creation/population and analytics
- home.html - home page template
- login.html - login page template
- register.html - register page template
- updates.html - updates page template
- app.py - app file, contains GET/POST request logic for each page
- import.py - file used to import historical data

# How to set up the web application
- Create a heroku app, set up database, run flask and commands

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