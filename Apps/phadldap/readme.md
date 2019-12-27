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

## Actions
### Add Group Member