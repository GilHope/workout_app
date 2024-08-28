import sys

def calculate_workouts(orms, unit='lbs', include_deload=True):
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
    warmup_sets = [
        (5, round(lift_max * 0.40 / 5) * 5),  # 40% of training max
        (5, round(lift_max * 0.50 / 5) * 5),  # 50% of training max
        (3, round(lift_max * 0.60 / 5) * 5)   # 60% of training max
    ]
    return [(f'{reps} reps', f'{weight} lbs') for reps, weight in warmup_sets]