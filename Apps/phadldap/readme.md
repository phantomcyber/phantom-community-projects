# AD LDAP
## Community App Project #1

First:  
My thanks to everyone who is actively contributing to the Phantom community. Doubly-so for those of you working on Apps in our GitHub repo and in our Slack channel.

Second:  
This app serves a few purposes. The primary is that I wanted additional features available for LDAP. The second is that I thought some of the hackers in the community might want to dig into a project "owned" by us - and finally, for folks just developing their dev chops, a place to learn and grow.

Third:  
This page is intended to serve as a _living_ document for this app with plently of use-cases, examples, and technical information. Please feel free to contribute!


## The Documentation
- [App Information](#app-information)
- [App Configuration](#app-configuration)
- [Actions](#actions)
    - [Add group member](#add-group-member)
    - [Remove group member](#remove-group-member)
    - [Get Attribute](#get-attribute)
    - [Set Attribute](#set-attribute)
    - [Disable Account](#disable-account)
    - [Enable Account](#enable-account)
    - [Unlock Account](#unlock-account)
    - [Reset Password](#reset-password)
    - [Move Object](#move-object)
    - [Query](#query)

## App Information
This LDAP application utilizes the [LDAP3](https://ldap3.readthedocs.io/) library for Python. This was chosen, in part, due to the pythonic design of the library and the quality of the documentation.

The AD LDAP app only supports [Simple Binding](https://ldap3.readthedocs.io/bind.html#simple-bind) at this time but other methods (e.g. NTLM) could be added relatively easily. It should be noted that [SSL](https://ldap3.readthedocs.io/ssltls.html) is suppoted and enabled by default, but [TLS](https://ldap3.readthedocs.io/ssltls.html#the-tls-object) (start_tls) has not due to certificate complexity within the configuration page.

If someone in the community requests either of these (or adds them with pull-request), I/we will try and make it happen. However, if neither of those happen - I'll implement NTLM soon, but probably not TLS.

### App Configuration
The configuration for this app is relatively straightforward. Let's looks at each component:

First, you'll need an account with which to Bind and perform actions. If you are only ever going to perform *information gathering* tasks (e.g., getting account attributes) then a standard user account would be fine. However, if you plan on doing things like Unlocking, Resetting Passwords, Moving objects, etc. - then you will need an account with permissions to actually perform these actions.  I would caution you to NOT use a "Domain Administrator" (or higher) account. Instead, delegate the appropriate least-privilege access to a service account with a very strong password... In other words, harden the account.
Obviously this can require more thorough testing than just giving the account Domain Admin privs... but thats why you make the big bucks. :)


Second: If you find yourself NOT using SSL, then you should take a good, hard look at why you're doing that. If you don't use SSL then someone could observe the password crossing over the wire. This is bad. Instead: fix SSL. If you have other binding requirements (other than Basic), raise an Issue on the project, maybe we can get it implemented.

(As an aside: My recommendation as a security professional is to disallow insecure (plaintext AND unsigned binds) if at all possible ([ref](#references): 1, 2, 3))

## Actions
### Add Group Member



# References
1. https://blogs.technet.microsoft.com/russellt/2016/01/13/identifying-clear-text-ldap-binds-to-your-dcs/
2. https://blogs.technet.microsoft.com/askds/2008/04/02/directory-services-debug-logging-primer/
3. https://docs.microsoft.com/en-us/windows/security/threat-protection/security-policy-settings/domain-controller-ldap-server-signing-requirements
