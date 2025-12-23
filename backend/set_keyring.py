#!/usr/bin/env python3
"""
Helper script to store SMTP password in the system keyring for the DAFONTE server.
Usage:
  python3 set_keyring.py --email you@gmail.com --password "your-app-password"
This will save the password under the service name `dafonte_email` and the given email as the username.
"""
import argparse
try:
    import keyring
except Exception as e:
    print('keyring not available. Install with: pip3 install keyring')
    raise

parser = argparse.ArgumentParser()
parser.add_argument('--email', required=True, help='Email address (SMTP username)')
parser.add_argument('--password', required=True, help='App password to store in keyring')
args = parser.parse_args()

keyring.set_password('dafonte_email', args.email, args.password)
print('Password saved to keyring for', args.email)
