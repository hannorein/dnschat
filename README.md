DNS Chat
=======

In many cases DNS works even when behind a paywalled internet connection. Examples of such networks include those often found in airplanes, airports and coffee shops. 
  
This is a collection of two small server/client scripts to send e-mails from behind a paywall solely via DNS queries. 

- Note that you need to configure your hosting provider's DNS server to forward the DNS requests of a specific (sub)domain to your host. Depending on your hosting provider, this might not be possible.
- Note that the security is very primitive. The current implementation just checks for a secret in the hostname. Anyone with access to the network can sniff this secret.
- No integrety/checksum check whatsoever is performed on the message. Only the number of characters is checked before sending the message.
- The code adds a salt to every query to ensure the DNS response has not been cached.
- Incoming messages can be received via a simple flask server.

This software is licensed under the GPL v3. See LICENSE.md for details.

Author: Hanno Rein <hanno@hanno-rein.de>

