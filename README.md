DNSChat
=======

In many cases DNS works even when behind a paywalled internet connection. Examples include airplane wifi, airports, coffee shops. 
  
This is a collection of small server/client scripts to send e-mails from behind a paywall solely via DNS queries. 

- Note that you need to configure your hosting provider's DNS server to forward the DNS requests to your host. Depending on your hosting provider, this might not be possible.
- Note that the security is very primitive. The code just checks for a secret in the hostname. Anyone with access to the network can sniff this secret.
- The code adds a salt to every query to ensure the DNS response has not been cached.

This software is licensed under the GPL v3. See LICENSE.md for details.

Author: Hanno Rein <hanno@hanno-rein.de>

