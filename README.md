# FinanceTracker 

A project to practice Flask, PostgreSql, MongoDB and Docker. 
Code in this project is not 100% refactored and it could use more design, but I was using it mainly to relearn and learn some of the concepts related to Flask and Docker. 
This project consists of Flask App with login and registration connected to Postgres database and part of Flask App that allows for creation, updating, deleting and displaying of Expenses. 
For login and registration, it does not use any extra methods of authentication like e.g. email, text messages, etc. This could be implemented using, e.g. standard libraries or via API like Twilio. 
Financial tracking could be improved by:  
- Adding pagination. 
- An option to standardize currency so that it would be easier to make data universal. E.g. an option in the form to specify which currency was used for a purchase. 
- Extra database in MongoDB for money-in. This would lead to an extra functionality where the user could see Spending against Income. 
- More options to organize data, e.g. by Category, by Item Name, most expensive to least expensive, etc. 
Initially the App was made using Postgres locally and connecting to MongoDB via MongoDB Atlas. Once moved to Docker, the app and both databases were moved to containers. 
This repository includes Dockerfile for App only. To build an image for Postgres I used Dockerfile with: 

FROM postgres 

> COPY init.sql /docker-entrypoint-initdb.d/ 

With init.sql: 

> CREATE DATABASE users; 

For MongoDB, I used official MongoDB image. 

For .env file these variables were set: 
PROJECT_KEY 
DATABASE_URL 
DATABASE_URL2 
PGHOST 
PGPORT 
POSTGRES_USER 
POSTGRES_PASSWORD 
MONGO_INITDB_ROOT_USER 
MONGO_INITDB_ROOT_PASSWORD 
MONGO_INITDB_DATABASE 

- Healthcheck for MongoDB could be added. 


* This project does not include docker volumes. * 
