import sys

def calculate_workouts(orms, unit='lbs', include_deload=True):

    # Validate input ranges for 1RM values
    for lift, value in zip(["Bench", "Squat", "OHP", "Deadlift"], orms):
        if value is None or value == '':
            raise ValueError(f"{lift} 1RM values cannot be None or empty.")
        
        try:
            value = int(value)  # Convert value to integer
        except ValueError:
            raise ValueError(f"{lift} 1RM must be an integer.")

        if value < 0 or value > 1000:
            raise ValueError(f"{lift} 1RM must be between 0 and 1000.")
        
    workout_plan = {}

    training_maxes = {lift: max * 0.9 for lift, max in zip(["BENCH", "SQUAT", "OHP", "DEADLIFT"], orms)}

    # Define the rep schemes and percentages for each week
    rep_schemes = {
        "WEEK 1": [(5, 0.65), (5, 0.75), (5, 0.85)],
        "WEEK 2": [(3, 0.70), (3, 0.80), (3, 0.90)],
        "WEEK 3": [(5, 0.75), (3, 0.85), (1, 0.95)]
    }

    if include_deload:
        rep_schemes["WEEK 4"] = [(5, 0.40), (5, 0.50), (5, 0.60)]  # Deload week

    # Calculate the weights for each set and bold entire main sets
    for week, reps_and_percs in rep_schemes.items():
        formatted_week = f'{week}:'
        workout_plan[formatted_week] = {}

        for lift, training_max in training_maxes.items():
            main_sets = [
                (f'<strong>{reps} x {round(training_max * perc / 5) * 5} {unit}</strong>') for reps, perc in reps_and_percs
            ]
            workout_plan[formatted_week][lift] = main_sets

    return workout_plan

def add_warmup_sets(lift_name, lift_max):
    # Calculate the training max as 90% of the 1RM
    training_max = lift_max * 0.9
    
    warmup_sets = [
        (5, round(training_max * 0.40 / 5) * 5),  # 40% of training max
        (5, round(training_max * 0.50 / 5) * 5),  # 50% of training max
        (3, round(training_max * 0.60 / 5) * 5)   # 60% of training max
    ]
    
    # Format warm-up sets without the word 'reps'
    return [f'{reps} x {weight} lbs' for reps, weight in warmup_sets]

def add_fsl_sets(workout_plan):
    # Add FSL sets logic
    for week, lifts in workout_plan.items():
        for lift, sets in lifts.items():
            for set_item in sets:
                if 'strong' in set_item:  # Find first main set with <strong> tag
                    first_set_weight = set_item.split(' x ')[-1].replace('</strong>', '')
                    break  # Only need the first main set

            fsl_label = f"<em>3-5 sets of 5-8 reps x {first_set_weight}</em>"
            sets.append(fsl_label)  # Append the FSL set

    return workout_plan

def add_pyramid_sets(workout_plan):
    # Add Pyramid sets logic
    for week, lifts in workout_plan.items():
        for lift, sets in lifts.items():
            if len(sets) >= 3:  # Ensure there are at least 3 main sets
                pyramid_sets = [
                    f"<em>{sets[-2].replace('<strong>', '').replace('</strong>', '')}</em>",  # Same as 2nd main set
                    f"<em>{sets[-3].replace('<strong>', '').replace('</strong>', '')}</em>"  # Same as 1st main set
                ]
                sets.extend(pyramid_sets)

    return workout_plan

def add_bbb_sets(workout_plan, orms, unit='lbs'):
    # Add BBB (Boring But Big) sets logic
    for week, lifts in workout_plan.items():
        for lift, sets in lifts.items():
            training_max = orms[["BENCH", "SQUAT", "OHP", "DEADLIFT"].index(lift)] * 0.9
            bbb_weight = round(training_max * 0.50 / 5) * 5  # 50% of the training max
            bbb_label = f"<em>5 sets of 10 x {bbb_weight} {unit}</em>"
            sets.append(bbb_label)  # Append the BBB set

    return workout_plan