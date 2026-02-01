"""
Email Skills - Send and check emails

Provides email integration capabilities.
"""

import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List
from skills import BaseSkill


class EmailSkills(BaseSkill):
    """Email management."""
    
    def __init__(self, config: dict):
        super().__init__(config)
        email_config = config.get('integrations', {}).get('email', {})
        self.email_address = email_config.get('address', '')
        self.email_password = email_config.get('password', '')
        self.smtp_server = email_config.get('smtp_server', 'smtp.gmail.com')
        self.smtp_port = email_config.get('smtp_port', 587)
        self.imap_server = email_config.get('imap_server', 'imap.gmail.com')
        self.imap_port = email_config.get('imap_port', 993)
    
    def can_handle(self, intent: str, entities: dict) -> bool:
        """Check if this skill can handle the intent."""
        email_intents = [
            'send_email',
            'check_email',
            'read_emails',
            'unread_count'
        ]
        return intent in email_intents
    
    def execute(self, intent: str, entities: dict, raw_text: str = "") -> str:
        """Execute email commands."""
        if not self.email_address or not self.email_password:
            return (
                "Email not configured. Add credentials to config.yaml:\n"
                "integrations:\n"
                "  email:\n"
                "    address: your_email@gmail.com\n"
                "    password: your_app_password\n"
                "Note: Use app-specific password for Gmail"
            )
        
        try:
            if intent == 'send_email':
                return self._send_email(entities)
            elif intent == 'check_email':
                return self._check_unread_count()
            elif intent == 'read_emails':
                return self._read_recent_emails(entities.get('count', 3))
            elif intent == 'unread_count':
                return self._check_unread_count()
            else:
                return "I can send and check emails."
        except Exception as e:
            self.logger.error(f"Email error: {e}")
            return f"Error with email: {str(e)}"
    
    def _send_email(self, entities: Dict) -> str:
        """Send an email."""
        to_address = entities.get('to', '')
        subject = entities.get('subject', 'Message from Jarvis')
        body = entities.get('body', '')
        
        if not to_address:
            return "Please specify recipient email address."
        
        if not body:
            return "Please specify email content."
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = to_address
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_address, self.email_password)
                server.send_message(msg)
            
            return f"Email sent to {to_address}"
            
        except Exception as e:
            self.logger.error(f"Send email error: {e}")
            return f"Failed to send email: {str(e)}"
    
    def _check_unread_count(self) -> str:
        """Check number of unread emails."""
        try:
            with imaplib.IMAP4_SSL(self.imap_server, self.imap_port) as mail:
                mail.login(self.email_address, self.email_password)
                mail.select('INBOX')
                
                # Search for unread emails
                status, messages = mail.search(None, 'UNSEEN')
                
                if status == 'OK':
                    unread_count = len(messages[0].split())
                    
                    if unread_count == 0:
                        return "You have no unread emails."
                    elif unread_count == 1:
                        return "You have 1 unread email."
                    else:
                        return f"You have {unread_count} unread emails."
                else:
                    return "Could not check emails."
                    
        except Exception as e:
            self.logger.error(f"Check email error: {e}")
            return f"Failed to check emails: {str(e)}"
    
    def _read_recent_emails(self, count: int = 3) -> str:
        """Read recent emails."""
        try:
            with imaplib.IMAP4_SSL(self.imap_server, self.imap_port) as mail:
                mail.login(self.email_address, self.email_password)
                mail.select('INBOX')
                
                # Search for all emails
                status, messages = mail.search(None, 'ALL')
                
                if status != 'OK':
                    return "Could not retrieve emails."
                
                email_ids = messages[0].split()
                
                if not email_ids:
                    return "No emails in inbox."
                
                # Get most recent emails
                recent_ids = email_ids[-count:]
                
                result = f"Recent {len(recent_ids)} emails:\n\n"
                
                for email_id in reversed(recent_ids):
                    status, msg_data = mail.fetch(email_id, '(RFC822)')
                    
                    if status == 'OK':
                        email_body = msg_data[0][1]
                        email_message = email.message_from_bytes(email_body)
                        
                        subject = email_message['subject']
                        from_addr = email_message['from']
                        date = email_message['date']
                        
                        result += f"From: {from_addr}\n"
                        result += f"Subject: {subject}\n"
                        result += f"Date: {date}\n"
                        result += "---\n"
                
                return result
                
        except Exception as e:
            self.logger.error(f"Read emails error: {e}")
            return f"Failed to read emails: {str(e)}"
