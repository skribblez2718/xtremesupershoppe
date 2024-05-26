# xtremesupershoppe
xtremesupershoppe is a vulnerable web application that can be solved with code analysis or blackbox methods. It is heavily influenced by Denis Ivy and Brad Traversy's Udemy course [Django with React | An Ecommerce Website](https://www.udemy.com/course/django-with-react-an-ecommerce-website) and a real life pentest engagements. The goal of the challenge is obtain admin privileges and capture the flag.

***IMPORTANT***: Currently deploying this application may or may not require some troubleshooting. It is on the TO DO to fix. The repository is still well suited for code analysis; however, I recommend getting the application up for learning purposes. Also, the exploit is very fun IMO! Finally, I originally created this application 2+ years ago. There may be vulnerabilities in this app that didn't exist or were unknown at it's creation time. Cpuld be a fun rabbit hole for the daring.

## Basic Setup
```sh
git clone https://github.com/skribblez2718/xtremesupershoppe.git
cd xtremesupershoppe/backend
virtualenv venv || pythhon3 -m pip virtualenv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
cd frontend
npm install
```

### Database Setup:
Install and start the postgresql service as per you OS's instructions

```sh
sudo -u postgres psql

postgres=# create database $DB_NAME;
postgres=# create user $USER with encrypted password '$DB_PASSWORD';
postgres=# grant all privileges on database $DB_NAME to $DB_USER;
postgres=# \q
```

Update the backend/backend/settings.py file with applicable database values

### Web Server Setup
From the xtremesupershoppe/backend directory run the below

```sh
python3 manage.py createsuperuser $SUPER_USER_EMAIL:$SUPER_USER_PASSWD
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic
python3 manage.py runserver localhost:8000 > /dev/null 2>&1 &
```

### PayPal
For full functionality (allowing purchase and checkout) a testing PaypAl account is required. Check out [PayPal Developer](https://developer.paypal.com) for the deets. Also, the client_id (found in backend/frontend/src/screens/OrderScreen.js) allowing PayPal integration is controlled by the ```javascript PAYPAL_CLIENT_ID``` environment variable.

Initially the application contained unintended logic flaws in the check out. These in theory should be fixed, but again, could be a fun rabbit hole to explore.

### S3
The application originally used S3 to upload images in the admin panel. If this functionality is desired see the applicable section in settings.py

### Hard Mode?
The CSP can be manipulated to prevent/allow certain attack strategies. Namely the connect-src attribute

### Optional, but Recommended for Realism
The interact.sh script simulates an admin user viewing the web page. This is probably best ran as a cron job. Chromedriver is required for this and setting the ```sh APP_HOST``` environment variable. You can also add more users to simulate higher volumes of traffic that include non-admin users. An extra bump for the Hard Mode


## TO DO
- Determine cause of the error ```sh settings.DATABASES is improperly configured. Please supply the NAME or OPTIONS['service'] value``` when running the ```sh python3 manage.py makemigrations```
    - settings.py appears fine and this historically was not an issue when deploying. 
- Complete setup instructions

## Resources
- [The Web Developer Bootcamp](https://www.udemy.com/course/the-web-developer-bootcamp/)
- [Django with React | An Ecommerce Website](https://www.udemy.com/course/django-with-react-an-ecommerce-website)
- [Django ProShop](https://github.com/divanov11/proshop_django)
- [PayPal Developer](https://developer.paypal.com)