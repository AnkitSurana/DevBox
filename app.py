import os
import subprocess
import socket
import requests
from flask import Flask, render_template, jsonify

app = Flask(__name__, static_url_path='/static')

# Function to get the EC2 instance's private IP using socket
def get_instance_private_ip():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.error as e:
        app.logger.error(f"Error fetching instance private IP: {e}")
        return None

# Route to render the index.html file
@app.route('/')
def index():
    return render_template('index.html')

# Function to check if a URL is reachable
def is_url_reachable(url):
    try:
        response = requests.get(url, timeout=2)
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error reaching URL {url}: {e}")
        return False

# Route to launch Airflow based on the selected environment
@app.route('/launch_airflow/<environment>')
def launch_airflow(environment):
    airflow_url = f'https://airflow-master.{environment}.assistant.natwest.com/'  # Replace with your actual Airflow URL
    return jsonify({'url': airflow_url})

# Route to launch an insight portal in a new tab
@app.route('/launch_insight_portal')
def launch_insight_portal():
    url = 'http://example.com/form'  # Replace with your actual URL
    return jsonify({'url': url})

# Route to launch Jupyter Lab or open the browser
@app.route('/launch_jupyter_lab')
def launch_jupyter_lab():
    instance_ip = get_instance_private_ip()
    if not instance_ip:
        return jsonify({'error': 'Could not determine instance IP address.'}), 500

    url = f'http://{instance_ip}:8888/lab'
    if is_url_reachable(url):
        return jsonify({'url': url})
    else:
        try:
            # Run Jupyter Lab command as a subprocess with port 8888 and ignore existing processes on the same port
            subprocess.Popen(['jupyter', 'lab', '--ip', '0.0.0.0', '--port', '8888', '--port-retries', '0'])
            return jsonify({'url': url})
        except Exception as e:
            app.logger.error(f"Error launching Jupyter Lab: {e}")
            return jsonify({'error': f'Error launching Jupyter Lab: {e}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)