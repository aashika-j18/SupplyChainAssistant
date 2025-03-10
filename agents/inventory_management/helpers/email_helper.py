import smtplib
import os
import dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


dotenv.load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(receiver_email:str, message:str) -> str:
    """
    Use this function to send an email to the specified receiver with the given message as body.

    Args:
        receiver_email (str): The email address of the recipient.
        message (str): The body content of the email.

    Raises:
        Exception: If an error occurs during the email sending process.
    """
    try:
        
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = receiver_email
        msg["Subject"] = "Stock Order"
        msg.attach(MIMEText(message, "plain"))

        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        
       
        server.sendmail(EMAIL_SENDER, receiver_email, msg.as_string())
        
        
        server.quit()

        return str({"response":f"Email sent successfully to {receiver_email}"})
    except Exception as e:
        print(f"Error sending email: {e}")


# send_email("aashika2210193@ssn.edu.in", "Stock Order", "Please send us 50 units of item 123.")
