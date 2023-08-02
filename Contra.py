import subprocess
import os

folder_path = "./Contra-DC"
if os.path.isdir(folder_path):
    print("Already cloned ...")
else:
    print("Cloning the folder. Wait...")
    # Set the GitHub repository URL
    repo_url = "https://github.com/JonathanCauchon/Contra-DC"
    #  Set the local path where the repository should be cloned
    # local_path = "/path/to/local/repo"
    # Run the git clone command
    command = ["git", "clone", repo_url]
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Check if the command was successful
    if result.returncode == 0:
        print("The repository was cloned successfully.")
    else:
        print("There was an error while cloning the repository.")


