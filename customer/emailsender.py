import smtplib, ssl, email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


sender_email = "appsender@shamigo.rw"
password = "Ishimuko@123"

def send_mail(receiver, company, phone, identity):

    #Create MIMEMultipart object
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Welcome "+company+" and thanks for joining us"
    msg['From'] = sender_email
    msg['To'] = receiver
  # Create the body of the message (a plain-text and an HTML version).
    text = "Hi!\nHow are you?\nHere is the all your information"
    #HTML Message Part
    
    html = """\
  <html>
    <head></head>
    <body>
      <p>Hi!<br>
        How are you? """+company+"""<br>
        Here is your client information.
        <br>
        <br>
        Identity number: """+identity+""" <br>
        With phone: """+phone+""" <br>,
        be sure to keep this information safe. and don't share it with anyone.
        any support visit us at <a href="http://localhost:3000/">Resilience website</a>
      </p>
    </body>
  </html>
  """

      # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

  # Attach parts into message container.
  # According to RFC 2046, the last part of a multipart message, in this case
  # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # Create secure SMTP connection and send email
    context = ssl.create_default_context() #SSL Connection
    with smtplib.SMTP_SSL("mail.shamigo.rw", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver, msg.as_string()
        )