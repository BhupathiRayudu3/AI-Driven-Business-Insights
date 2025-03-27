
from flask import Flask, render_template, url_for, redirect, jsonify, Response, abort, session, request, send_file
import sqlite3
from Customer_Segmentation_UI import predict_new_customer
from Price_Optimization_UI import price_optimization
from Profit_Prediction_UI import profit_prediction
from Sales_prediction_UI import sales_prediction
from Revenue_prediction_UI import forecast_revenue
import pandas as pd

conn = sqlite3.connect('data.db') 


#Use USER Table only when need to add new login users
conn.execute('''CREATE TABLE IF NOT EXISTS user_details
         (ID INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age TEXT,
            gender TEXT NOT NULL,
            password TEXT NOT NULL
         );''')

conn.close()


app = Flask(__name__)


def html_return(msg, redirect_to = "/", delay = 2):
    return f"""
                <html>    
                    <head>      
                        <title>Project Name </title>      
                        <meta http-equiv="refresh" content="{delay};URL='{redirect_to}'" />    
                    </head>    
                    <body> 
                        <h2 style='color:red'> {msg}</h2>
                        <p>This page will refresh automatically.</p> 
                    </body>  
                </html>   
                
                """

@app.route('/signup', methods=['get', 'post'])
def signup(): 
    if request.method == "POST":
        try:
            data = request.json

            print("Data:", data)

            name = data.get('name')
            email = data.get('email')
            age = data.get('age')
            gender = data.get('gender')
            password = data.get('password')

            if not all([name, email, age, gender, password]):
                return jsonify({"error": "All fields are required"}), 400

            # Connect to the database
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()

            # Check if email already exists
            cursor.execute("SELECT * FROM user_details WHERE email = ?", (email,))
            if cursor.fetchone():
                return jsonify({"error": "Email already exists"}), 400

            # Insert user into database
            cursor.execute(
                "INSERT INTO user_details (name, email, age, gender, password) VALUES (?, ?, ?, ?, ?)",
                (name, email, age, gender, password)
            )
            conn.commit()

            return jsonify({"message": "Signup successful"}), 201

        except Exception as e:
            return jsonify({"error": str(e)}), 500

        finally:
            if conn:
                conn.close()

    else:
        return render_template('signup.html')

@app.route('/login', methods=['get'])      
def redirect_login():
    return redirect(url_for('login_page'))
 
