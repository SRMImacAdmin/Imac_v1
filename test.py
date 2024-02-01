import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import make_msgid
import base64


# Email configuration
admin = "srmimactest@gmail.com"
sender_email = admin
receiver_email = "rprem058@gmail.com"
subject = "test 2"

# Read the SVG file
with open("D:/MyCode/MainProjects/iman-main/imac/templates/myqr.png", "rb") as svg_file:
    svg_contents = svg_file.read()

# Encode the contents in Base64
base64_encoded_svg = base64.b64encode(svg_contents).decode("utf-8")

img_cid = make_msgid()



# Create an HTML email message
html_message = """
<!DOCTYPE html>
<html>
<head>
    <title>iMac Booking Confirmation</title>
</head>
<body>
    <table width="100%" style="max-width: 600px; margin: 0 auto; font-family: Arial, sans-serif; border: 1px solid #ccc;">
        <tr>
            <td style="background-color: #7864F6; color: #fff; padding: 20px; text-align: center;">
                <h1>iMac Booking Confirmation</h1>
            </td>
        </tr>
        <tr>
            <td style="padding: 20px;">
                <p>Dear Priyanshu,</p>
                <!-- Replace 'base64_encoded_svg_data_here' with your actual Base64-encoded SVG image data -->
                <img src="cid:image1" alt="QR Code">

                <p>Your booking for an iMac system has been confirmed. Below are the details of your booking:</p>
                <ul>
                    <li><strong>Date:</strong> 25-10-2023</li>
                    <li><strong>Time:</strong> 12:00 PM</li>
                    <li><strong>Lab No:</strong> 1</li>
                </ul>
                <p>Please make sure to arrive on time and bring any necessary identification or materials required for your task.</p>
                <p>If you have any questions or need to make changes to your booking, please contact our support team at [Contact Email].</p>
                <p>Thank you for using our services. We look forward to serving you!</p>
                <p>Best regards,<br>[Your Name]</p>
                
                
            </td>
        </tr>
        <tr>
            <td style="background-color: #f5f5f5; text-align: center; padding: 10px;">
                &copy; SRMIST
            </td>
        </tr>
    </table>
</body>
</html>
"""
html_message = html_message.format(image= img_cid[1:-1])

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
smtp_port = 587
smtp_username = admin
smtp_password = "khqp aqjr lkmg ttsk"

# Start the SMTP connection
with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(smtp_username, smtp_password)
    server.sendmail(sender_email, receiver_email, message.as_string())

print("Email sent successfully.")
