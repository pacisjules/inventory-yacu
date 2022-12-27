import smtplib, ssl, email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


sender_email = "appsendertestv1@gmail.com"
password = "Ishimwe12345@123"

def send_mail(receiver, company, phone, identity):

    #Create MIMEMultipart object
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Welcome "+company+" to our system"
    msg["From"] = sender_email
    msg["To"] = receiver


    #HTML Message Part
    html = """\
<html>
  <body>
    <p><h2>Car Care system registration</h2>
    <br>
       Thank you for work you will receive all information progress on Job<br>
       Download our mobile app here <a href="http://localhost:3000/reset_password/">Iphone</a>, <a href="http://localhost:3000/reset_password/">Android</a> and <a href="http://localhost:3000/reset_password/">Windows</a> 
       </br>
        <p>This app will help you how any process about services and check the invoices </br>
        and also you can check the status of your car and also you can check the status of your car</p>
        </p>
        <h3>Here there are service information</h3>
        </br>
        <p></p>
        <b>Company: </b> """+company+"""</br>
        <b>Phone: </b> """+phone+"""</br>
        
        <b>Identity: </b> """+identity+"""</br>
        </br>
        <p>Thank you  """+company+""" if any question fill at free to call us</p>
        </br>
        <h3>Scan this Qr code to access job progress</h3>
    </p>
  </body>
</html>
"""


    part = MIMEText(html, "html")
    msg.attach(part)


    encoders.encode_base64(part)

    """ # Set mail headers
    part.add_header(
        "Content-Disposition",        
    ) """


    # Create secure SMTP connection and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver, msg.as_string()
        )