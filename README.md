# Network-Troubleshooting
Scripts that I've developed to help with network diagnostics and troubleshooting.

# Customer-Circuit-IP-Checker.py
Script runs through a pre-defined dictionary that consists of customer names, contact info and IP addresses and attempts to ping each IP. If the ping attempt fails it will send an automated email to the administrator that the ping has failed, along with the customer name, contact information and the IPs that failed. Only one email will be sent per customer even if the customer has multiple ips that failed to ping.

# Reverse-DNS-Resolver.py
Script parses all of the IPs out of a string. Then iterates through each IP to find all of the FQDNs for the corresponding IP.

# ping-sweep.py
Script parses all of the IPs out a string. Then attempts to ping each IP. The script will print out whether the host was reachable or not.
