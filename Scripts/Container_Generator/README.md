
# Container Generator

## This Script
This script was created as response to a request by a Phantom Community member looking for a more versatile way to create containers for testing.

### The Utility

This utility is a small Python script that uses the `rest/container` API endpoint to as well as optional "artifact" files to generate containers and associated artifacts.

At the time of this writing, there are several parameters that can be used (with more to come, certainly). An execution with the `-h` parameter looks like this:

```
usage: container_generator.py [-h] -e ENDPOINT [-f FILE] [-k] [-l LABEL] [-r]
                              [-c NUMBERCONTAINERS] [-n NAME] [-d]

Create containers in Phantom.

optional arguments:
  -h, --help            show this help message and exit
  -e ENDPOINT, --endpoint ENDPOINT
                        The Phantom host (for REST requests e.g.
                        'https://phantom.host.com')
  -f FILE, --file FILE  A file containing JSON file of artifacts.
  -k, --usekey          Use API key instead of username/password
  -l LABEL, --label LABEL
                        The label for the container. Must be a registered
                        label within the system.
  -r, --runautomation   Tells the API to run automation upon ingestion of the
                        container. (defaults True)
  -c NUMBERCONTAINERS, --numbercontainers NUMBERCONTAINERS
                        How many containers to create?
  -n NAME, --name NAME  Name of the container
  -d, --debug           Turns on some debug printing...
```
 
Most of the above is self-explanatory but I'll give some examples here to further clarify usage.

## Artifact Files

Consider the following file `EXAMPLE_JSON_1.json`:
```
[
  {
    "name": "some artifact",
      "cef": {
        "sourceDnsDomain": "www.splunk.com"
      }
  }
]
```

Note that the outermost structure is an array/list (`[]`) which is required for these. Each element of the list is a json object. These files should align to the `artifacts` object detailed here: https://docs.splunk.com/Documentation/Phantom/4.9/PlatformAPI/RESTContainers

Yet another example where multiple artifacts can be added:
```
[
  {
    "name": "some artifact",
    "cef": {
      "sourceDnsDomain": "www.splunk.com",
      "destinationDnsDomain": "www.phantom.us"
    }
  },
  {
    "name": "a second artifact"
  },
  {
    "name": "A third artifact with custom fields",
    "cef": {
      "test_field_1": 1,
      "test_field_2": [1, 2, 3]
    }
  }
]
```
Again, in the above you can see the outermost block is a list and contains an array of artifact objects.

Note: Artifact files do not have to be used, but omitting them will mean that the created containers will not have artifacts.

## Examples

### With no optional parameters:
```
% python3 container_generator.py -e https://192.168.3.141                                           
username: admin
password (will not echo): 
Success: Container(s) created.
```

Specifying a file with artifacts:
```
% python3 container_generator.py -e https://192.168.3.141 -f EXAMPLE_JSON_1.json 
username: admin
password (will not echo): 
Success: Container(s) created.
```

Specifying more than 1 container. This will create 10 containers:
```
% python3 container_generator.py -e https://192.168.3.141 -f EXAMPLE_JSON_1.json -c 10
username: admin
password (will not echo): 
Success: Container(s) created.
```


## Authentication Types

You can use ether username/password (as in the screenshots above) to log in or you can use an API key. If you do not specify any authentication-related parameters, you will be prompted for username and password. However you can specify `-k` to use an Automation user's key. For example:

```
 % python3 container_generator.py -e https://192.168.3.141 -f EXAMPLE_JSON_1.json  -k   
key will not echo: 
Success: Container(s) created.
```

In the above example, I specified `-k` and instead of a username and password, I was prompted for the API key. 

