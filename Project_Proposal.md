** **

## MOC-UI Project Proposal

## 1. Vision and Goals Of The Project:


## 2. Users/Personas Of The Project


## 3. Scope and Features Of The Project:


## 4. Solution Concept

Global Architectural Structure Of the Project:
Blow is the system components and their descriptions.

* User UI: Visualization of networks with analysis presented to public
* Admin UI: Any admin work will be done in this UI.
* Auth: Authentication is needed for admins to signup/ login.
* DB (DB sandbox?): Data and analysis are stored here. 
* Business Logic: all backend jobs such as data analysis will be done here. 
* Communication: this logic is responsible for the communication between frontend and backend.
* GET/POST/PUT/DELETE request to the database via restAPI.

![image alt text](system_design.png)
**Figure 1: System components. The frontend consists of the UI and the admin UI, and the backend consists of API, business layer, and database layer.**

Figure 1 is a diagram of the overall software lifecycle for this web-based visualization project. It is expected to have two types of users: regular, unauthorized users and admins. The regular users only have GET request privilege, which fetches the data from database via restAPI and displays it on the client server, whereas admins have GET/POST/PUT/DELETE request privileges if necessary. Authentication system will be implemented, so only the admins with the credential can perform such tasks. All the requests that go to the API layer will be handled by the communication logic in the business layer. The communication logic is responsible for all the communications between restAPI and database, as well as sending commands to Analysis logic to compute any analysis. The communication layer, then, sends the analysis result to the database as well as fetching it to update the data on the restAPI. 




## 5. Acceptance criteria



## 6. Release Planning