@app.route('/', methods=['get', 'post'])
def login_page():
    global user_details
    if request.method == 'POST':
        try:
            data = request.get_json()

            # Access email and password from the JSON payload
            email = data.get('email')
            password = data.get('password')

            print(email, password)

            # Connect to the database
            conn = sqlite3.connect('data.db')
            cursor = conn.cursor()

            # Check if the user exists and password matches
            cursor.execute("SELECT name, password FROM user_details WHERE email = ?", (email,))
            user_data = cursor.fetchone()

            if user_data is None:
                return jsonify({"error": "User not found"}), 404

            user_name, stored_password = user_data

            if password != stored_password:
                return jsonify({"error": "Invalid password"}), 401

            # Query for all user data after successful login
            cursor.execute("SELECT * FROM user_details WHERE email = ?", (email,))
           
            user_details = cursor.fetchone()

            print(user_details)

            # Set session data on successful login
            session['usermail'] = email
            session['name'] = user_name
            session['user_details'] = user_details

            # Pass all user details to the dashboard
            return  jsonify({"message": "success"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500

        finally:
            if conn:
                conn.close()

    elif 'usermail' in session.keys():
        # Direct login if user is already in session
        # Query for all user details to send to the dashboard
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_details WHERE email = ?", (session['usermail'],))
        user_details = cursor.fetchone()
        return redirect(url_for('dashboard'))

    else:
        return render_template('login-page.html')


@app.route('/dashboard', methods=['GET'])
def dashboard():
    print(session['user_details'])
    if "user_details" in session:
        return render_template('dashboard.html', user=session['user_details'], side_focus = 1)
    return redirect('/login')
 
@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

 
@app.route('/customer_segmentation', methods=['get', 'post'])
def customer_segmentation():
     
    if "user_details" in session:
        print("Coming Here")
        return render_template('customer_segmentation.html', user=session['user_details'])
    else:
        return redirect(url_for('login_page'))




@app.route('/customer_segmentation_result', methods=['get', 'post'])
def customer_segmentation_result():
    if "user_details" in session:      
        if request.method == 'POST': 

            data = dict(request.form)

            data["latitude"] = int( data["latitude"])
            data["longitude"] = int( data["longitude"])

            print("Updated Data :", data)

            prediction_result = predict_new_customer(data)

            print(prediction_result)
 
            return render_template('customer_segmentaion_result.html', user=session['user_details'], prediction_result = prediction_result, side_focus = 2)
    
    return redirect(url_for('login_page'))


# /price_optimization
@app.route('/price_optimization', methods=['get', 'post'])
def price_optimization_ui():
     
    if "user_details" in session:
        print("Coming Here")
        return render_template('price_optimization.html', user=session['user_details'])
    else:
        return redirect(url_for('login_page'))
 
@app.route('/price_optimization_result', methods=['get', 'post'])
def price_optimization_result():
    if "user_details" in session:      
        if request.method == 'POST': 

            data = dict(request.form)

            data["quantity"] = int( data["quantity"])
            data["unit_price"] = int( data["unit_price"])
            data["customers"] = int( data["customers"])
            data["lag_price"] = int( data["lag_price"])
             

            print("Updated Data :",data['product_category'], data['quantity'], data['unit_price'], data['customers'], data['lag_price'])

            product_category = data['product_category']
            quantity= data['quantity']
            unit_price= data['unit_price']
            customers= data['customers']
            lag_price= data['lag_price']

            price_optimization_result = price_optimization( product_category,quantity, unit_price, customers, lag_price )

            print(price_optimization_result)
 
            return render_template('price_optimization_result.html', user=session['user_details'], prediction_result = price_optimization_result, side_focus = 3)
    
    return redirect(url_for('login_page'))


# /price_optimization
@app.route('/profit_prediction', methods=['get', 'post'])
def profit_prediction_ui():
     
    if "user_details" in session:
        print("Coming Here")
        return render_template('profit_prediction.html', user=session['user_details'])
    else:
        return redirect(url_for('login_page'))
 
@app.route('/profit_prediction_result', methods=['get', 'post'])
def profit_prediction_result():
    if "user_details" in session:      
        if request.method == 'POST': 

            data = dict(request.form)

            print(data)
 

            RD_Spend = float(data['RD_Spend'])
            Administration= float(data['administration'])
            marketing_spend= float(data['marketing_spend'])
            state_encoded= data['state_encoded']
            

            profit_prediction_result = profit_prediction(RD_Spend,Administration, marketing_spend, state_encoded)

            print(profit_prediction_result)
 
            return render_template('profit_prediction_result.html', user=session['user_details'], prediction_result = profit_prediction_result, side_focus = 4)
    
    return redirect(url_for('login_page'))

@app.route('/sales_prediction', methods=['get', 'post'])
def sales_prediction_ui():
     
    if "user_details" in session:
        print("Coming Here")
        return render_template('sales_prediction.html', user=session['user_details'])
    else:
        return redirect(url_for('login_page'))
 
@app.route('/sales_prediction_result', methods=['get', 'post'])
def sales_prediction_result():
    if "user_details" in session:      
        if request.method == 'POST': 

            data = dict(request.form)

            print(data)
 

            city = data['city']
            customer_type=data['customer_type']
            gender=  data['gender'] 
            product_line= data['product_line']
            unit_price= float(data['unit_price'])
            quantity = float(data['quantity'])
            rating = float(data['rating'])

            sales_prediction_result = sales_prediction(city,customer_type,gender, product_line, unit_price, quantity, rating )

            print(sales_prediction_result)
 
            return render_template('sales_prediction_result.html', user=session['user_details'], prediction_result = sales_prediction_result, side_focus = 5)
    
    return redirect(url_for('login_page'))



@app.route('/revenue_prediction', methods=['get', 'post'])
def revenue_prediction_ui():
     
    if "user_details" in session:
        print("Coming Here")
        return render_template('revenue_prediction.html', user=session['user_details'])
    else:
        return redirect(url_for('login_page'))
 
@app.route('/revenue_prediction_result', methods=['get', 'post'])
def revenue_prediction_result():
    if "user_details" in session:      
        if request.method == 'POST': 

            data = dict(request.form)

            print(data)
 

            fixed_date = data['fixed_date']
            varying_date=data['varying_date']
            sequence_length= int(data['sequence_length'])
            future_steps = int(data['future_steps'])
            

            revenue_prediction_result = forecast_revenue(fixed_date, varying_date, sequence_length, future_steps )

            revenue_prediction_final_result = [(row.Date, row._2) for row in revenue_prediction_result[0].itertuples()]


            print(revenue_prediction_final_result)
             
 
            return render_template('revenue_prediction_result.html', user=session['user_details'], prediction_result = revenue_prediction_final_result, side_focus = 6)
    
    return redirect(url_for('login_page'))

@app.errorhandler(404)
def nice(_):
    return render_template('error_404.html')

app.secret_key = '3423432423gdsgdfh'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 8080, debug = True)#80)

