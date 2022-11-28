# Natty Parks App
By Michelle Antelo
___
Table Of Contents
- [Natty Parks App](#natty-parks-app)
  - [App Heroku Link](#app-heroku-link)
  - [Description](#description)
    - [Features](#features)
    - [Planned Bonus Features](#planned-bonus-features)
  - [Api](#api)
  - [Initializing Project](#initializing-project)
  - [Data Flow](#data-flow)
  - [Database Schema](#database-schema)
___
## App Heroku Link
https://natty-parks.herokuapp.com

___
## Description
This app will highlight facts and information of all the US National Parks. Through this app, users will be able to create an account allowing them to favorite and plan future trips to these locations! Once they've visited a location, they can insert their photos, caption their memories, and upload them for all of their friends and families to see! They will also be able to submit ratings and comments on visited locations for everyone else to see!
___
### Features
- Parks
  - Parks List
  - Parks Data Page
- Add Users 
  - User Database
  - User page 
    - Logout Button
    - Edit User Button
    - User Data Display
  - Edit user Page
  - Login/Signup
    - Login User form
    - Signup User Form
___
### Planned Bonus Features
- Search Bar
- Users Can
  - Plan trips to locations! 
  - Insert Photos
    - Caption memories 
  - Users can favorite Parks
  - Users Social Page 
    - Lists users liked Parks
  - Add friends and families
  - Submit ratings
  - Comments 
- Add a map View of all the parks
___
## Api
  [National Park Api](https://rapidapi.com/jonahtaylor/api/national-park-service/)
___

## Initializing Project
    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ createdb natty_parks   
    $ db.create.all()
    $ flask run
___
## Data Flow
Login Flow
UI --> Login --> Authenticate --> UI
Update User Flow
UI --> Database --> UI
___
## Database Schema
* User
  * UID
  * Username (Required)
  * Password (Required)
  * Email (Required)
  * Profile photo (Default)
  * Bio (Default)
  * Parks Id's
  * Friend Id's
___