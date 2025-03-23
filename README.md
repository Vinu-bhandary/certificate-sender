# Certificate Generator & Email Sender

## Overview

This project automates the process of generating personalized certificates and sending them via email. It reads participant data from a CSV file, creates a certificate for each participant by overlaying their name and ID on a certificate template, and sends the certificate as an email attachment using the Gmail API with OAuth2 authentication. You can use this for schools or universities.

## Features

- **Certificate Generation:**  
  Automatically overlays participant details onto a certificate template.

- **Email Sending:**  
  Uses the Gmail API (OAuth2) to send personalized emails with the generated certificate attached.

- **Configurable:**  
  Easily update certificate design, email content, and participant data.

## Prerequisites

- **Python 3.6+**
- **Google Cloud Project:**  
  Set up a Google Cloud project with the Gmail API enabled.  
  Follow [this guide](https://developers.google.com/gmail/api/quickstart/python) to create OAuth2 credentials and download the `credentials.json` file.

- **Required Python Packages:**  
  Install the dependencies using:
  ```bash
  pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client Pillow pandas
  ```

## Project Structure

```
certificate-sender/
├── certificate_generator.py       # Main script for generating certificates and sending emails
├── credentials.json               # OAuth2 credentials (downloaded from Google Cloud)
├── certificate_template.jpg       # Certificate template image
├── participants.csv               # CSV file containing participant details (Name, Srn, Email id)
└── certificates/                  # Folder where generated certificates are saved
```

## CSV File Format

The `participants.csv` file should contain at least the following columns:
- **Name**
- **Srn**
- **Email id**


## Usage

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Vinu-bhandary/certificate-sender.git
   cd certificate-sender
   ```

2. **Place Your Files:**
   - Put your `credentials.json` in the repository root.
   - Ensure your certificate template is named `certificate_template.jpg` (or update the `TEMPLATE_PATH` in the script).
   - Update `participants.csv` with your participant data.

3. **Adjust Configurations (if needed):**
   - Modify the font settings, text position, and other configuration variables in `certificate_generator.py`.

4. **Run the Script:**
   ```bash
   python certificate_generator.py
   ```
   - A browser window will open for OAuth2 authentication. Log in with your Gmail account and authorize the application.
   - The script will generate certificates in the `certificates/` folder and send emails to all participants.

## Customization

- **Email Content:**  
  You can customize the email subject and body in the `send_certificate` function within the script.

- **Certificate Design:**  
  Update the certificate template image or adjust the text position and font settings to match your design requirements.

## Notes

- The script uses OAuth2 for authentication, so no app passwords are required.
- Make sure your Google Cloud project is set up correctly and that the Gmail API is enabled.
- This project is intended for demonstration purposes and can be extended or modified to suit your needs.
