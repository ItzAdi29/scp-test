# django-in-home-service-application

serviceman appointment application using djangothis web application is a example of the online service marketplace 
where the user can book appointment for services like cleaning to electrical from the ease of there home.

to run this application use the below commands.

create a virtual enviroment,

## python -m venv ihm-env

to activate the enviroment,

## source ihm-env/bin/activate

to Navigate into the application,

## cd in_home_service

now change the database, S3 bucket, input object key and SNS arn details in the setting.py and views.py file

then install the dependencies by running,

## pip install -r requirements.txt

now launch the application by below command,

python manage.py runserver 0.0.0.0:8000