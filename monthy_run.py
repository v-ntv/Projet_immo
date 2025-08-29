import subprocess

files_to_run = ["script1.py", "script2.py"]

for file in files_to_run:
    subprocess.run(["python", file])
