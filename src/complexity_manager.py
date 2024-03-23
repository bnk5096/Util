"""
Handles the processing of both Metrix++ and SonarScanner/SonarQube
"""

import subprocess
import requests
import os
import sonar_fetch
import time

PROJECT_NAME = "test"
TOKEN = "sqp_4c14e1cf903ca8706f5b5be9cc0747c65389b214"
# TOKEN = "SONAR_QUBE_TOKEN_HERE"

def complexity(name):
    """
    Processes complexity calculations from sonarQube
        Parameters:
            name (string): the repository name
    """
    work_dir = "Repos/"+name
    os.system("cp src/sonar-project.properties Repos/" + name) 
    subprocess.check_output(["sonar-scanner", "-Dsonar.projectKey=" + PROJECT_NAME, "-Dsonar.sources=.", "-Dsonar.host.url=" + "http://localhost:9000", "-Dsonar.token=" + TOKEN], cwd=work_dir)
    time.sleep(120)
    sonar_fetch.fetch_data("http://localhost:9000", name)


def metrix(name):
    """
    Processes complexity calculations from metrix++
        Parameters:
            name (string): the repository name
    """
    work_dir = "Repos/"+name
    path_chain = str(subprocess.check_output(["find", "-name", "*.c*"], cwd=work_dir))[2:-1].split("\\n")[:-1] #currently not grabbing header files
    to_use = []
    valid_extensions = {".c", ".cpp", ".cc", ".h", ".java"}
    for path in path_chain:
        if "." + path.split(".")[-1] in valid_extensions:
            to_use.append(path)
    
    path_chain = str(subprocess.check_output(["find", "-name", "*.h"], cwd=work_dir))[2:-1].split("\\n")[:-1] #currently not grabbing header files
    valid_extensions = {".c", ".cpp", ".cc", ".h", ".java"}
    for path in path_chain:
        if "." + path.split(".")[-1] in valid_extensions:
            to_use.append(path)
    
    path_chain = str(subprocess.check_output(["find", "-name", "*.java"], cwd=work_dir))[2:-1].split("\\n")[:-1] #currently not grabbing header files
    valid_extensions = {".c", ".cpp", ".cc", ".h", ".java"}
    for path in path_chain:
        if "." + path.split(".")[-1] in valid_extensions:
            to_use.append(path)
        
    if len(to_use) > 100:
        counter = 0
        subprocess.check_output(["python3", "../../../metrixplusplus/metrix++.py", "collect", "--std.code.lines.code", "--std.code.complexity.cyclomatic"],cwd=work_dir)
        while counter - 100 <= len(to_use):
            final_out = subprocess.check_output(["python3", "../../../metrixplusplus/metrix++.py", "view", "--", *to_use[counter:counter+100]], cwd=work_dir).decode()
            with open("Data/metrixpp_"+name+str(counter/100)+".txt", "w+") as f:
                f.write(final_out)
            counter+=100
    elif len(to_use) == 0:
        return
    else:
        subprocess.check_output(["python3", "../../../metrixplusplus/metrix++.py", "collect", "--std.code.lines.code", "--std.code.complexity.cyclomatic"],cwd=work_dir)
        final_out = subprocess.check_output(["python3", "../../../metrixplusplus/metrix++.py", "view", "--", *to_use], cwd=work_dir).decode()
        with open("Data/metrixpp_"+name+".txt", "w+") as f:
            f.write(final_out)

def main():
    # for project in ["tomcat","systemd","django","FFmpeg","linux","struts","httpd"]:
    for project in ["chromium_c1","chromium_c2"]:
        complexity(project)
        # metrix(project)


if __name__ == '__main__':
    main()
