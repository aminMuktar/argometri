import argparse
from datetime import date
import json
import os

from matplotlib import pyplot as plt
from auth import auth

def generate_piechart():
    current_date= date.today().isoformat()
    folder_path=os.path.join("data",current_date)
    file_path= os.path.join(folder_path,"optimized_argocd_apps.json")
    with open(file_path,"r") as file:
        data=json.load(file)
    squad_deployments={}
    
    for app in data:
        squad=app.get("Squad")
        deployments=app.get("NumberOfDeployment")

        if squad in squad_deployments:
            squad_deployments[squad]+=deployments
        else:
            squad_deployments[squad]=deployments

    squad_names=list(squad_deployments.keys())
    deployment_counts=list(squad_deployments.values())


    plt.figure(figsize=(12,12))
    plt.pie(deployment_counts,labels=squad_names,autopct='%1.1f%%',startangle=140)
    plt.title('Number of Deployments by Squad')
    return plt.savefig(f'{folder_path}/deployment_pie_chart_kality.png',bbox_inches='tight')

    # plt.show()

def generate_horizontal_chart():
    current_date= date.today().isoformat()
    folder_path=os.path.join("data",current_date)
    file_path= os.path.join(folder_path,"optimized_argocd_apps.json")
    with open(file_path,"r") as file:
        data=json.load(file)
    filtered_data=[app for app in data if app.get("NumberOfDeployment")>0]
    sorted_data=sorted(filtered_data,key=lambda app: app.get("NumberOfDeployment"), reverse=True)
    squad_names = [app.get("Squad") for app in sorted_data]
    app_names=[app.get("NameOfApplication").replace('-',' ').title() for app in sorted_data]
    num_deployments = [app.get("NumberOfDeployment") for app in sorted_data]

    plt.figure(figsize=(10,6))
    plt.barh([f'{app}' for squad,app in zip(squad_names,app_names)],num_deployments)
    plt.xlabel("Number of deployments")
    plt.title("Number of deployments by application (Descending order)")
    
    return plt.savefig(f'{folder_path}/deployment_chart.png',bbox_inches='tight')


def main():
    parser = argparse.ArgumentParser(description="Argometrics client")
    parser.add_argument("-d","--domain",help="argocd base url")
    parser.add_argument("-u","--username",help="username for authentication")
    parser.add_argument("-p","--password",help="password for authentication")
    parser.add_argument('-w','--weeks', nargs='?', type=int, help='Number of weeks back to count from (optional)')
    parser.add_argument("-pc","--piechart",action='store_true',help="generate pie chart")
    parser.add_argument("-hc","--horizontal",action='store_true',help="generate horizontal chart")
    args = parser.parse_args()

    

    if args.username and not args.password:
        parser.error("password is required when username is provided")
    
    if args.username and args.password:
        auth.create_argocd_client(base_url=args.domain,username=args.username,password=args.password, weeks=args.weeks)

    if args.piechart:
        generate_piechart()

    if args.horizontal:
        generate_horizontal_chart()
    

    
    
    # print(client.weeks_back_from_current_date(args.weeks))

if __name__ == "__main__":
    main()