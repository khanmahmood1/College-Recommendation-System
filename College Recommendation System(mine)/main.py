from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Load the dataset
file_name = 'dataset.csv'
dataset = pd.read_csv(file_name)

# Define the available branches and categories
branches = [
    "Computer Science and Engineering",
    "Mechanical Engineering",
    "Civil Engineering",
    "Electronics and Computer Science",
    "Computer Science and Engineering(Data Science)",
    "Electrical Engineering",
    "Artificial Intelligence (AI) and Data Science",
    "Computer Engineering",
    "Information Technology",
    "Artificial Intelligence and Data Science",
    "Artificial Intelligence and Machine Learning",
    "Computer Science and Engineering (Artificial Intelligence and Data Science)",
    "Electronics and Telecommunication Engg",
    "Automobile Engineering",
    "Instrumentation and Control Engineering",
    "Computer Science and Engineering (Artificial Intelligence)",
    "Computer Science and Engineering(Artificial Intelligence and Machine Learning)",
    "Chemical Engineering",
    "Robotics and Automation",
    "Bio Technology",
    "Mechanical & Automation Engineering",
    "Textile Technology",
    "Man Made Textile Technology",
    "Fashion Technology",
    "Instrumentation Engineering",
    "Food Technology",
    "Oil and Paints Technology",
    "Petro Chemical Engineering",
    "Industrial IoT",
    "Electrical Engg[Electronics and Power]",
    "Production Engineering",
    "Textile Technology",
    "Food Engineering and Technology",
    "Polymer Engineering and Technology",
    "Surface Coating Technology",
    "Food Technology And Management",
    "Civil and infrastructure Engineering",
    "Bio Medical Engineering"
]

categories = [
    "OPEN",
    "OBC",
    "SC",
    "ST",
    "ST/DEF2",
    "NT 1 (NT-B)",
    "NT 3 (NT-D)",
    "NT 2 (NT-C)",
    "NT 1 (NT-B)",
    "Open/DEF3",
    "SC/DEF1",
    "SC/DEF2",
    "OBC/PH1",
    "DT/VJ"
]

@app.route('/')
def index():
    return render_template('index.html', branches=branches, categories=categories)

@app.route('/recommend', methods=['POST'])
def recommend():
    user_data = request.get_json()
    user_percentile = user_data['percentile']
    user_branch = user_data['branch']
    user_gender = user_data['gender']
    user_category = user_data['category']

    # Filter the dataset based on the criteria entered by the user
    filtered_data = dataset[
        (dataset['percentile'] <= user_percentile) &
        (dataset['branch'].str.lower() == user_branch.lower()) &
        (dataset['gender'].str.upper() == user_gender) &
        (dataset['category'].str.lower() == user_category.lower())
    ]

    # Sort the filtered data by percentile in descending order
    sorted_data = filtered_data.sort_values(by='percentile', ascending=False)

    # Select the top 20 colleges from the sorted data
    top_colleges = sorted_data.head(20)

    # Prepare data for the response
    recommendations = [
        {
            'name': row['college_name'],
            'percentile': row['percentile'],
            'rank': row['rank']
        }
        for idx, row in top_colleges.iterrows()
    ]

    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)
