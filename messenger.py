import secrets
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def hydrate_message(message, email_recipient, gift_recipient, participants_list):
    message = message.replace('{{email_recipient_name}}', email_recipient['name'])
    message = message.replace('{{gift_recipient_name}}', gift_recipient['name'])
    message = message.replace('{{participants}}', participants_list)
    return message


def format_html_participants(participants):
    participants_list = ''
    for participant in participants:
        participants_list += '<li>' + participant['name'] + '</li>'
    return participants_list


def html_email_template(email_recipient, gift_recipient,participants_html):
    # import html template from santa_email.html
    with open('santa_email.html', 'r', encoding='utf-8') as file:
        html_message = file.read()
        message = hydrate_message(html_message, email_recipient, gift_recipient, participants_html)
        return message


def process_santa_assignment_emails(allocated_pairs, participants, subject):
    html_participants = format_html_participants(participants)
    emails_to_send = []

    for pair in allocated_pairs:
        email_recipient = pair[0]
        gift_recipient = pair[1]

        # print('{} is sending a gift to {}'.format(email_recipient['name'], gift_recipient['name']))
        message_html = html_email_template(email_recipient, gift_recipient, html_participants)

        emails_to_send.append({'recipient': email_recipient['email'], 'message_html': message_html})

    for email in emails_to_send:
        send_email(email['recipient'], email['message_html'], subject)


def send_gmail_email(recipient_email, subject, html_body):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    msg = MIMEMultipart()
    msg['From'] = secrets.SENDER_EMAIL
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_body, 'html'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(secrets.SENDER_EMAIL, secrets.SENDER_PASSWORD)

        server.sendmail(secrets.SENDER_EMAIL, recipient_email, msg.as_string())
        print('Email sent successfully')

    except Exception as e:
        print(f'Failed to send email: {e}')

    finally:
        # Close the connection to the SMTP server
        server.quit()


def send_email(recipient, message_html, subject):
    # do not send emails while testing
    if recipient != 'testtest@gmail.com' and recipient != 'test@example.com':
        print('not sending email to ' + recipient)
        return None

    send_gmail_email(recipient, subject, message_html)
