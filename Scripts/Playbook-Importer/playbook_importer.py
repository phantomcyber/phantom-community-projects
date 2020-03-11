# Copyright 2020 - Splunk
# Written by Sam Hays (ghays at splunk com)
# 
# This script will load playbooks into a Phantom instance from
# the file system.

import argparse
import base64
import getpass
import glob
import requests
import json
import urllib3

VERSION = 1.0


def get_playbook_list(directory):
    return glob.glob("{}/*.tgz".format(directory))


def get_arguments():
    parser = argparse.ArgumentParser(description="Add playbooks to Phantom.")
    parser.add_argument('-c', '--confirm',
                        help="Confirm each file during import.",
                        action='store_true')
    parser.add_argument('-k', '--usekey',
                        help="Use API key instead of username/password",
                        action='store_true')
    parser.add_argument('-f', '--forceoverwrite',
                        help="If playbook exists, overwrite it",
                        action='store_true')
    parser.add_argument('-e', '--endpoint',
                        help="The Phantom host (for REST requests e.g. 'https://phantom.host.com')",
                        required=True,
                        type=str)
    parser.add_argument('-r', '--repository',
                        help="Phantom repository in which to import (local*)",
                        required=False,
                        default="local")
    parser.add_argument('directory',
                        help="directory with .tgz playbooks",
                        type=str)
    return parser.parse_args()


def get_credentials(args):
    if args.usekey:
        api_key = getpass.getpass("key will not echo: ")
        return ('API', 'ph-auth-token', api_key)
    else:
        username = input("username: ")
        password = getpass.getpass("password (will not echo): ")
        return ('BASIC', username, password)


def import_playbooks(confirm, files, creds, endpoint, repo, force):
    for file in files:
        body = {"scm": repo, "force": force}
        f = open(file, 'rb')
        try:
            if confirm:
                prompt = input("Continue with file: '{}'? [y/N]".format(file))
                if prompt.lower().strip()[0:1] == 'n' or len(prompt) == 0:
                    continue
            encoded = base64.encodebytes(f.read())
            body['playbook'] = str(encoded, 'utf-8')
            if creds[0] == 'BASIC':
                resp = requests.post(url=endpoint + "/rest/import_playbook",
                                     json=body,
                                     auth=creds[1:],
                                     verify=False)
            else:
                resp = requests.post(url=endpoint + "/rest/import_playbook",
                                     json=body,
                                     headers={creds[1]: creds[2]},
                                     verify=False)
            if(resp.status_code == 200):
                print("SUCCESS: file={}, message={}".format(
                    file, json.loads(resp.text)['message']))
            else:
                print("FAILED: file={}, message={}".format(
                    file, json.loads(resp.text)['message']))
        except Exception as e:
            print(str(e))
        finally:
            f.close()


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    args = get_arguments()
    files = get_playbook_list(args.directory)

    if(len(files) == 0):
        print("No files found to import.")
        return(-2)

    creds = get_credentials(args)
    import_playbooks(args.confirm,
                     files,
                     creds,
                     args.endpoint,
                     args.repository,
                     args.forceoverwrite)


if __name__ == '__main__':
    main()