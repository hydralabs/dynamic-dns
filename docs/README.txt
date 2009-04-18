===================
Dynamic DNS Updater
===================

== Requirements ==

 * Python 2.5
 * Twisted 8.2
 * dnspython 1.6
 

== Running the Server ==

To run the server use the following command:

  twistd -y ddns.py
  
By default the server will listen on port 8080, though this can be changed
in ddns.py
  
You may want to consult the "twistd" documentation for more options such
as logging and dameonizing the application.

== Using the Updater ==

Updates are handled by simply passing url parameters to the update listener.
The updater takes the following arguments:

 * tsig_id
 * tsig_key
 * zone
 * record
 * ttl
 * dns_server
 * type
 * value

Here is an example where <xxxx> would be substituted by your values:

http://server_ip:8080/update?tsig_id=<name>&tsig_key=<key>
&zone=<zone>&record=&ttl=<ttl>&dns_server=<dns_ip>&type=<type>&value=<address>