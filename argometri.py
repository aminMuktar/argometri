import argparse
from auth import auth



def main():
    parser = argparse.ArgumentParser(description="Argometrics client")
    parser.add_argument("-d","--domain",required=True,help="argocd base url")
    parser.add_argument("-u","--username",required=True,help="username for authentication")
    parser.add_argument("-p","--password",required=True,help="password for authentication")
    args = parser.parse_args()

    if args.username and not args.password:
        parser.error("password is required when username is provided")
    
    if args.username and args.password:
        client = auth.create_argocd_client(base_url=args.domain,username=args.username,password=args.password)
    else:
        client = auth.create_argocd_client(base_url=args.domain)
    print(client.list_applications())

if __name__ == "__main__":
    main()