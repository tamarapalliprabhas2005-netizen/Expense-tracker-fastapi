# Expense Tracker

A simple backend project made with FastAPI and MySQL.

Users can create an account, log in, and save their daily expenses. Each user can see only their own expenses.

## What it can do
- Register and login (with JWT token)
- Add an expense
- See all my expenses
- Edit an expense
- Delete an expense
- See total per category
- See a monthly report

## Technologies used
- Python
- FastAPI
- MySQL
- SQLAlchemy
- JWT and bcrypt (for safe login)

## Files in this project
- main.py : all the APIs
- database.py : connects to MySQL
- models.py : database tables
- schemas.py : checks the data
- auth.py : password and token code

## How to run
1. Install packages: pip install -r requirements.txt
2. Create a MySQL database: CREATE DATABASE expense_db;
3. In database.py, replace YOUR_PASSWORD with your MySQL password
4. Start the server: uvicorn main:app --reload
5. Open http://127.0.0.1:8000/docs in your browser and test the APIs

## Made by
T.prabash
