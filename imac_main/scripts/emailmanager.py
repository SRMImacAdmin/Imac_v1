import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Email configuration
admin = "srmimactest@gmail.com"
sender_email = admin

def send_email(receiver_email, title, stud_name, date, time_from, time_till, labno):
    subject = "iMac Booking Confirmation"





    # Create an HTML email message
    with open("D:/MyCode/MainProjects/iman-main/imac/templates/email_temp.html", "r") as file:
        html_message = file.read()


    html_message = html_message.format(stud_name=stud_name, title= title, date= f"{date}", time= f"{time_from} - {time_till}", lab=labno)

    # Create a MIMEText object for the HTML content
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(html_message, "html"))

    image = MIMEImage(open("D:/MyCode/MainProjects/iman-main/imac/templates/myqr.png", "rb").read())

    image.add_header("Content-ID", '<image1>')
    message.attach(image)

    # Connect to your SMTP server (e.g., for Gmail)
    smtp_server = "smtp.gmail.com"
    smtp_port = 25
    smtp_username = admin
    smtp_password = "khqp aqjr lkmg ttsk"

    # Start the SMTP connection
    server =  smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.sendmail(sender_email, receiver_email, message.as_string())

    print("Email sent successfully.")

#send_email("ps0891@srmist.edu.in","ps0891", "ps0891", "ps0891", "ps08" ,"", "4")