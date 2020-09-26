# API
## Deployment
This program worked with Python 3.8.2
### Create Virtual Environment
Clone this repo, then 
```
python3 -m venv [name_of_ur_ve]
source [name_of_ur_ve]/bin/activate
```
### Install Dependencies
```
pip install -r requirements.txt
```
### Deploy
```
python3 run.py
```

This will be running on your localhost:8080/api/v1/members.
Note that if you have something else running on the port 8080, it'll run on a different port (i.e. 8081).