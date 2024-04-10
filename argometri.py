import argparse
from auth import auth



def main():
    parser = argparse.ArgumentParser(description="Argometrics client")
    parser.add_argument("-d","--domain",help="argocd base url")
    parser.add_argument("-u","--username",help="username for authentication")
    parser.add_argument("-p","--password",help="password for authentication")
    # parser.add_argument('--weeks', nargs='?', type=int, help='Number of weeks back to count from (optional)')
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