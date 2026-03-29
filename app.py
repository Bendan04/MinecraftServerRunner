from flask import Flask, render_template, request, redirect
import subprocess
import os

app = Flask(__name__)

server_process = None
SERVER_FOLDER = None


def accept_eula():
    if not SERVER_FOLDER:
        return

    eula_path = os.path.join(SERVER_FOLDER, "eula.txt")
    with open(eula_path, "w") as f:
        f.write("eula=true\n")


def find_server_file():
    if not SERVER_FOLDER:
        return (None, None)

    for file in os.listdir(SERVER_FOLDER):
        if file.endswith(".bat"):
            return ("bat", file)
        #if file.endswith(".jar"): # Uncomment this eventually to also work with java server starters
            #return ("jar", file)

    return (None, None)


@app.route("/")
def index():
    status = "Running" if server_process else "Stopped"
    return render_template(
        "dashboard.html",
        status=status,
        folder=SERVER_FOLDER
    )


@app.route("/set-folder", methods=["POST"])
def set_folder():
    global SERVER_FOLDER
    folder = request.form.get("folder")

    if folder and os.path.exists(folder):
        SERVER_FOLDER = folder

    return redirect("/")



@app.route("/start", methods=["POST"]) 
def start(): 
    global server_process 
    if server_process is None and SERVER_FOLDER: 
        accept_eula() 
        file_type, file_name = find_server_file() 
        if file_type == "bat": 
            print("Starting server using batch file:", file_name) 

            server_process = subprocess.Popen(
                ["cmd.exe", "/k", 'run.bat'], # Change this to f'{file_name}' eventually
                cwd=SERVER_FOLDER,
                creationflags=subprocess.CREATE_NEW_CONSOLE
        )
        elif file_type == "jar": 
            print("Starting server using jar file:", file_name) 
            server_process = subprocess.Popen( ["java", "-jar", file_name, "nogui"],
             cwd=SERVER_FOLDER, creationflags=subprocess.CREATE_NEW_CONSOLE ) 
            
    return redirect("/")


@app.route("/stop", methods=["POST"])
def stop():
    global server_process

    if server_process:
        server_process.terminate()
        server_process = None

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)