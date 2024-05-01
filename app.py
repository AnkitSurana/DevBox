import requests
import subprocess
import webbrowser
from flask import Flask, render_template 

app = Flask(__name__, static_url_path='/static')

# Route to render the index.html file
@app.route('/')
def index():
    return render_template('index.html')

# Function to check if a URL is reachable
def is_url_reachable(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False

# Route to launch Airflow based on the selected environment
@app.route('/launch_airflow/<environment>')
def launch_airflow(environment):
    airflow_url = f'https://airflow-master.{environment}.assistant.natwest.com/'  # Replace with your actual Airflow URL
    # if is_url_reachable(airflow_url):
    #     # Open Airflow in a new browser tab
    webbrowser.open_new_tab(airflow_url)
    #     print(f'Airflow for environment {environment} is already accessible')
    # else:
    #     print(f'Airflow for environment {environment} is not reachable', 404)


# Route to launch a insight portal in a new tab
@app.route('/launch_insight_portal')
def launch_insight_portal():
    url = 'http://example.com/form'  # Replace with your actual URL
    # if is_url_reachable(url):
        # Open the insight portal in a new browser tab
    webbrowser.open_new_tab(url)
        # print(f'Insight Portal is already accessible')
    # else:
    #     print(f'Insight Portal is not reachable', 404)


# Route to launch Jupyter Lab or open the browser
@app.route('/launch_jupyter_lab')
def launch_jupyter_lab():
    url = 'http://localhost:8888/lab'
    if is_url_reachable(url):
        # Open Jupyter Lab in a new browser tab
        webbrowser.open_new_tab(url)
        print(f'Jupyter Lab is already running on port 8888')
    else:
        try:
            # Run Jupyter Lab command as a subprocess with port 8888 and ignore existing processes on the same port
            subprocess.Popen(['jupyter', 'lab', '--port', '8888', '--port-retries', '0'])
            print(f'Jupyter Lab launched successfully!')
        except Exception as e:
            print(f'Error launching Jupyter Lab: {e}', 500)


if __name__ == '__main__':
    app.run(debug=True)
