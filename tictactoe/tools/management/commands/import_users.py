#!/usr/bin/env python
import csv

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User


class Command(BaseCommand):
    args = '<csv file>'
    help = 'Import users from dalyviai.csv'

    def handle(self, *args, **kwargs):
        try:
            csvfile = open(args[0], 'r')
        except IndexError:
            raise CommandError("Not enough arguments")
        except FileNotFoundError:
            raise CommandError("Cannot read '%s'" % args[0])
        reader = csv.DictReader(csvfile, delimiter=';')
        created = 0
        for row in reader:
            username, first_name = row['code'], row['name']
            surname, passwd = row['surname'], row['psw_day0']
            if User.objects.filter(username=username).exists():
                self.stdout.write("User %s exists, skipping" % username)
            else:
                User.objects.create_user(
                    username=username, password=passwd,
                    first_name=first_name, last_name=surname)
                self.stdout.write("User %s created" % username)
                created += 1
        self.stdout.write("%d user(s) created" % created)
