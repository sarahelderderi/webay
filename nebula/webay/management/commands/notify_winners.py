# coding=utf-8
from django.core.management.base import BaseCommand
from django.db import connection

NOTIFY_MESSAGE = 'Dear {} {},\\nCongrats! You have won the {}.\\nJust to remind you, you bidded: £{}.' \
                 '\\nKind regards,\\nWebay'


class Command(BaseCommand):
    help = 'Finds winners of closed auctions who have not been notified, ' \
           'and creates a notification for them'

    def handle(self, *args, **options):
        winners = self.get_all_not_notified_winners()
        for winner in winners:
            fname, lname, title, item_id, user_id, amount = winner
            message = NOTIFY_MESSAGE.format(fname, lname, title, amount)
            self.create_notification_db(user_id, item_id, message)

    def get_all_not_notified_winners(self):
        with connection.cursor() as cursor:
            cursor.execute('SELECT u.first_name, u.last_name, i.title, i.id, u.id, '
                           'MAX(b.amount) as max_price '
                           'FROM webay_bid b '
                           'JOIN auth_user u ON u.id = b.user_id '
                           'JOIN webay_item i ON i.id = b.item_id '
                           'WHERE i.id NOT IN (SELECT item_id from webay_notification) '
                           'GROUP BY b.item_id')
            row = cursor.fetchall()
        return row

    def create_notification_db(self, user_id, item_id, message):
        with connection.cursor() as cursor:
            sql = 'INSERT INTO webay_notification(message, email_sent, read_message, recipient_id, item_id) ' \
                  'VALUES (%s, %s, %s, %s, %s)'
            params = (message, 0, 0, user_id, item_id)
            cursor.execute(sql, params)
            connection.commit()
