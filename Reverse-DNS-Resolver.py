import re
import dns.resolver
import tkinter
import tkinter.simpledialog

#Build a list of IPs to resolve PTR.
#Take in a string, regex out the IPs and then resolve PTR.

'''
Example:
Monitoring Missing for 192.168.36.2/32    
Monitoring Missing for 192.168.42.11/32
''' 

pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'


def get_ips():
    string = tkinter.simpledialog.askstring('Input IPs to resolve:','Input IPs to resolve:')
    if string == '' or type(string) == type(None):
        #Cancel Button was clicked.
        return {}
    else:
        #Check for valid IPs.
        matches = re.findall(pattern, string)
        
        #Build a list of IPs to ping.
        ips = {i: ip for i, ip in enumerate(matches)}

        return ips

ips = get_ips()
#print(ips)

while len(ips) == 0:
    tkinter.messagebox.showinfo('Try Again','No vailid IPs were entered. Please try again.')
    ips = get_ips()

for ip in ips:
    try:
        n = dns.resolver.resolve_address(ipaddr=ips[ip])
        print(ips[ip] + ':')
        for ptr in n.response.answer[0].items:
            print(ptr.target)
        print('\n')
    except Exception:
        print(f'Error resolving PTR for IP: {ips[ip]}\n')            
