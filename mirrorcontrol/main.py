from flask import Flask, render_template, redirect, url_for
import subprocess
import platform
import datetime

app = Flask(__name__)

# In-memory list to store timeline events
timeline = []

def get_service_status():
    """Check the service status of MagicMirror using pm2."""
    if platform.system() == "Linux":
        try:
            # Abrufen der pm2-Status-Tabelle
            result = subprocess.run(['pm2', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            output = result.stdout.decode('utf-8')

            # Initialstatus als inaktiv setzen
            status = "inactive"

            # Jede Zeile nach dem MagicMirror-Prozess durchsuchen
            for line in output.splitlines():
                if "magicmirror" in line.lower() and "online" in line.lower():
                    status = "active"
                    break

            update_timeline(status)
            return status
        except FileNotFoundError:
            return "pm2 not installed"
        except Exception as e:
            return f"Error: {e}"
    else:
        # Simulate the service status on non-Linux systems
        status = "active"
        update_timeline(status)
        return status

def update_timeline(status):
    """Update the timeline with the current status."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    event = {"time": now, "status": status}
    timeline.append(event)
    # Keep only the last 10 events for simplicity
    if len(timeline) > 10:
        timeline.pop(0)

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
