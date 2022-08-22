# Unlock22-api
The application was used to monitor activity, attendence, and socres of the participantes at the summer camp of educational project [Unlock](https://vk.com/unlock_shift)

## Table of contents
* General Information
* [Functionality](#functionality)
* [Technologies](#technologies)

## Functionality
### Admin Panal
Through this panal, orginizers could create events and activities, distrebute points, and get real time look at data.

<img src="./images/admin_panal.png" alt="drawing" width="600"/>

### QR Scanner 
To create a conviniant way to keep count of active participantes, a QR scanner was added to the system. 
#### How does it work: 
1. Admin sends a link that contains id of an event `/qr/scan/{id:int}`
2. Orginizers scan the personal QR code of the participants
3. An object of [ScoreLog]() is created and saved in the database
4. The user gets notified about who he scanned
<img src="./images/qr_scanner.jpeg" alt="drawing" width="300"/>

### Bot Manager
Every participant has access to telegram bot [Cherlock](), which has following functions:
1. Asking questions
2. Sending polls 
3. Sending regestrations
4. Activating promocodes
The answers and results of the functions above is saved in the database, and available for review by admins later. 

Such functions are generated on the backend for further requests from the [chatbot]()   

## Technologies
