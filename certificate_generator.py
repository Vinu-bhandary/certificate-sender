"""
Certificate Generator & Email Sender

This script:
1. Reads participant data from a CSV file.
2. Generates personalized certificates by placing each participant's
   name and SRN on a certificate template image.
3. Authenticates with the Gmail API using OAuth2.
4. Sends each participant an email with their certificate attached.

Prerequisites:
- Install the required Python packages:
    pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client Pillow pandas

- Place your Google OAuth2 credentials file (credentials.json) in the same folder.
- Ensure 'certificate_template.jpg' and 'participants.csv' exist in the project folder.
- Create a 'certificates' folder to store generated certificates (or let the script create it).
"""

from PIL import Image, ImageDraw, ImageFont
import pandas as pd
import os
import base64
import mimetypes
from email.message import EmailMessage
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

# ---------------------- CONFIGURATIONS ----------------------
TEMPLATE_PATH = "certificate_template.jpg"  # Path to your certificate template image
FONT_PATH = "arial.ttf"                    # Path to a TrueType font file (adjust as needed)
FONT_SIZE = 80                             # Font size for participant's text
TEXT_POSITION = (900, 1000)                # (x, y) coordinates to place the text on the template
CERTIFICATES_FOLDER = "certificates/"      # Folder to store generated certificates
CSV_FILE = "participants.csv"              # CSV file with columns: Name, Srn, Email id

# Gmail API scope
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

# Sender email (the email you authorized in Google Cloud)
EMAIL_SENDER = "your_email@gmail.com"

# ---------------------- STEP 1: GENERATE CERTIFICATES ----------------------
def generate_certificates():
    """
    Reads the CSV file, generates a certificate for each participant,
    and saves it in the certificates folder.
    """
    # Load participant data
    df = pd.read_csv(CSV_FILE)

    # Create the certificates folder if it doesn't exist
    if not os.path.exists(CERTIFICATES_FOLDER):
        os.makedirs(CERTIFICATES_FOLDER)

    # Load the font
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)

    # Generate a certificate for each participant
    for _, row in df.iterrows():
        name_text = f"{row['Name']} ({row['Srn']})"
        cert_path = f"{CERTIFICATES_FOLDER}{row['Name']}.jpg"

        # Open template and draw text
        img = Image.open(TEMPLATE_PATH)
        draw = ImageDraw.Draw(img)
        draw.text(TEXT_POSITION, name_text, fill="black", font=font)

        # Save the personalized certificate
        img.save(cert_path)
        print(f"Certificate created for: {row['Name']}")

# ---------------------- STEP 2: AUTHENTICATE GMAIL ----------------------
def authenticate_gmail():
    """
    Authenticates with the Gmail API using OAuth2 and returns a service object.
    Make sure you have 'credentials.json' in the same folder.
    """
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)
    return build("gmail", "v1", credentials=creds)

# ---------------------- STEP 3: SEND EMAILS WITH CERTIFICATES ----------------------
def send_certificate(service, recipient_email, recipient_name, certificate_path):
    """
    Sends an email with the generated certificate attached using the Gmail API.
    """
    msg = EmailMessage()
    msg["Subject"] = "Congratulations! Your Certificate"
    msg["From"] = EMAIL_SENDER
    msg["To"] = recipient_email

    # Email body content
    msg.set_content(
        f"Dear {recipient_name},\n\n"
        "Congratulations! You have successfully participated in our event.\n\n"
        "We truly appreciate your dedication, enthusiasm, and contributions.\n\n"
        "Please find your Certificate of Appreciation attached.\n\n"
        "Best regards,\n"
        "The Organizing Team\n"
        "Your Institution\n"
    )

    # Attach the certificate
    with open(certificate_path, "rb") as cert_file:
        cert_data = cert_file.read()
        mime_type, _ = mimetypes.guess_type(certificate_path)
        maintype, subtype = mime_type.split("/", 1)
        msg.add_attachment(
            cert_data,
            maintype=maintype,
            subtype=subtype,
            filename=os.path.basename(certificate_path)
        )

    # Encode and send
    encoded_message = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    send_message = {"raw": encoded_message}
    service.users().messages().send(userId="me", body=send_message).execute()
    print(f"Email sent to {recipient_email}")

# ---------------------- MAIN PROCESS ----------------------
if __name__ == "__main__":
    print("🔹 Generating Certificates...")
    generate_certificates()

    print("🔹 Authenticating Gmail API...")
    gmail_service = authenticate_gmail()

    print("🔹 Sending Emails...")
    df = pd.read_csv(CSV_FILE)

    for _, row in df.iterrows():
        recipient_name = row["Name"]
        recipient_email = row["Email id"]
        certificate_path = f"{CERTIFICATES_FOLDER}{recipient_name}.jpg"

        if os.path.exists(certificate_path):
            send_certificate(gmail_service, recipient_email, recipient_name, certificate_path)
        else:
            print(f"❌ Certificate not found for {recipient_name}")

    print("✅ All certificates generated and emailed successfully!")
