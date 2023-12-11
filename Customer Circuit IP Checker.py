import subprocess
import smtplib
import ssl
import sys
import threading
from datetime import date

# Define the customer data dictionary
customer_data = {
    "Customer1 CID# 1234567890": {
        "ips": ["8.8.8.6","8.8.8.8"],
        "contact_info": "Name: Jim Test \nEmail: Jim@test.com \nPhone: 519-270-8888",
    },
    "Customer2": {
        "ips": ["8.8.8.7"],
        "contact_info": "customer2@example.com",
    },
    # Add more customers if needed
}

# Function to send email
def send_email(customer_name, contact_info, failed_ips):
    # Configure the email settings
    smtp_server = "smtp.gmail.com"
    sender_email = "" #who the email is coming from
    receiver_email = "" #who the email should be sent too.
    password = "" #add email password

    subj = f"Subject: IP Ping Failure - {customer_name}"
    message_text = f"{customer_name}\n{contact_info}\nIP(s): {', '.join(failed_ips)}"

    email = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % (sender_email, receiver_email, subj, date, message_text)
    #print(email)
    #sys.exit()  # Test code only without sending the email message.

    # Create the email message

    # Send the email
    try:  # try to connect to mail server via ssl.
        server = smtplib.SMTP(smtp_server, 587)
        server.starttls(context=ssl.create_default_context())
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, email)  # from, to, email
        server.quit()
        server.close()
        print('Email was sent successfully.')
    except Exception as e:
        print("Can't send the email because: %s" % e)


def ping(ip):
    # return subprocess.run(["ping", "-c", "2", ip], capture_output=True) #Linux
    return subprocess.run(["ping", "-n", "3", ip], capture_output=True)  # Windows


def check_ip(customer_name, contact_info, ip, failed_ips):
    result = ping(ip)
    if result.returncode != 0:
        # Retry for failed pings just to make sure.
        max_retries = 1
        for retry in range(max_retries):
            print(f"Retrying... Attempt {retry + 1} for {ip}")
            result = ping(ip)
            if result.returncode == 0:
                break
            elif retry == max_retries - 1:
                # All retries failed, add the failed IP to the list
                failed_ips.append(ip)


# Loop through the customer data
for customer_name, customer_info in customer_data.items():
    ips = customer_info["ips"]
    contact_info = customer_info["contact_info"]
    failed_ips = []  # List to store the failed IPs

    # Loop through the IP addresses
    for ip in ips:
        # Create a thread for each IP address
        thread = threading.Thread(target=check_ip, args=(customer_name, contact_info, ip, failed_ips))
        thread.start()

    # Wait for all threads to finish
    for thread in threading.enumerate():
        if thread != threading.current_thread():
            thread.join()

    # Send email with all the failed IPs for the customer
    if failed_ips:
        send_email(customer_name, contact_info, failed_ips)
            
