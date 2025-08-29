import subprocess

files_to_run = ["get_fiscality.py", "script2.py"]

for file in files_to_run:
    subprocess.run(["python", file])
