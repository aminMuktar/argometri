import requests
import json
import os
from datetime import date,datetime,timedelta
requests.packages.urllib3.disable_warnings()


class ArgoCDAuth:
    def __init__(self, base_url,token=None,username=None, password=None,optimized_apps=None):
        self.base_url=base_url
        self.token=token
        self.username=username
        self.password=password
        if optimized_apps is None:
            self.optimized_apps=[]
        else:
            self.optimized_apps=optimized_apps

        if self.token:
            self.headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            }
        elif self.username and self.password:
            self.authenticate()
        else:
            raise ValueError("Either token or username/password must be provided.")
        
    def authenticate(self):
        response = requests.post(f'{self.base_url}/api/v1/session',json={'username':self.username,'password':self.password}, verify=False)
        self.token=response.json().get('token')
        if not self.token:
            raise ValueError("failed to authenticate. Invalid username or password")
        self.headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
                }

    def list_applications(self):
        response = requests.get(f'{self.base_url}/api/v1/applications',headers=self.headers, verify=False)
        current_date= date.today().isoformat()
        folder_path=os.path.join("data",current_date)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        file_path= os.path.join(folder_path,"argocd_apps.json")
        if response.status_code == 200:
            data = response.json()
            with open(file_path,"w") as file:
                json.dump(data,file)
        else:
            print(f"Request failed with status code {response.status_code}")
            return None
    def weeks_back_from_current_date(self,weeks):
        current_date=datetime.now()
        weeks_delta=timedelta(weeks=weeks)
        target_date=current_date - weeks_delta
        return target_date.strftime("%Y-%m-%d")
        
def create_argocd_client(base_url, username=None, password=None):
    if username and password:
        return ArgoCDAuth(base_url=base_url, username=username, password=password)
    else:
        return ArgoCDAuth(base_url=base_url)



        