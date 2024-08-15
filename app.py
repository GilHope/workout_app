from flask import Flask, render_template, request, send_file
from workout_functions.block_calc.main import calculate_workouts
import pdfkit
import os
import json
import traceback
from io import BytesIO

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

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    try:
        workout_plan_json = request.form['workout_plan'].strip()
        print("Received workout plan JSON:", repr(workout_plan_json))
        workout_plan = json.loads(workout_plan_json)
        
        rendered = render_template('pdf_template.html', workout_plan=workout_plan)
        
        path_to_wkhtmltopdf = '/usr/bin/wkhtmltopdf'
        config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
        
        pdf = pdfkit.from_string(rendered, False, configuration=config)
        
        response = BytesIO(pdf)
        return send_file(
            response,
            as_attachment=True,
            download_name='workout_plan.pdf',
            mimetype='application/pdf'
        )
    except Exception as e:
        print("Error during PDF generation:", e)
        traceback.print_exc()
        return "Error generating PDF", 500

if __name__ == '__main__':
    app.run(debug=True)
