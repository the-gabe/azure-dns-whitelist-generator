# Azure DNS domain whitelist generator

With the launch of [Azure DNS Security Policy](https://learn.microsoft.com/en-us/azure/dns/dns-security-policy), many folks such as myself want to cut off the usage of DNS based C2 fully now with this new Azure service.

The expectation (and only really point of using this script and the former Azure resource) is you have an Azure Firewall already configured, along with properly configured NSGs, and now you want to close off DNS based data exfiltration.

With this whitelist, you will be able to ensure that all your Private DNS Zones used by Private Links are resolvable by default, as you can just import the produced file into a DNS domain list.

# Not in scope of this script but you may wish to add...

Beware: Allowing the usage of the Graph API in your environment opens up a [well known](https://x.com/vxunderground/status/1429867158075498506) and commonly used [C2](https://github.com/boku7/azureOutlookC2) data exfiltration vector, known to be used by [state sponsored](https://www.elastic.co/security-labs/siestagraph-new-implant-uncovered-in-asean-member-foreign-ministry) [threat actors](https://www.elastic.co/security-labs/update-to-the-REF2924-intrusion-set-and-related-campaigns). Looking right at you North Korea :)

Someone should probably pitch to Microsoft having private per-application Graph API endpoints which strictly control what Graph API requests may be issued. Also you could probably do some form of restrictions using TLS inspection with Azure Firewall Premium I guess.

This script will not generate domains for the Graph API and OpenID Connect endpoint used for Entra ID SSO. You need to allow the below in such a scenario:

Graph API:

`graph.microsoft.com`

`ags.privatelink.msidentity.com`

`www.tm.prd.ags.trafficmanager.net`

`www.tm.prd.ags.akadns.net`

OpenID Connect:

`login.microsoftonline.com`

`login.mso.msidentity.com`

`ak.privatelink.msidentity.com`

`www.tm.ak.prd.aadg.trafficmanager.net`

`www.tm.ak.prd.aadg.akadns.net`
