from flask import Flask, render_template, request, send_file
from workout_functions.block_calc.main import calculate_workouts
import pdfkit
import os
import json
from io import BytesIO

# Create Flask app instance
app = Flask(__name__, 
            template_folder=os.path.join('frontend', 'templates'), 
            static_folder=os.path.join('frontend', 'static'))

# Render home page
@app.route('/')
def home():
    return render_template('home.html')

# Function for adding warm-up sets
def add_warmup_sets(lift_name, lift_max):
    warmup_sets = [
        (5, round(lift_max * 0.40 / 5) * 5),  # 40% of training max
        (5, round(lift_max * 0.50 / 5) * 5),  # 50% of training max
        (3, round(lift_max * 0.60 / 5) * 5)   # 60% of training max
    ]
    return warmup_sets

# Route to handle workout calculator form
@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    if request.method == 'POST':
        try:
            # Extract 1RM inputs from the form
            bench_1rm = int(request.form['bench_1rm'])
            squat_1rm = int(request.form['squat_1rm'])
            ohp_1rm = int(request.form['ohp_1rm'])
            deadlift_1rm = int(request.form['deadlift_1rm'])
            unit = request.form.get('unit', 'lbs')
            include_warmup = request.form.get('warmup', 'no') == 'yes'
            include_deload = request.form.get('deload', 'yes') == 'yes'  # Default to 'yes' if not specified

            # Debugging output for selected unit
            print(f"Unit selected: {unit}")
            
            # Call to calculate the workout plan
            orms = (bench_1rm, squat_1rm, ohp_1rm, deadlift_1rm)
            workout_plan = calculate_workouts(orms, include_deload=include_deload)

            # Add warm-up sets if the option is selected
            if include_warmup:
                for lift, lift_max in zip(["BENCH", "SQUAT", "OHP", "DEADLIFT"], orms):
                    warmup_sets = add_warmup_sets(lift, lift_max)
                    for week in workout_plan:
                        # Ensure the lift exists in the current week's plan
                        if lift not in workout_plan[week]:
                            workout_plan[week][lift] = []
                        # Prepend warm-up sets before the main workout sets
                        workout_plan[week][lift] = warmup_sets + workout_plan[week][lift]

            # Generate workout plan
            return render_template('calculator.html', workout_plan=workout_plan, unit=unit)
        
        # Error handling
        except ValueError:
            return render_template('calculator.html', error="Please enter valid integer values for all 1RMs.")
    
    # If GET request, just render the form
    return render_template('calculator.html')

# Render FAQ page
@app.route('/faq')
def faq():
    return render_template('faq.html')

# Generate PDF from workout plan
@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    try:
        # Extract the JSON from form and parse with py dict.
        workout_plan_json = request.form['workout_plan'].strip()
        workout_plan = json.loads(workout_plan_json)
        unit = request.form.get('unit', 'lbs')
        
        # Render HTML template for PDF generation
        rendered = render_template('pdf_template.html', workout_plan=workout_plan, unit=unit)
        
        # Generate PDF from HTML
        path_to_wkhtmltopdf = '/usr/bin/wkhtmltopdf'
        config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
        
        pdf = pdfkit.from_string(rendered, False, configuration=config)
        
        # Return PDF as a download
        response = BytesIO(pdf)
        return send_file(
            response,
            as_attachment=True,
            download_name='workout_plan.pdf',
            mimetype='application/pdf'
        )
    # Error handling
    except Exception as e:
        print("Error during PDF generation:", e)
        return "Error generating PDF", 500

# Run flask app. In debug mode, the server will reload on code changes.
if __name__ == '__main__':
    app.run(debug=True)
