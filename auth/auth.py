import requests
import json
import os
from datetime import date,datetime,timedelta
requests.packages.urllib3.disable_warnings()


class ArgoCDAuth:
    def __init__(self, base_url,token=None,username=None,weeks=None, password=None,optimized_apps=None):
        self.base_url=base_url
        self.token=token
        self.username=username
        self.weeks=weeks
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
            with open(file_path,"r") as file:
                to_be_optimized=json.load(file)
            items=to_be_optimized.get("items",[])
            target_date=self.weeks_back_from_current_date(self.weeks)
            for item in items:
                metadata=item.get("metadata",{})
                spec=item.get("spec",{})
                source=spec.get("source",{})
                directory=source.get("directory",{})
                jsonnet=directory.get("jsonnet",{})
                extVars=jsonnet.get("extVars",[])
                status=item.get("status",{})
                histories=status.get("history",[])
                name=metadata.get("name")
                destination=spec.get("destination",{})
                server=destination.get("server")
                namespace=destination.get("namespace")
                count=0
                for history in histories:
                    deployed_at=history.get("deployedAt")
                    str_to_date=datetime.strptime(deployed_at,"%Y-%m-%dT%H:%M:%SZ")
                    target_to_date=datetime.strptime(target_date,"%Y-%m-%d").date()
                    deployed_at_date=str_to_date.date()
                    if deployed_at_date >= target_to_date:
                        count+=1
                squad=""
                for vars in extVars:
                    squad=vars.get("value")
                    # print(squad)
                optimized_app={
                    "NameOfApplication": name,
                    "Server": server,
                    "Namespace": namespace,
                    "NumberOfDeployment": count,
                    "Squad":squad
                }
                self.optimized_apps.append(optimized_app)
            with open(f"{folder_path}/optimized_argocd_apps.json","w") as output_file:
                json.dump(self.optimized_apps,output_file,indent=2)
            print("Optimized JSON data saved to optimized_argocd_apps.json")
        else:
            print(f"Request failed with status code {response.status_code}")
            return None

    def weeks_back_from_current_date(self,weeks):
        current_date=datetime.now()
        weeks_delta=timedelta(weeks=weeks)
        target_date=current_date - weeks_delta
        return target_date.strftime("%Y-%m-%d")
        
def create_argocd_client(base_url, username=None, password=None, weeks=None):
    if username and password:
        client=ArgoCDAuth(base_url=base_url, username=username, password=password, weeks=weeks)
        return client.list_applications()
    else:
        return ArgoCDAuth(base_url=base_url)



        