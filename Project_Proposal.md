# Interactive Web Visualization Project Proposal
## Members:
* Ben Leone (bleone90@bu.edu)
* Ryuichi Ohhata (ryu74@bu.edu)
* Lukas Rosario (lukasr@bu.edu)
* Jinyu Tian (jinyutn@bu.edu)
* Angela Vellante (akv@bu.edu)
** **

## 1. Vision and Goals Of The Project:
This project focuses on the development of an interactive, web-based visualization around the scientific collaboration network associated with the Hariri Institute faculty affiliates, leveraging data from a bibliographic database.
*	Provide an intuitive user experience, especially for people outside of BU, that allows for easy networking and a visually pleasing network of connected collaborations
*	Provide researchers with a tool to find similar collaborators based on their profiles
*	May serve as a base prototype for other departments

## 2. Users/Personas Of The Project
Admins at Hariri will go through an authentication process before being able to access the admin UI. Admins will be able to make additions and deletions if necessary. Regular users will only have the ability to access the information.
* Target:
   * Faculty affiliates of the Hariri Institute for Computing
   * Potential collaborators and researchers looking for assistance in their work
   * BU faculty members and non-members who are conducting teaching/training initiatives in computing or computational science 
   * Anyone interested in how the departments and schools at BU work together and what is done in computing at BU

## 3. Scope and Features Of The Project:
Minimum Viable Product:
  * Presents a visually pleasing and easily navigated interface
    * Dynamic system of linked nodes representing users’ collaboration
      * Making networks
        * Link
          * Published literature, research projects, people
        * Node
          * Collaborations
      * Search/filter feature making it easier to narrow down information and user profiles
      * Minimum scalability: 250 users
      * Facilitate group extensibility
        * Charles River campus and medical campus
      * Regular user UI:
        * No authentication needed
        * Users will have the ability to only see and interact with data on client server
      * Admin user UI:
        * Authentication system
        * Users will have the authority to make additions, deletions, etc. if necessary
  * Showcase the research collaboration at BU
    * Helps to understand the way computing and data-driven research is like at BU
  * Security: Provides secure storage of user credentials, servers, and data
  
 Out of scope:
   * Option to see direct collaboration and extended/mutual links
   * Live data resource
     * Update information, ability to see inactive users
   * May serve as a base prototype for other departments
     * Scalability: be able to handle more than 250 user profiles
 
## 4. Solution Concept
Global Architectural Structure Of the Project:
Below is the system components and their descriptions.

* User UI: Visualization of networks with analysis presented to public
* Admin UI: Any admin work will be done in this UI.
* Auth: Authentication is needed for admins to signup/login.
* Database: Data of affiliates and their research are stored here. 
* Business Logic: All backend jobs such as data analysis will be done here. 
* Communication: This logic is responsible for the communication between frontend and backend.
    * GET/POST/PUT/DELETE request to the database via restAPI.

![image alt text](system_design.png)

**Figure 1: System components. The frontend consists of the UI and the admin UI, and the backend consists of API, business layer, and database layer.**

Figure 1 is a diagram of the overall software lifecycle for this web-based visualization project. It is expected to have two types of users: regular, unauthorized users and admins. The regular users only have GET request privilege, which fetches the data from database via restAPI and displays it on the client side, whereas admins have GET/POST/PUT/DELETE request privileges if necessary. Authentication system will be implemented, so only the admins with the credential can perform such tasks. All the requests that go to the API layer will be handled by the communication logic in the business layer. The communication logic is responsible for all the communications between restAPI and database, as well as sending commands to Analysis logic to compute any analysis. The communication layer, then, sends the analysis result to the database as well as fetching it to update the data on the restAPI. 

Design Implications and Discussion:
* The layers should not have a significant impact on each other. That being said, if any change that’s been made in one layer should have minimal to no effect to other layers. This is to reduce the time to search for bugs when one part of the program fails. 
* Vanilla Javascript or a JS framework (i.e. React.js) will be used for the frontend and Python and Flask will be used for the backend.
* The data in restAPI will be fetched from the database per GET request through communication logic. If any changes are made in the database, the updated value will be fetched in the next GET request. 
* Analysis logic computes the jobs only when the database is updated in order to reduce the loading time. The computational functions will be called with POST/PUT/DELETE requests. GET requests will bypass the analysis logic. 

## 5. Acceptance criteria
The minimum acceptance criteria is an interactive, web-based network visualization showing the existing connections between Hariri Institute affiliates and their research areas.

Stretch goals:
* Analytics implementation for Hariri Institute visualizations
* CLI for deploying similar visualizations in different settings
* Tooling for custom analytics

## 6. Release Planning

* Sprint 1 (Demo: Oct. 1):
  * As an admin user, I’d like to be able to easily see who’s involved and how they are related to each other
    * Visualization of network collaborations
  * As a potential collaborator, I’d like to interact with the visualization in order to make it easier to get in contact with a researcher within the      Institute
  * As a BU faculty member, I’d like for my contact information to be displayed if a potential collaborator were interested in working with me
  * configure API
  * Start constructing D3 front-end
  * Discuss with mentors what kind of database to use
  * Keep up to date with Taiga project management so that clients are aware of progress/setbacks

* Sprint 2 (Demo: Oct. 15)：
  * As a regular user, I would like for my contact and collaboration information to be updated frequently, so I don’t miss out on opportunities
  * As a user of this network i would like to privately collab with someone in the department of biomedical engineering and maybe someone else within the domain of biostatistics and public health because i need a team for research 
  * As someone not currently affiliated with computing at BU, I would like to see what work is currently being done so that I can reach out if there are projects that align with my interests and experience
    * Filter: department, college, domains, interests
  * Combine D3 front-end with current API
  * Keep up to date with Taiga project management so that clients are aware of progress/setbacks

* Sprint 3 (Demo: Oct. 29):
  * TBD
  * Keep up to date with Taiga project management so that clients are aware of progress/setbacks

* Sprint 4 (Demo: Nov. 12):
  * TBD
  * Keep up to date with Taiga project management so that clients are aware of progress/setbacks

* Sprint 5 (Demo: Dec. 3):
  * Make sure our project's goals and requirements are fulfilled
  * Verify all features are implemented correctly and working smoothly
  * Keep up to date with Taiga project management so that clients are aware of progress/setbacks

