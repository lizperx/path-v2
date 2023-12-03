from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()  # This loads the environment variables from the .env file.

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Extract data from form
    name = request.form['name']
    job1 = request.form['job1']
    duration1 = request.form['duration1']
    job2 = request.form['job2']
    duration2 = request.form['duration2']
    job3 = request.form['job3']
    duration3 = request.form['duration3']

    # Adjusted inputs structure based on API expectation
    inputs = {
        "name": name,
        "job1": job1,
        "duration1": duration1,
        "job2": job2,
        "duration2": duration2,
        "job3": job3,
        "duration3": duration3
    }

    # Prepare data for API
    data = {
        "specification_hash": os.getenv('SPECIFICATION_HASH'),
        "config": {
            "MODEL": {
                "provider_id": "openai",
                "model_id": "gpt-3.5-turbo",
                "use_cache": True
            }
        },
        "blocking": True,
        "inputs": [inputs]  # Passing the adjusted inputs as a list
    }

    # Send data to API
    response = requests.post(
        'https://dust.tt/api/v1/w/0e9eb6604b/apps/2e5f8e0d5b/runs',
        headers={
            "Authorization": f"Bearer {os.getenv('DUST_TT_API_KEY')}",
            "Content-Type": "application/json"
        },
        json=data
    )

    # Get response
    if response.status_code == 200:
        api_response = response.json()
        completion_text = api_response['run']['results'][0][0]['value']
        return jsonify({"completionText": completion_text})
    else:
        # Return an error message
        return jsonify({"error": "API request failed"}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
