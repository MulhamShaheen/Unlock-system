# Unlock22-api
This system was used to monitor activity, attendence, and socres of the participantes at the summer camp of educational project [Unlock](https://vk.com/unlock_shift)

## Table of contents
* [Technologies and Skills](#technologies_and_skills)
* [Structure](#structure)
* [Functionality](#functionality)

## Technologies and Skills

The stack that was used:
* Django
* Django Restful Framework 
* Vue.js

During development the following skills were used and improved:
1. RESTful API design
2. Databases design
3. Working with high load
4. Implimenting third party JS libraries
5. Rapide maintenance and bug fixing

## Structure

The projects consets of two applications

### Score Manager
Which managed data of participants, teams, and their scores

<img src="./images/scoremanager_diagramm.jpg" alt="drawing" width="550"/>


### Bot Manager
Which managed the interaction between the backend and the chatbot 

<img src="./images/botmanager_diagramm.jpg" alt="drawing" width="700"/>


## Functionality
### Admin Panal
Through this panal, orginizers could create events and activities, distrebute points, and get real time look at data.

<img src="./images/admin_panal.png" alt="drawing" width="500"/>

### QR Scanner 
To create a conviniant way to keep count of active participantes, a QR scanner was added to the system. 

#### How does it work: 
1. Admin sends a link that contains id of an event `/qr/scan/{id:int}`
2. Orginizers scan the personal QR code of the participants
3. An object of [ScoreLog](/) is created and saved in the database
4. The user gets notified about who he scanned
<img src="./images/qr_scanner.jpeg" alt="drawing" width="300"/>

### Chat Bot Functions

Every participant has access to telegram bot [Cherlock](/), which has following functions:
1. Asking questions
2. Sending polls 
3. Sending regestrations
4. Activating promocodes
The answers and results of the functions above is saved in the database, and available for review by admins later. 

Such functions are generated on the backend for further requests from the [chatbot]()

### Score Monitoring

After every event or activity, points are added accordingly to participants and teams, these information are updated in real time, and can be viewed by admins 

<img src="./images/team_monitoring.png" alt="drawing" width="750"/>


