from flask import Flask, render_template, request
from workout_functions.block_calc.main import calculate_workouts
import os

app = Flask(__name__, 
            template_folder=os.path.join('frontend', 'templates'), 
            static_folder=os.path.join('frontend', 'static'))

@app.route('/', methods=['GET', 'POST'])
def index():
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
            return render_template('index.html', workout_plan=workout_plan)
        
        except ValueError:
            return render_template('index.html', error="Please enter valid integer values for all 1RMs.")
    
    # If GET request, just render the form
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
