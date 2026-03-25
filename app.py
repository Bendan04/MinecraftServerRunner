from flask import Flask, render_template, request, redirect
import subprocess
import os

app = Flask(__name__)

server_process = None
SERVER_FOLDER = "server" # Placeholder

def accept_eula():
    eula_path = os.path.join(SERVER_FOLDER, "eula.txt") # Auto accept EULA
    with open(eula_path, "w") as f: # Create eula.txt and write "eula=true" to it
        f.write("eula=true\n") # Accept EULA

def find_server_file():
    for file in os.listdir(SERVER_FOLDER): # Look for .bat or .jar files in the server folder
        if file.endswith(".bat"): # If a .bat file is found, return it
            return ("bat", file)
        if file.endswith(".jar"): # If a .jar file is found, return it
            return ("jar", file)
    return (None, None)

@app.route("/")
def index():
    status = "Running" if server_process else "Stopped" # Determine server status based on whether the process is running
    return render_template("base.html", status=status)

@app.route("/start", methods=["POST"])
def start():
    global server_process

    if server_process is None:
        accept_eula() # Ensure EULA is accepted before starting the server

        file_type, file_name = find_server_file() # Find the server file to run (either .bat or .jar)

        if file_type == "bat": # If it's a .bat file, run it directly using subprocess.Popen
            server_process = subprocess.Popen(
                file_name,
                cwd=SERVER_FOLDER,
                shell=True
            )

        elif file_type == "jar": # If it's a .jar file, run it using "java -jar" command
            server_process = subprocess.Popen(
                ["java", "-jar", file_name, "nogui"],
                cwd=SERVER_FOLDER
            )

    return redirect("/")

@app.route("/stop", methods=["POST"])
def stop():
    global server_process

    if server_process: # If the server process is running, terminate it
        server_process.terminate()
        server_process = None

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)