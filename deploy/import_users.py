#!/usr/bin/env python

import os
import csv
import argparse


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tictactoe.settings")


import django
django.setup()
from django.contrib.auth.models import User


def do_import(csvfile):
    reader = csv.DictReader(csvfile, delimiter=';')
    created = 0
    for row in reader:
        username, first_name = row['code'], row['name']
        surname, passwd = row['surname'], row['psw_day0']
        if User.objects.filter(username=username).exists():
            print("User %s exists, skipping" % username)
        else:
            User.objects.create_user(
                username=username, password=passwd,
                first_name=first_name, last_name=surname)
            print("User %s created" % username)
            created += 1
    print("%d user(s) created" % created)


def main():
    parser = argparse.ArgumentParser(
        description='Import users from dalyviai.csv')
    parser.add_argument('csvfile', type=argparse.FileType('r'))
    args = parser.parse_args()
    do_import(args.csvfile)


if __name__ == '__main__':
    main()
