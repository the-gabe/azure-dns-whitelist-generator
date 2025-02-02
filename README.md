# Azure DNS domain whitelist generator

With the launch of [Azure DNS Security Policy](https://learn.microsoft.com/en-us/azure/dns/dns-security-policy), many individuals such as myself want to eliminate the risk of DNS based C2 fully with this new Azure service.

The expectation (and only real scenario where there is a point in using this script and the former Azure resource) is that you have an Azure Firewall already configured, along with properly configured Network Security Groups, and now you want to close off any potential for DNS based data exfiltration.

With this whitelist, you will be able to ensure that all your Private DNS Zones used by Private Links and Azure resources you have created with platform provided subdomains are resolvable by default, as you can just import the produced file into a DNS Domain List resource. As of writing you will need to split the list across 2 DNS domain lists, as there is a limit of 100 domains per DNS Domain List resource.

# Not in scope of this script but you may wish to add this...

Beware: Allowing the usage of the Graph API in your environment opens up a [well known](https://x.com/vxunderground/status/1429867158075498506) and commonly used [C2](https://github.com/boku7/azureOutlookC2) data exfiltration vector, known to be used by [state sponsored](https://www.elastic.co/security-labs/siestagraph-new-implant-uncovered-in-asean-member-foreign-ministry) [threat actors](https://www.elastic.co/security-labs/update-to-the-REF2924-intrusion-set-and-related-campaigns). Looking right at you North Korea :)

Someone should probably pitch to Microsoft having private per-application Graph API endpoints which strictly control what Graph API requests may be issued. The alternative until such a time, is building a HTTPS proxy which does TLS MITM, which has traffic rules to restrict what Graph API requests/traffic is allowed. You could probably do that with Squid proxy.

## Graph API:

This script will not generate domains for the Graph API. Domains are below.

`graph.microsoft.com`

`ags.privatelink.msidentity.com`

`www.tm.prd.ags.trafficmanager.net`

`www.tm.prd.ags.akadns.net`


## MSAL Authority URL:

This script will not generate domains for the MSAL Authority URL endpoint (The thing you use for OpenID Connect, SAML and so on), you definitely need this if you are using the Graph API for Entra ID single sign-on by end users. Domains are below.

`login.microsoftonline.com`

`login.mso.msidentity.com`

`ak.privatelink.msidentity.com`

`www.tm.ak.prd.aadg.trafficmanager.net`

`www.tm.ak.prd.aadg.akadns.net`

# "I have other Private DNS Zones which I named myself"

Ok, did you name them with the `.internal` suffix? Because `.internal` is what you should be using for your Azure Private DNS Zones which do not fall into the list used by Private Links and the Azure platform as a whole. ICANN as part of [ICANN Resolution 2024.07.29.06](https://www.icann.org/en/board-activities-and-meetings/materials/approved-resolutions-special-meeting-of-the-icann-board-29-07-2024-en#section2.a) reserved `.internal` specifically for intranet and virtual network usage such as this. Do things properly, and then you only need to allow `.internal` in you DNS domain list. Otherwise, have fun! :) Because if you don't follow this, you technically open up your infrastructure to malicious DNS based exfiltration because on paper, if you don't use `.internal` any suffix you use is pretty much up for grabs for anyone to register as a TLD at ICANN. Even if you own the domain you are using for your internal DNS resolution with Azure Private DNS, why introduce additional risk for no reason? If you are doing this, ask yourself if what you are doing there is seriously needed to run your infrastructure or not.

# Disclaimer

This repository is not endorsed by my employer, organisation, clients, anyone, anything or any entity in any way, shape or form. This is released on the internet as a convenience only. Usage of this script may cause toast to sporadically appear inside of your computer case. No refunds, no "the toast has jammed my computer's fan" support here.
