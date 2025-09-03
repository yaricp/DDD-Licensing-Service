import smtplib
from loguru import logger
from email.mime.text import MIMEText

from settings import main_config



class MailMessage:
    """A class for creating and send Gmail message.

      Methods
      -------
      get_credentials()
          Return google credential object for using GMail API

      create()
          returns the finished letter in base64 format
      send()
          Sends a message
      make_template()
          Processes a template using the Template class. Returns the processing result
      """

    def __init__(self):
        """Initialize a message

        Parameters
        ----------
        email : str
            Destination e-mail address
        subject : str
            Subject your e-mail. Default subject vars contains in mails package
        template : str
            Name of template. F.e. 'default.html'. Templates finds in TEMPLATES_DIR
            (this parameter can be change in __init__ file mails package)
        template_vars : dict
            Dictionary with names and values of variables for the passed template
       """

        self.logger = logger
        self.smtp_server = main_config.SMTP_SERVER
        self.port = main_config.SMTP_SERVER_PORT
        self.sender_email = main_config.MASTER_EMAIL
        self.password = main_config.SMTP_SERVER_PASSWORD
        self.timeout = main_config.SMTP_TIMEOUT

    def create_message(
        self, email: str, subject: str, message: str
    ) -> str:
        """Create raw message for sending (using base64)"""
        message_email = MIMEText(message, 'html')
        message_email['To'] = email
        message_email['From'] = self.sender_email
        message_email['Subject'] = subject
        # message_email['Cc'] = self.sender_email
        self.logger.info(
            f'Create message to {message_email["to"]} with subject \'{message_email["subject"]}\''
        )
        self.logger.info(f'Create message from {message_email["from"]}')
        return message_email.as_string()

    def send(
        self, email: str, subject: str, message: str
    ) -> bool:
        """
        Sends a message with object parameters
        """
        self.logger.info(f"Try to send to: {email}")
        message = self.create_message(
            email=email, subject=subject, message=message
        )
        try:
            with smtplib.SMTP(
                self.smtp_server, self.port, timeout=self.timeout
            ) as server:
                server.ehlo_or_helo_if_needed()
                # server.ehlo()
                server.starttls()
                server.login(self.sender_email, self.password)
                self.logger.info(
                    f"connected to {self.smtp_server}: {self.port}"
                )
                self.logger.info(
                    f"for {self.sender_email}: {self.password}"
                )
                server.sendmail(
                    self.sender_email,
                    [email, self.sender_email],
                    message
                )
        except Exception as e:
            self.logger.error(f"error: {e}")
            return False
        self.logger.info(f"Succesful sent: {email}")
        return True
