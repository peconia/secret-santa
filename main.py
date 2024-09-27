import csv
import random
import requests
import secrets
from messenger import process_santa_assignment_emails

MAX_ATTEMPTS = 200
EMAIL_SUBJECT = 'Salainen joulupukki 🎅🏽 Secret Santa'


def read_google_sheet(sheet_url):
    response = requests.get(sheet_url)
    data = response.content.decode('utf-8')
    reader = csv.reader(data.splitlines())
    next(reader)  # remove first row with column names
    return list(reader)


def participant_list(data):
    participants = []
    for row in data:
        participants.append({'name': row[0], 'email': row[1], 'household': row[2]})
    return participants


def naive_allocate_santa(participants):
    targets = participants.copy()
    allocated = []

    random.shuffle(participants)
    random.shuffle(targets)

    for participant in participants:
        target = targets.pop()
        attempts = 0
        while target['email'] == participant['email'] and attempts < len(participants):
            targets.insert(0, target)

            target = targets.pop()
            attempts += 1
        allocated.append([participant, target])

    return allocated


def check_validity(allocated):
    for pair in allocated:
        if pair[0]['email'] == pair[1]['email']:
            # print('Error: ' + pair[0]['name'] + ' is assigned to themselves')
            return False
        if pair[0]['household'] == pair[1]['household']:
            # print('Error: ' + pair[0]['name'] + ' is assigned to someone in their household')
            return False
    print('All assignments are valid')
    return True


def get_valid_santa_assignments(participants):
    allocated = naive_allocate_santa(participants)
    attempts = 1
    while not check_validity(allocated) and attempts < MAX_ATTEMPTS:
        allocated = naive_allocate_santa(participants)
        attempts += 1

    if attempts == MAX_ATTEMPTS and not check_validity(allocated):
        raise Exception('Failed to find valid assignments after {} attempts'.format(MAX_ATTEMPTS))

    print('Found valid assignments after ' + str(attempts) + ' attempts')
    return allocated


def santa():
    sheet_url = secrets.SHEET_URL.split('/edit')[0] + '/export?format=csv&usp=sharing'

    data = read_google_sheet(sheet_url)
    participants = participant_list(data)
    allocated = get_valid_santa_assignments(participants)
    process_santa_assignment_emails(allocated, participants, EMAIL_SUBJECT)


if __name__ == '__main__':
    santa()
