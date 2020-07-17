
# Playbook Importer

## This Script
There may be a circumstance where you want to import many playbooks into a Phantom instance at once. This article will briefly describe the usage of a utility written for and maintained by the Phantom Community to leverage the REST API to do just that.

### A Little Background

Phantom uses git to store all playbooks. There is a default repository for playbooks you create within the platform called local but you can create others in the Administration -> Administration Settings -> Source Control section of the UI. When you write a new playbook and go to save it, you will be prompted for the repository in which it will be saved.

![Save Playbook](./.images/save_playbook.png)

The Phantom UI allows you to upload playbooks into any of these repositories, but only one at a time. Luckily, Phantom includes a REST API (https://docs.splunk.com/Documentation/Phantom/4.8/PlatformAPI/Using) that can load playbooks into any configure repository programmatically. The Playbook Importer utility leverages this API to load playbooks in bulk.

### Why?

There is a customer whose Development network is air-gapped from their Production network, and the Production network has no Internet connectivity whatsoever nor any shared resources with their Development network, so they cannot share a repository between the two. What they can do, however, is copy their playbooks over using media (e.g. USB drives). The problem is that they have hundreds of playbooks and do not want to manually upload every single playbook, every single release cycle. Having heard about this, it seemed like having a utility our community could use in their own cases made sense, so I wrote one. Now our community can use it and study the code to learn from it, and of course, contribute to it to make it better.

### The Utility

This utility is a small Python script that uses the `rest/import_playbook` API endpoint to load playbooks. 

At the time of this writing, there are several parameters that can be used (with more to come, certainly). An execution with the `-h` parameter looks like this:
```
ghays@phcom Playbook-Importer % python3 ./playbook_importer.py -h
usage: playbook_importer.py [-h] [-c] [-k] [-f] -e ENDPOINT [-r REPOSITORY]
                            directory

Add playbooks to Phantom.

positional arguments:
  directory             directory with .tgz playbooks

optional arguments:
  -h, --help            show this help message and exit
  -c, --confirm         Confirm each file during import.
  -k, --usekey          Use API key instead of username/password
  -f, --forceoverwrite  If playbook exists, overwrite it
  -e ENDPOINT, --endpoint ENDPOINT
                        The Phantom host (for REST requests e.g.
                        'https://phantom.host.com')
  -r REPOSITORY, --repository REPOSITORY
                        Phantom repository in which to import (local*)
ghays@phcom Playbook-Importer %
```
 
Most of the above is self-explanatory but I'll give some examples here to further clarify usage. I will be operating on a playbook with the name: `Playbook_Importer_Test.tgz` as can be seen here:

```
ghays@phcom Playbook-Importer % ls -l
total 32
-rw-r--r--@ 1 ghays  staff  1832 Mar 17 10:58 Playbook_Importer_Test.tgz
-rw-r--r--  1 ghays  staff  5386 Mar 17 11:29 README.md
-rw-r--r--  1 ghays  staff  3777 Mar 11 16:25 playbook_importer.py
ghays@phcom Playbook-Importer % 
```

Using the parameters `-c -e https://ph48.splunk.lab .` I am doing the following:
1. Specifying I want to confirm each playbook to be loaded. (`-c`)
2. Specify the endpoint of Phantom in my lab (`-e https://ph48.splunk.lab`)
3. Specify the to load tgz files from the local directory (`.`)


Then the program will prompt me as it iterates through the files:


```
ghays@phcom Playbook-Importer % python3 playbook_importer.py -c -e https://ph48.splunk.lab . 
username: admin
password (will not echo): 
Continue with file: './Playbook_Importer_Test.tgz'? [y/N]y
SUCCESS: file=./Playbook_Importer_Test.tgz, message=Playbook "Playbook_Importer_Test" imported
ghays@phcom Playbook-Importer % 
```


Now we see the Playbook was loaded:


![local repo playbook](./.images/local_playbook.png)

If I try the same command again, it will fail because the playbook already exists:

```
ghays@phcom Playbook-Importer % python3 playbook_importer.py -c -e https://ph48.splunk.lab .
username: admin
password (will not echo): 
Continue with file: './Playbook_Importer_Test.tgz'? [y/N]y
FAILED: file=./Playbook_Importer_Test.tgz, message=Playbook "Playbook_Importer_Test.py" already exists in repo "local". Use force to overwrite.
ghays@phcom Playbook-Importer % 
```

If we are uploading a newer version, we can specify the -f parameter to overwrite the one in the repository.

## Authentication Types

You can use ether username/password (as in the screenshots above) to log in or you can use an API key. If you do not specify any authentication-related parameters, you will be prompted for username and password. However you can specify `-k` to use an Automation user's key. For example:

```
ghays@phcom Playbook-Importer % python3 ./playbook_importer.py -f -c -e https://ph48.splunk.lab -k .
key will not echo: 
Continue with file: './Playbook_Importer_Test.tgz'? [y/N]y
SUCCESS: file=./Playbook_Importer_Test.tgz, message=Playbook "Playbook_Importer_Test" imported
ghays@phcom Playbook-Importer %
```

In the above example, I specified `-k` and instead of a username and password, I was prompted for the API key. The API user must have 'Automation Engineer' Roles associated to be able to upload playbooks.

## Other Repos

If you've set up another repository that will be the target for the uploads, you can specify that as well. In my lab, I have a Source Control configuration pointing to Github called "scm_test":

![scm_test repo](./.images/source_control.png)

I can write to this repository by specifying the `-r <name>` parameter as in the example below.


```
ghays@phcom Playbook-Importer % python3 ./playbook_importer.py -r scm_test -e https://ph48.splunk.lab -k .
key will not echo: 
SUCCESS: file=./Playbook_Importer_Test.tgz, message=Playbook "Playbook_Importer_Test" imported
ghays@phcom Playbook-Importer %
```


Note I specified the name as it appears in the UI. In the screenshot below you can see that the playbook now exists in both repositories.

![both repos](./.images/two_repos.png)

I hope you find this helpful!

-Sam Hays