import imaplib
import email
import re
import time
import logging

class GmailUtil:
    def __init__(self, email_address, app_password):
        self.email_address = email_address
        self.app_password = app_password
        self.imap_server = "imap.gmail.com"
        self.imap_port = 993

    def get_otp_from_gmail(self, timeout=30, retry_interval=5):
        """
        Connects to Gmail, fetches latest email from 'no-reply@brightcone.ai' or subject containing OTP,
        and extracts 6-digit OTP using regex.
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # Login to Gmail
                mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
                mail.login(self.email_address, self.app_password)
                mail.select("inbox")

                # Search for emails from the sender or related subject
                # Searching all since we want newest. Then filter.
                # In practice, searching for 'UNSEEN' is better but we'll fetch last few.
                status, messages = mail.search(None, 'ALL')
                if status != 'OK':
                    mail.logout()
                    time.sleep(retry_interval)
                    continue

                mail_ids = messages[0].split()
                if not mail_ids:
                    mail.logout()
                    time.sleep(retry_interval)
                    continue

                # Get latest mail ID
                latest_mail_id = mail_ids[-1]
                status, data = mail.fetch(latest_mail_id, '(RFC822)')
                
                if status != 'OK':
                    mail.logout()
                    time.sleep(retry_interval)
                    continue

                for response_part in data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        # Get body
                        if msg.is_multipart():
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                if content_type == "text/plain":
                                    body = part.get_payload(decode=True).decode()
                                    break
                        else:
                            body = msg.get_payload(decode=True).decode()

                        # Extract 6-digit OTP
                        otp_match = re.search(r'\b\d{6}\b', body)
                        if otp_match:
                            otp = otp_match.group(0)
                            print(f"DEBUG: Found OTP: {otp}")
                            mail.close()
                            mail.logout()
                            return otp

                mail.close()
                mail.logout()
                
            except Exception as e:
                logging.error(f"Error fetching email: {e}")
            
            time.sleep(retry_interval)
            print(f"DEBUG: Waiting for OTP... (Time elapsed: {int(time.time() - start_time)}s)")
        
        print("DEBUG: OTP Fetching timed out!")
        return None
