so my topic is log security analyzer and threat blocker , so here as you know websites keep web server log file where any user who clicks on the domain of website all the actions of user like where did he go , what did he do etc is stored in a specefic format along with its ip address.

so there are millions of user and their data stored in it so it becomes difficult to track all of them as there are messy lines of text in it and when an attacker comes it becomes tedious to find manually the attacker's ip address and block it

so i decided to create an automatic log securty analyzer and theat blocker where based on the ip address we track the user/attacker behaviour and add it in a clean and structured format in sqlite database and then we detect two types of threats / attacks :

1. brute force attack -> where the attacker tries to log into a webiste multiple times like 50 times with 5 seconds with wrong passwords and failed

2. directory scanning attack: where attacker tries to invade hidden administrative files like /admin , /.env etc

and then we detect the attack made by the attacker along with attacker's ip address we sent an alert message / notification to phone / slack / discord and then we block the ip address either through windows firewall simulator or by connectin to cloudflare api connector ( cloud firewall api)

and then there is a dashbaord also called soc dashbaord which shows live charts , maps and alert messages we can view it visually.

the front end used is react with javascript library , we are using SIEM ( security information and event management ) that help in real time loging activity , http traffic request , detecting the threats , blocking it and running SOAR engine playbook

now SOAR stands for ( security orchestration and automation response) which executes the whole automated pipeline of our project.

for server we are using fast api server as it also provides swagger ui which is used to test fast api endpoints internally in the browser without externally relying on tools like postman 

and then we have executed active monitoring 

and we use regex (regular expressions ) which  uses template that we give a rulebook which creates variables on how to store info from web server log file

we display the alerts and attacks detected in terminal as well in dashboard 

we have also pasted discord web hook url , where the alert notifications are shown in the SIEM Security lab server

there is no maximum limit to store logs in a database , we use two frameworks apache for backend api and nginx for frontend api , so when recent logs are taken from apache from the server the maximum limit is 50 then when apache gives to nginx and nginx gives to user by showing on the dashboard then the maximum limit is 15.

``` text
Directory structure:
└── itiyashah-log-security-analyzer/
    ├── images.md
    ├── requirements.txt
    ├── app/
    │   ├── alerts.py
    │   ├── detector.py
    │   ├── firewall.py
    │   ├── main.py
    │   ├── parser.py
    │   └── soar_engine.py
    └── security-dashboard/
        ├── package.json
        └── src/
            ├── App.css
            └── App.js
```

to run the react app , first run uvicorn app.main:app --reload on one terminal then on another terminal run cd security-dashboard and then npm start , to run specefic python code script files run it in third terminal

then we also have option where admin can manually block the ip addresses






