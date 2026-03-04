import subprocess, os, sys

project_dir = "/vercel/share/v0-project/scripts/backend"
os.makedirs(project_dir, exist_ok=True)
os.chdir(project_dir)
subprocess.run([sys.executable, "-m", "pip", "install", "flask", "flask-cors"], check=True)
print("flask and flask-cors installed successfully")
