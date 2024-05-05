import multiprocessing
import subprocess

# Get the workers by CPU
workers = multiprocessing.cpu_count() * 2 + 1

# Bind gunicorn to Port
bind = "0.0.0.0:9001"

# Specify the application to run
module = "main:app"

# Specify the application type
application_type = "uvicorn"

# Construct the Gunicorn command
gunicorn_command = [
    "gunicorn",
    f"--workers={workers}",
    f"--bind={bind}",
    f"--worker-class={application_type}.workers.UvicornWorker",
    module
]

# Run the Gunicorn command
subprocess.run(gunicorn_command)
