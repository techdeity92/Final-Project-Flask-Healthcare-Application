# Final-Project-Flask-Healthcare-Application

---

## Overview

This project collects and processes personal financial data using a full stack workflow. It includes a Flask web application, MongoDB storage, CSV export, data visualization in a Jupyter notebook, and deployment to AWS using Elastic Beanstalk.

---

## Features

- Collects **user data** (age, gender, income, expenses).
- Stores that data in **MongoDB Atlas** and also in a **CSV file**.
- Uses a Python class named `User` to manage the data and format it for both storage methods.
- Includes a **Jupyter notebook** to visualize trends:
  - Who earns the most by age.
  - How different genders spend across categories.
- Visualizations are exported for PowerPoint.
- The web app is deployed live on **AWS Elastic Beanstalk**.

---

## Project Structure

application.py : Main Flask app that runs the survey form and handles logic

Flask Healthcare Application.py : Version used for local testing before AWS deployment

requirements.txt : Lists all required Python packages

procfile : Tells AWS how to run the Flask app

user_data.csv : Stores survey responses locally for visualization

Flask Healthcare Application.ipynb : Jupyter notebook for analysis and chart generation

charts/ : Folder containing exported visual charts (PNG/JPG)

---

## Data Visualization (Jupyter)
Open Flask Healthcare Application.ipynb in Jupyter.

It reads from the saved user_data.csv.

Generates the following charts:

Bar chart: Ages with the highest income.

Bar chart: Gender distribution across expense categories.

Charts are saved to the charts/ folder.

---

## Deployment on AWS
Deployed using Elastic Beanstalk with Python 3.13 on Amazon Linux 2023.

Packaged as a zip file (application.zip) containing:

- application.py

- requirements.txt

- procfile

Uploaded and launched via the AWS Console.

MongoDB connection string is included in application.py.

## Live Application

Access the deployed survey here:

(http://flaskhealthcareapplication-env.eba-33qksxmn.us-east-2.elasticbeanstalk.com/)

