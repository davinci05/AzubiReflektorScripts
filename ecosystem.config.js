module.exports = {
    apps: [
      {
        name: 'mirrorcontrol-webserver',
        script: './mirrorcontrol/main.py',
        interpreter: 'python3'
      },
      {
        name: 'movement-sensor-script',
        script: './movement_sensor/main.py',
        interpreter: 'python3'
      },
      {
        name: "influx-data-script",
        script: "./influx_data/main.py",
        interpreter: "python3",
        cron_restart: "*/5 * * * *" // Run every 5 minutes
      }
    ]
  }
  