from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)

# Get the path to the desktop
desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')

# List of policies with their points
policies = [
    ("Tax carbon emissions to save the planet vs. Cut carbon taxes to boost the economy!", 10),
    ("Subsidize green energy to fuel the future vs. Fund fossil fuels to keep the lights on!", 9),
    ("Trade carbon credits to cap pollution vs. Ditch carbon trading for business freedom!", 8),
    ("Invest in public transit to clear the air vs. Build more highways for smoother rides!", 7),
    ("Enforce energy-saving rules for efficiency vs. Relax energy standards for lower costs!", 8),
    ("Capture and store carbon to clean the sky vs. Abandon carbon capture for cheaper solutions!", 7),
    ("Drive electric cars to a cleaner tomorrow vs. Stick with gasoline cars for economic gains!", 9),
    ("Build green homes for a sustainable living vs. Support traditional construction for affordability!", 8),
    ("Conserve forests to trap carbon vs. Develop land to spur economic growth!", 9),
    ("Farm sustainably to nourish the Earth vs. Intensify agriculture to maximize yield!", 7)
]

@app.route('/')
def index():
    return render_template('index.html', policies=policies)

@app.route('/submit', methods=['POST'])
def submit():
    contestant_name = request.form['name']
    selected_policies = request.form.getlist('policies')
    if len(selected_policies) != 5:
        return redirect(url_for('index'))
    total_score = sum(int(policy.split('|')[-1]) for policy in selected_policies)
    
    # Store results in an Excel file on the desktop
    results = {
        "Contestant Name": contestant_name,
        "Selected Policies": [selected_policies],
        "Total Score": [total_score]
    }
    df = pd.DataFrame(results)
    file_path = os.path.join(desktop, "contest_results.xlsx")
    try:
        df_existing = pd.read_excel(file_path)
        df = pd.concat([df_existing, df], ignore_index=True)
    except FileNotFoundError:
        pass
    df.to_excel(file_path, index=False)

    return render_template('result.html', score=total_score)

if __name__ == '__main__':
    app.run(debug=True)
