## COVID-19 IOC Playbook

This playbook was written as a companion to [TA-covidiocs](https://github.com/splunk/ta-covidiocs), which is a free Splunk TA designed download IOCs related to COVID related atttacks. 

This playbook is modular in design and can be incorporated into most existing playbooks as a subplaybook.

### Prerequisites

1. This project assumes there is a Splunk instance to which Phantom can conneect **and** that Splunk instance has [TA-covidiocs](https://github.com/splunk/ta-covidiocs) installed and properly configured.

2. This project assumes that Phantom has the Splunk app installed. A free, community edition of phantom can be downloaded [here](https://www.splunk.com/en_us/software/splunk-security-orchestration-and-automation.html).

### How it works?

The playbook will search for the existence of event data in the lookups provided by the TA's. It currently pulls event data from the following artifact CEF fields:

- requestURL
- destinationDNSDomain
- fileHashMd5
- sourceAddress

If matches are found the playbook will add the matched indicators to HUD Cards by category (URLs, Hashes, IPs, Domains). Additionally, an artifact field "covid_related = yes" will be added to the artifact from where the indicator came. The artifact field will allow upstream playbooks to easily discern whether the event contains COVID related malicious indicators by searching for artifacts with **artifact:*.cef.codid_related = yes**. 

### How to install it?

1. Download the playbook tgz (no need to untar)
2. Log in to Phantom
3. Main Menu -> Playbooks
4. Click the "import" button.
5. Select the downloaded tgz
6. Select the repo (probably "Local", unless you've setup an external git repo)
7. Click "import."

### How to extend it?

If you need searches performed for more artifact CEF fields, add a new track for that CEF field. You can use the tracks for the existing CEF fields as templates.