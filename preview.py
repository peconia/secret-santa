"""
Preview the Secret Santa email without drawing names or touching the real participant list.

    python preview.py                      # writes preview.html, open it in a browser
"""
from main import EMAIL_SUBJECT
from messenger import format_html_participants, html_email_template

SAMPLE_PARTICIPANTS = [
    {'name': 'Maija', 'email': 'maija@example.com'},
    {'name': 'Pekka', 'email': 'pekka@example.com'},
    {'name': 'Liisa', 'email': 'liisa@example.com'},
    {'name': 'Erik', 'email': 'erik@example.com'},
]


def main():
    email_recipient, gift_recipient = SAMPLE_PARTICIPANTS[0], SAMPLE_PARTICIPANTS[1]
    html = html_email_template(email_recipient, gift_recipient,
                               format_html_participants(SAMPLE_PARTICIPANTS))

    with open('preview.html', 'w', encoding='utf-8') as file:
        file.write(html)
    print(f'Subject: {EMAIL_SUBJECT}')
    print('Preview written to preview.html')

if __name__ == '__main__':
    main()
