from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3


app = Flask(__name__)
app.secret_key = 'Atp@4466'  # Required for flashing messages





# Create a database connection and table if not exists
def init_db():

    # conn = sqlite3.connect('batteries.db')
    conn = sqlite3.connect('batteries1.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS battery_sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            mobile_number TEXT NOT NULL,
            sale_date TEXT NOT NULL,
            battery_id TEXT NOT NULL UNIQUE,
            battery_name TEXT NOT NULL ,
            ampires INTEGER NOT NULL,
            price REAL NOT NULL,
            warranty TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()
# Route to handle form submission
@app.route('/add', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        mobile_number = request.form['mobile_number']
        sale_date = request.form['sale_date']
        # print(sale_date)
        battery_id = request.form['battery_id']
        battery_name = request.form['battery_name']
        # print(battery_name)
        ampires = request.form['ampires']
        price = request.form['price']
        warranty = request.form['warranty']

        conn = sqlite3.connect('batteries.db')
        c = conn.cursor()

        # Check if battery ID already exists
        c.execute('SELECT * FROM battery_sales WHERE battery_id = ?', (battery_id,))
        existing_battery = c.fetchone()

        if existing_battery:
            # Flash message for duplicate battery ID
            flash(f"सीरियल नंबर वाली बैटरी पहले से मौजूद है : {battery_id}", 'error')
        else:
            # Insert the new battery sale data
            c.execute('''
                INSERT INTO battery_sales (customer_name, mobile_number, sale_date, battery_name, battery_id, ampires, price, warranty)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (customer_name, mobile_number, sale_date, battery_name, battery_id, ampires, price, warranty))
            conn.commit()

            # Flash success message
            flash("बैटरी डेटा सफलतापूर्वक जोड़ा गया!", 'success')

        conn.close()

        return redirect(url_for('index'))

    return render_template('index.html')

# Route to handle searching for data by battery ID
@app.route('/search', methods=['GET', 'POST'])
def search():
    result = None
    session.clear()
    if request.method == 'POST':
        battery_id = request.form['battery_id']
        conn = sqlite3.connect('batteries.db')
        c = conn.cursor()
        c.execute('SELECT * FROM battery_sales WHERE battery_id = ?', (battery_id,))
        result = c.fetchone()
        conn.close()
        if result:
            
            return render_template('search.html', result=result)
        else:
            flash("Not Found")
            return render_template('search.html', result=result)
    return render_template('search.html', result=result)


@app.route("/")
def main():
    return render_template("main.html") 


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    app.run(port=5001)
