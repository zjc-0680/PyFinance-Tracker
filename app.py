from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import numpy as np
import os
from datetime import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from typing import Optional, List, Dict, Any

app = Flask(__name__)

# config
DB = 'cashflow.db'
UploadFolder = 'static'
PlotFileName = 'cashflow_analysis.png'
DataTable = 'transactions' 

# get a connection to db
def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

# initialize db
def init_db() -> None:
    with get_db_connection() as conn:
        conn.execute(f'''
            CREATE TABLE IF NOT EXISTS {DataTable} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                amount REAL NOT NULL,
                date TEXT DEFAULT (datetime('now', 'localtime')) 
            )
        ''')

# routing

# mian page rooting
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        item_input = request.form.get('item')
        price_input = request.form.get('price')

        try:
            # make sure item names are filled
            if not item_input or not item_input.strip():
                raise ValueError("Item name cannot be empty")
            
            # make sure prices are filled
            if not price_input:
                 raise ValueError("Price cannot be empty")

            # convert price to float
            # Will get to excpet if there is a ValueError
            amount = float(price_input.strip().replace(',', ''))
            
            # negative prices become 0.0
            if amount < 0:
                amount = 0.0

            # push to db
            with get_db_connection() as conn:
                conn.execute(f'INSERT INTO {DataTable} (item_name, amount) VALUES (?, ?)', 
                             (item_input, amount))
        
        except ValueError as e:
            print(f"Error when adding item: {e}")
            return redirect('/')

        return redirect('/')
        
    else:
        # request.method == 'GET'   
        with get_db_connection() as conn:
            # last entry goes first
            cursor = conn.execute(f'SELECT * FROM {DataTable} ORDER BY id DESC')
            all_expenses = cursor.fetchall()

        plot_path = os.path.join(UploadFolder, PlotFileName)
        has_plot = os.path.exists(plot_path)

        # creating map to store param for rendere_template
        context = {
            'expenses': all_expenses,
            'plot_available': has_plot,
            'plot_image': PlotFileName,
        }

        # unpack context
        return render_template('index.html', **context)

# delete a specific item
@app.route('/delete/<int:id>', methods=['POST'])
def delete_expense(id: int):
    with get_db_connection() as conn:
        conn.execute(f'DELETE FROM {DataTable} WHERE id = ?', (id, ))
    return redirect('/')

# receive user email address
@app.route('/send_email', methods=['POST'])
@app.route('/send_email', methods=['POST'])
def send_email():
    email = request.form.get('email')
    email_success = False 
    
    # check for valid email
    if not email or '@' not in email:
        print(f"Invalid email input: {email}")
    else:
        print(f'\nEMAIL RECEIVED: {email}\n')
        email_success = True 

    with get_db_connection() as conn:
        expenses = conn.execute(f'SELECT * FROM {DataTable} ORDER BY id DESC').fetchall()
    
    context = {
        'expenses': expenses,
        'received_email': email_success 
    }
    
    return render_template('index.html', **context)

# Visualize spendings
def generate_plot() -> Optional[str]: 
    with get_db_connection() as conn:
        prices_data = conn.execute(f'SELECT amount FROM {DataTable}').fetchall()
    
    # draw chart only if the user has entered spendings
    if not prices_data:
        return None
        
    prices = [row['amount'] for row in prices_data]
    
    if not prices:
        return None

    prices_array = np.array(prices)
    max_price = np.max(prices_array)
    

    # adjust bin size
    step = 5 if max_price < 100 else 10 if max_price < 500 else 50
    bins = list(range(0, int(max_price) + step + 1, step))
    
    # draw chart
    fig, ax = plt.subplots(figsize=(6, 4), dpi=500)
    ax.hist(prices_array, 
            bins=bins, 
            edgecolor='white', 
            color='black', 
            alpha=0.9, 
            linewidth=1.2,  
            rwidth=0.86, 
            zorder=3)
    
    ax.set_title('Spending Distribution Analysis')
    ax.set_xlabel('Amount Range ($)')
    ax.set_ylabel('Frequency\n')
    ax.set_xticks(bins) 
    ax.grid(True, linestyle='--', alpha=0.3, color='gray', zorder=0)
    ax.grid(axis='y', alpha=0.3)

    # check directory
    if not os.path.exists(UploadFolder):
        os.makedirs(UploadFolder)

    full_plot_path = os.path.join(UploadFolder, PlotFileName)
    
    # save and exit
    fig.savefig(full_plot_path, bbox_inches='tight', dpi=500)
    plt.close(fig) 
    print(f" Chart is now at: {full_plot_path}")
    
    return PlotFileName

@app.route('/visualize')
def visualize():
    generate_plot()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    print(f'Server starting... \ Database: {DB} \n Uploads: {UploadFolder}')
    app.run(debug=True)