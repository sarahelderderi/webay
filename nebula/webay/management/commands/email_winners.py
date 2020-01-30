from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django.db import connection

SUBJECT = 'You won auction {}!'


class Command(BaseCommand):
    help = 'Finds winners of closed auctions who have not been emailed yet ' \
           'and sends them an email. Updates db to reflect whether email was ' \
           'sent successfully.'

    def handle(self, *args, **options):
        not_emailed = self.get_all_not_emailed()
        for winner in not_emailed:
            user_id, email, item_id, message = winner
            subject = SUBJECT.format(item_id)
            email_successful = send_mail(subject, message, 'webaycw@gmail.com', [email])
            if email_successful:
                self.update_email_db(item_id)

    def get_all_not_emailed(self):
        with connection.cursor() as cursor:
            cursor.execute('SELECT u.id, u.email, n.item_id, n.message '
                           'FROM webay_notification n '
                           'JOIN auth_user u ON u.id = n.recipient_id '
                           'WHERE email_sent = 0')
            row = cursor.fetchall()
        return row

    def update_email_db(self, item_id):
        with connection.cursor() as cursor:
            sql = 'UPDATE webay_notification ' \
                  'SET email_sent = 1 ' \
                  'WHERE item_id = :item_id'
            cursor.execute(sql, {'item_id': item_id})
            connection.commit()
