# Copyright 2020 - Splunk
# Written by Sam Hays (ghays at splunk com)
# 
# This script will load playbooks into a Phantom instance from
# the file system.

import argparse
import getpass
import requests
import json
import urllib3
from uuid import uuid4


VERSION = 1.0


def get_arguments():
    parser = argparse.ArgumentParser(description="Create containers in Phantom.")
    parser.add_argument(
        '-e', '--endpoint',
        help="The Phantom host (for REST requests e.g. 'https://phantom.host.com')",
        required=True,
        type=str)
    parser.add_argument(
        '-f', '--file',
        help="A file containing JSON file of artifacts.",
        type=str,
        required=False)
    parser.add_argument(
        '-k', '--usekey',
        help="Use API key instead of username/password",
        action='store_true')
    parser.add_argument(
        '-l', '--label',
        help="The label for the container. Must be a registered label within the system.",
        default="events",
        type=str)
    parser.add_argument(
        '-r', '--runautomation',
        help="Tells the API to run automation upon ingestion of the container. (defaults True)",
        action='store_true')
    parser.add_argument(
        '-c', '--numbercontainers',
        help="How many containers to create?",
        type=int,
        default=1)
    parser.add_argument(
        '-n', '--name',
        help="Name of the container",
        type=str,
        default="container_generator")
    parser.add_argument(
        '-d', '--debug',
        help="Turns on some debug printing...",
        action="store_true")
    return parser.parse_args()


def get_credentials(args):
    if args.usekey:
        api_key = getpass.getpass("key will not echo: ")
        return ('API', 'ph-auth-token', api_key)
    else:
        username = input("username: ")
        password = getpass.getpass("password (will not echo): ")
        return ('BASIC', username, password)


def load_file(cef_file):
    with open(cef_file) as f:
        return json.loads(f.read())

def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    args = get_arguments()

    body = {
        "label": args.label,
        "name": args.name,
        "run_automation": args.runautomation
    }

    if args.debug:
        print(f"DEBUG: args = {args}")

    try:
        if args.file:
            cef = load_file(args.file)
            if isinstance(cef, list):
                body["artifacts"] = cef
            else:
                print(f"Error: CEF file must be list of objects.")
                return

        creds = get_credentials(args)

        if args.debug:
            print(f"DEBUG: generated body for post = {json.dumps(body, indent=4)}")
        
        c = args.numbercontainers if args.numbercontainers > 1 else 1
        for _ in range(c):
            
            # ensure unique sdi's in each container
            body["source_data_identifier"] = str(uuid4()),
            
            if creds[0] == 'BASIC':
                if args.debug:
                    print(f"DEBUG: Posting with API key")
                resp = requests.post(
                    url=args.endpoint + "/rest/container",
                    json=body,
                    auth=creds[1:],
                    verify=False)
            else:
                if args.debug:
                    print(f"DEBUG: Posting with Username/Password")
                resp = requests.post(
                    url=args.endpoint + "/rest/container",
                    json=body,
                    headers={creds[1]: creds[2]},
                    verify=False)
        
        if args.debug:
            print(f"DEBUG: Response from API: {resp.text}")
        if resp.status_code == 200:
            print(f"Success: Container(s) created.")
        else:
            print(f"Failure: Container not created. Resp: {resp.text}")

    except json.decoder.JSONDecodeError:
        print(f"Error: Unable to decode CEF file as JSON.")
    
    except Exception as e:
        print(f"Error: An exception has occurred. Error: {e}")


if __name__ == "__main__":
    main()
