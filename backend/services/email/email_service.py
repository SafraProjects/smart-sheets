import os
import smtplib
from email.message import EmailMessage
from services.application.app_service import Env
from pydantic import EmailStr


class EmailService:
    @staticmethod
    def send_email(
        sender_email: EmailStr = "daivid.aba@gmail.com",
        receiver_email: EmailStr = "a100200303@gmail.com",
        smtp_server: str = "smtp.gmail.com",
        smtp_password: str = Env.get_app_gmail_password(),
        smtp_port: int = 465,
        subject: str = "אימות אימייל - Tabio",
        body: str = "this is a test message",
        add_attachment: list[str] = ["tabio.png"],
        link: str = None,
    ):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email

        if link:
            EmailService._add_link(msg, link=link, body=body)
        else:
            EmailService._no_link(msg, body)

        if add_attachment:
            EmailService._add_attachment(msg, add_attachment)

        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(sender_email, smtp_password)
        a = server.send_message(msg)
        server.quit()
        return a

    def _add_attachment(msg: EmailMessage, files: str or list = []):  # type: ignore
        if isinstance(files, str):
            files = [files]

        for file in files:
            try:
                file_path = os.path.join(os.path.dirname(
                    __file__), "..", "..", "assets", file)
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                    file_name = f.name

                msg.add_attachment(file_data, maintype='application',
                                   subtype='octet-stream', filename=file_name)
            except FileNotFoundError:
                print(f"Error: File '{file}' not found.")
            except Exception as e:
                print(
                    f"An error occurred while attaching the file '{file}': {e}")

    def _add_link(msg: EmailMessage, body: str, link: str):
        if isinstance(body, str):
            body = [body]

        html_content = f"""
        <html dir="rtl">
            <body style="direction: rtl; text-align: right;">
                <p>{"<br/>".join(body)}</p>
                <p>אימות חשבון: <a href="{link}" style='color: rgb(255, 142, 14);'>לחץ כאן</a></p>
            </body>
        </html>
        """
        msg.set_content(html_content, subtype='html')

    def _no_link(msg: EmailMessage, body: str):
        if isinstance(body, str):
            body = [body]

        html_content = f"""
        <html dir="rtl">
            <body style="direction: rtl; text-align: right;">
                <p>{"<br/>".join(body)}</p>
            </body>
        </html>
        """
        msg.set_content(html_content, subtype='html')


# if __name__ == "__main__":
#     a = EmailService.send_email(
#         receiver_email="a100200303@gmail.com",
#         subject="Test Email Html",
#         body="This is a test email sent from Python!",
#         link="http://localhost:8000/user/get_by_id/69d65a5f-df0c-4626-b157-9457806692c9",
#     )
