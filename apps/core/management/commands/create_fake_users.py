# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

import datetime
import pytz
import requests

USER_NUMBER_DEFAULT = 100


class Command(BaseCommand):
    help = 'Fetch couple fake users from https://randomuser.me/'

    def add_arguments(self, parser):
        parser.add_argument('user_number',
                            nargs='?',
                            help='Number of users to be created')

    def handle(self, *args, **options):
        User.objects.filter(is_staff=False).delete()

        try:
            user_number = int(options.get('user_number'))
        except (ValueError, TypeError):
            user_number = USER_NUMBER_DEFAULT

        if user_number < 1:
            user_number = 1
        if user_number > USER_NUMBER_DEFAULT:
            user_number = USER_NUMBER_DEFAULT

        ru_url = 'http://api.randomuser.me/?results=%d' % user_number
        try:
            response = requests.get(ru_url)
            response.raise_for_status()
            for user in response.json()['results']:
                u = User(
                    username=user['user']['username'],
                    first_name=user['user']['name']['first'],
                    last_name=user['user']['name']['last'],
                    email=user['user']['email'],
                    password=make_password(user['user']['password']),
                    date_joined=datetime.datetime.fromtimestamp(
                        float(user['user']['registered'])).replace(tzinfo=pytz.UTC)
                )
                u.save()
        except requests.exceptions.HTTPError:
            self.stdout.write('Request "%s" returned HTTP error %s' % (response.url, response.status_code,))
            return
        except ValueError:
            self.stdout.write('Decoding JSON has failed')
            return
        self.stdout.write('')
        self.stdout.write('Done')