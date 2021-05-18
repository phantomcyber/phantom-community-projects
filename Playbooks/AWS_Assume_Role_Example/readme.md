## AWS Assume Role Example Playbooks

This playbook is an example of how the AWS STS app can be used to assume a role and generate a temporary credential to use another AWS service, potentially in another AWS account.

### Prerequisites

1. You will need an AWS environment with at least an access key that has permission to assume a role and a role that can be assumed. The AWS Knowledge Center has a nice tutorial that walks through creation of all the necessary resources to demonstrate the assumeRole capability using the AWS command line tool: https://aws.amazon.com/premiumsupport/knowledge-center/iam-assume-role-cli/

### How it works?

Lets consider an example organization that has a security account that monitors a set of other AWS accounts (we will call those the monitored accounts). The security account should have an access key that is used across all the AWS assets in Phantom, including an AWS STS asset. In order for the Phantom actions to run in the monitored accounts, each action needs to run with temporary access keys created by the "assume role" action in the STS app. Each execution of "assume role" requires a role ARN which is the identifier for a role in one of the monitored accounts. This playbook relies on a custom list that has a single column of role ARNs. The "assume role" action will be run once per row in that custom list, then the generated credentials will be passed to the EC2 app to run the "describe instance" action once per monitored account. Each app that supports usage of an assumed role has the **credentials** parameter in each of its actions, which is how the generated token is passed from the "assume role" output to the app that will take action in the monitored account.

If more granularity is needed to only target specific accounts, other metadata about the accounts could also be stored in the custom list and used to filter down to only certain role ARNs that match whatever criteria are needed.

### How to install it?

1. Download the playbook tgz (no need to untar)
2. Log in to Phantom
3. Main Menu -> Playbooks
4. Click the "import" button.
5. Select the downloaded tgz
6. Select the repo (probably "Local", unless you've setup an external git repo)
7. Click "import."

### How to extend it?

The same generated access key can be used repeatedly for any number of AWS actions, as long as that usage takes place within the **role_session_duration**, which is the number of seconds until the generated access key expires. S3, Lambda, and EC2 are currently (May 2021) supported for usage of an assumed role through the **credentials** field. Updates are in the works to extend the usage of an assumed role to all of the other AWS apps.
