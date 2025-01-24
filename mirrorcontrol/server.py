from flask import Flask, render_template, redirect, url_for
import subprocess
import platform
import datetime

app = Flask(__name__)

# In-memory list to store timeline events
timeline = []

def get_service_status():
    if platform.system() == "Linux":
        result = subprocess.run(['pm2', 'status', 'magicmirror'], stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        status = "inactive"
        if "online" in output:
            status = "active"
        update_timeline(status)
        return status
    else:
        # Simulate the service status on non-Linux systems
        status = "active"
        update_timeline(status)
        return status

def update_timeline(status):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    event = {"time": now, "status": status}
    timeline.append(event)
    # Keep only the last 10 events for simplicity
    if len(timeline) > 10:
        timeline.pop(0)

def calculate_uptime():
    if not timeline:
        return 0
    active_count = sum(1 for event in timeline if event["status"] == "active")
    return (active_count / len(timeline)) * 100

@app.route('/')
def index():
    status = get_service_status()
    uptime = calculate_uptime()
    return render_template('index.html', status=status, timeline=timeline, uptime=uptime)

@app.route('/start')
def start_service():
    if platform.system() == "Linux":
        subprocess.run(['pm2', 'start', 'magicmirror'])
    return redirect(url_for('index'))

@app.route('/getgit')
def update_git():
    if platform.system() == "Linux":
        subprocess.run(['pm2', 'stop', 'magicmirror'])
        subprocess.run(['/usr/bin/bash', '/home/admin/AzubiReflectorScripts/pipe/update.sh'])
        subprocess.run(['pm2', 'start', 'magicmirror'])
    return redirect(url_for('index'))

@app.route('/stop')
def stop_service():
    if platform.system() == "Linux":
        subprocess.run(['pm2', 'stop', 'magicmirror'])
    return redirect(url_for('index'))

@app.route('/restart')
def restart_service():
    if platform.system() == "Linux":
        subprocess.run(['pm2', 'restart', 'magicmirror'])
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)