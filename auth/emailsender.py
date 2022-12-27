import smtplib, ssl, email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


sender_email = "appsender@shamigo.rw"
password = "Ishimuko@123"

def send_mail(receiver, username, key, new_pass):

    #Create MIMEMultipart object
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Recover "+username+" Password"
    msg["From"] = sender_email
    msg["To"] = receiver
    filename = "auth/qrkey/"+key+".png"

    #HTML Message Part
    html = """\
<html>
  <body>
    <p><h2>Password Recover Email</h2>
    <br>
       This is your new authorization and link to change password<br>
       if you want to change now <a href="http://localhost:3000/reset_password/"""+key+""""> Click here</a> 
       </br>
        </br>
        <p>Use this authorization generate by system</p>
        </br>
        <b>Username: </b> """+username+""" and 
        <b>Password: </b> """+new_pass+"""
        </br>
        <p>Thank you ! """+username+"""</p>
        </br>
        <h3>Scan this Qr code to access password change page:</h3>
    </p>
  </body>
</html>
"""

    part = MIMEText(html, "html")
    msg.attach(part)

    # Add Attachment
    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    
    encoders.encode_base64(part)

    # Set mail headers
    part.add_header(
        "Content-Disposition",
        "attachment", filename= filename
    )
    msg.attach(part)

    # Create secure SMTP connection and send email
    context = ssl.create_default_context() #SSL Connection
    with smtplib.SMTP_SSL("mail.shamigo.rw", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver, msg.as_string()
        )