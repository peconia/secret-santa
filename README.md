# Secret Santa

## Description
This is a simple Secret Santa program that takes a list of names and randomly assigns each person a Secret Santa. 
The program will then send an email to each person with the name of the person they are buying a gift for.

The email template is in the `santa_email.html` file. You can modify this file to change the email that is sent to each person.

## Prerequisites

You will need a public (can be temporary for when running the script) google sheet with the following columns:
- **Name** (will be shown to others as teh recipient of the gift)
- **Email** (message will be sent to this email)
- **Household name** (any unique identifier for the household, people in the same household cannot be assigned to each other)

You will also need gmail account with an app password. You can create an app password by following the instructions 
[here](https://support.google.com/accounts/answer/185833?hl=en).

## Installation

1. install the required packages
```bash 
pip install -r requirements.txt
```

2. copy the secrets-example.py file to secrets.py. Fill in the fields with your information.
```bash
cp secrets-example.py secrets.py
```

3. Run the script
```bash
python secret_santa.py
```

## Usage

You can update the number of maximum attempts to assign a secret santa in the `main.py` file, as well as set the
email subject. If a suitable assignment cannot be found after the maximum number of attempts, the program will exit.

```python
MAX_ATTEMPTS = 200
EMAIL_SUBJECT = 'Your Secret Santa Assignment'
```
