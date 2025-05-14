from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import socket 


################################################
# util 1.
#sends mail when component changes (not used now)
#################################################
def send_email(to_email, subject, html_content):
    message = Mail(
        from_email='nikoschairop@gmail.com                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      ',
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        return response.status_code
    except Exception as e:
        return str(e)
    

def get_local_ip():
    try:
        # Create a socket connection to Google's DNS server
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        # Get the local IP address from this connection
        local_ip = s.getsockname()[0]
        s.close()
        # return local_ip.split('.')[-1]
        return local_ip
    except:
        return "Could not determine local IP"