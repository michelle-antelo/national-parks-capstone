# Natty Parks App
By Michelle Antelo
___
Table Of Contents
- [Natty Parks App](#natty-parks-app)
  - [Description](#description)
    - [MVP Features](#mvp-features)
    - [Planned Features](#planned-features)
  - [Api](#api)
  - [Initializing Project](#initializing-project)
  - [User Story](#user-story)
  - [Data Flow](#data-flow)
  - [Database Schema](#database-schema)
___
## Description
This app will highlight facts and information of all the US National Parks. Through this app, users will be able to create an account allowing them to favorite and plan future trips to these locations! Once they've visited a location, they can insert their photos, caption their memories, and upload them for all of their friends and families to see! They will also be able to submit ratings and comments on visited locations for everyone else to see!
___
### MVP Features
- Parks
  - Parks List
  - Parks Data Page
  - Users can favorite Parks
- Add Users
  - User Database
  - User page
    - Logout Button
    - Edit User Button
    - User Data Display
  - Edit user Page
  - Users Social Page
    - Lists users liked Parks
  - Login/Signup
    - Login User form
    - Signup User Form
___
### Planned Features
- Search Bar
- Users Can
  - Plan trips to locations! 
  - Insert Photos
    - Caption memories 
  - Add friends and families
  - Submit ratings
  - Comments 
- Add a map View of all the parks
- Add photos on each park page
- Chat feature with friends
- Send parks to friends
___
## Api
  [National Park Api](https://rapidapi.com/jonahtaylor/api/national-park-service/)
___

## Initializing Project
    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    $ createdb natty_parks   
    $ flask run
___
## User Story
As a Hiker
<br> 
When I search for parks that have hikes in them
<br>
Then the app suggests some parks with hikes
<br><br>
As a Chatty user
<br> 
When I save a location to the app
<br>
Then the app saves it for me in my profile
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