import ssl
import smtplib
import requests

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from nameko.rpc import rpc

from config import settings


class EmailService:
    """Email Service."""

    name = "email_service"

    @rpc
    def send(self, to, subject, contents):
        if settings.debug == 'True':
            print(f'Sending email "{subject}" to "{to}" with contents "{contents}"')
            return

        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = settings.email
        message["To"] = to

        # Create the plain-text and HTML version of your message
        text = contents

        html = """\
            <html>
              <body>
                <p>Hi,<br/>
                   <br/>
                   {}
                </p>
              </body>
            </html>
            """.format(contents)

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            server.starttls(context=context)
            server.login(settings.user, settings.password)
            server.sendmail(settings.email, to, message.as_string())


class SMSService:
    """SMS Service."""

    name = "sms_service"

    @rpc
    def send(self, mobile, message):
        response = requests.post(
            url=settings.sms_api_url,
            headers={
                'Content-Type': 'application/json',
                'x-api-key': settings.sms_api_token,
            },
            json={
                'phone': mobile,
                'country_code': settings.country_code,
                'sender_id': settings.sender_id,
                'message': message,
            }
        ).json()
        return response
