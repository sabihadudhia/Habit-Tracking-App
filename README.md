# Habit Tracker App

## Overview
This app allows users to create, manage, and analyze their habits. It supports daily and weekly tracking, shows streaks, and provides analytics on habit performance.

## Features
- Create new habits with daily or weekly frequency.
- Mark habits as completed and track streaks.
- Analyze habits with built-in analytics functions.
- Command-line interface (CLI) using Python Click.

## Installation
1. Clone the repository:
   
bash
   git clone https://github.com/sabihadudhia/Habit-Tracking-App
   cd habit-tracker-app
   
2. Set up a virtual environment
bash
   python -m venv venv
   source venv\Scripts\activate
   
3. Install the required packages:
    
bash
    pip install -r requirements.txt

3. If requirements.txt is not installed, first install it manually:
bash
    pip install click pytest

## Usage
The Command Line Interface is utilized for the application usage

1. Creating a habit:
   
bash
   python cli.py create-habit --name "Habit Name" --periodicity "daily/weekly" --start-date YYYY-MM-DD

2. Listing habits:
bash
   python cli.py list-habits

3. Checking off a habit:
   
bash
   python cli.py check-off --name "Habit Name"

4. Analysing a habit:
bash
   python cli.py analyse-habits

5. Deleting a habit:
   
bash
   python cli.py delete-habit "Habit Name"

## Data Storage
habits are stored in a JSON file (habits.json)
