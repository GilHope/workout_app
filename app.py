from flask import Flask, render_template, request
from workout_functions.block_calc.main import calculate_workouts
import os

app = Flask(__name__, 
            template_folder=os.path.join('frontend', 'templates'), 
            static_folder=os.path.join('frontend', 'static'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    if request.method == 'POST':
        try:
            # Get the 1RM inputs from the form
            bench_1rm = int(request.form['bench_1rm'])
            squat_1rm = int(request.form['squat_1rm'])
            ohp_1rm = int(request.form['ohp_1rm'])
            deadlift_1rm = int(request.form['deadlift_1rm'])
            
            # Calculate the workout plan
            orms = (bench_1rm, squat_1rm, ohp_1rm, deadlift_1rm)
            workout_plan = calculate_workouts(orms)

            # Pass the workout plan to the template
            return render_template('calculator.html', workout_plan=workout_plan)
        
        except ValueError:
            return render_template('calculator.html', error="Please enter valid integer values for all 1RMs.")
    
    # If GET request, just render the form
    return render_template('calculator.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

if __name__ == '__main__':
    app.run(debug=True)
