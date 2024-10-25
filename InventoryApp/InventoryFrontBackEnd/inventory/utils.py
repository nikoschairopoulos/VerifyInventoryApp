from django.conf import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


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