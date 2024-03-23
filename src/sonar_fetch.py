"""
Manages the reading and usage of the Sonar API, currently partially hardcoded in terms of the login
"""

import requests

PROJECT_NAME = "test"



def fetch_data(uri, project_name):
    """
    Access the API for SonarQube
        Parameters:
            uri (string): the host information of the SonarQube instance
            project_name (string): the name to use when writing the retrieved data to a file
    """
    payload = {
        "login": "admin",
        "password": "password"
    }
    with requests.Session() as s:
        p = s.post(uri + "/api/authentication/login", data=payload)
        page = 1
        while True:
            url = uri + "/api/measures/component_tree?additionalFields=metrics&ps=500&asc=false&metricSort=complexity&s=metric&metricSortFilter=withMeasuresOnly&p="+str(page)+"&component=" + PROJECT_NAME + "&metricKeys=ncloc,complexity&strategy=leaves"
            response = s.get(url)
            data = response.json()
            if len(data['components']) == 0:
                break
            with open("Data/sonar_"+project_name+"_"+"page"+str(page)+".json", 'a+') as f:    
                f.write(str(data['components']) + "\n")
            page += 1 
