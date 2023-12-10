from flask import Flask, render_template, request
import random

app = Flask(__name__)

exercises = [
    {"name": "Kettlebell Swing", "body_part": "Whole Body", "weights_kg": [8, 16, 24, 32]},
    # ... (add all other exercises)

]

def suggest_kettlebell_weight(exercise, max_press_10_reps):
    weights = exercise.get("weights_kg", [])
    
    if not weights:
        return None
    
    if max_press_10_reps <= 16:
        return random.choice(weights[:2])
    elif max_press_10_reps <= 24:
        return random.choice(weights[:3])
    elif max_press_10_reps <= 32:
        return random.choice(weights)
    else:
        return random.choice(weights)

def calculate_reps(weight, is_lower_body):
    if is_lower_body:
        return round((10 / (weight * 0.0333 + weight)))
    else:
        return round((10 / (weight * 0.0333 + weight)))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/suggest_workout', methods=['POST'])
def suggest_workout():
    workout_level = request.form.get('workout_level').lower()
    body_part = request.form.get('body_part').title()
    max_press_10_reps = float(request.form.get('max_press_10_reps'))

    if workout_level not in ["beginner", "intermediate", "advanced"]:
        return render_template('error.html', message="Invalid workout level. Please choose from beginner, intermediate, or advanced.")

    if body_part not in ["Upper", "Lower", "Whole Body"]:
        return render_template('error.html', message="Invalid body part. Please choose from Upper, Lower, or Whole Body.")

    if max_press_10_reps <= 0:
        return render_template('error.html', message="Invalid max press input. Please enter a positive value.")

    min_sets, max_sets = 0, 0

    if workout_level == "beginner":
        min_sets, max_sets = 5, 10
    elif workout_level == "intermediate":
        min_sets, max_sets = 10, 15
    elif workout_level == "advanced":
        min_sets, max_sets = 15, 25

    filtered_exercises = [exercise for exercise in exercises if exercise["body_part"] == body_part]

    if body_part == "Whole Body":
        whole_body_exercises = [exercise for exercise in exercises if exercise["body_part"] == "Whole Body"]
        if len(whole_body_exercises) < 2:
            return render_template('error.html', message="For whole body workouts, please choose at least 2 whole body exercises.")

    if not filtered_exercises:
        return render_template('error.html', message="No exercises found for the selected body part.")

    clusters = {}
    for _ in range(random.randint(min_sets, max_sets)):
        exercise = random.choice(filtered_exercises)
        suggested_weight = suggest_kettlebell_weight(exercise, max_press_10_reps)
        if exercise["name"] not in clusters:
            clusters[exercise["name"]] = []
        clusters[exercise["name"]].append(suggested_weight)

    workout_suggestion = ""
    for exercise_name, weights in clusters.items():
        workout_suggestion += f"\nSets for {exercise_name}:"
        for weight in weights:
            reps = calculate_reps(weight, exercise["body_part"] == "Lower")
            reps = min(max(6, reps), 10) if exercise["body_part"] != "Lower" else min(max(8, reps), 15)
            workout_suggestion += f"\n- {reps} reps with {weight}kg"

    return render_template('result.html', workout_suggestion=workout_suggestion)

if __name__ == '__main__':
    app.run(debug=True)
