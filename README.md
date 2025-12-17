PyFinance Tracker
A Full-Stack Spending Tracking & Visualization Tool
PyFinance Tracker is a lightweight web application designed to help users track their daily cash flow and spending habits.

It is built with Flask, SQLite, NumPy, and Matplotlib, allowing users to generate statistical visualizations of spending distributions.

Key Features
Data Visualization:

Generate high-DPI histograms.

Use NumPy for efficient data vectorization and dynamic binning.

Use Matplotlib 'Agg' for thread-safe rendering.

Transaction Management:

Support CRUD operations for expense records.

Defensive Programming: Implements server-side validation and error handling.

Parameter Unpacking: Clean data passing between backend and frontend.

Clean User Interface:

Responsive ghost buttons for dangerous actions.

Tech Stack
Backend: Python, Flask

Database: SQLite3

Data Processing: NumPy, Matplotlib

Frontend: HTML, CSS, Jinja2 Templates

How to Run Locally
Clone the repository

Bash

git clone https://github.com/zjc-0680/PyFinance-Tracker.git
Create virtual environment

Bash

python -m venv venv

# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate
Install dependencies

Bash

pip install -r requirements.txt
Run the App In the terminal, enter:

Bash

python app.py
Enjoy the App Open your browser and visit: http://127.0.0.1:5000/

Future Improvements
[ ] Add user authentication

[ ] Implement weekly/monthly/yearly spending reports

[ ] Deploy to cloud platforms