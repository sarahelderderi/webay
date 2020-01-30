# Generated by Django 2.2.5 on 2019-11-24 20:56

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=500)),
                ('item_pic', models.ImageField(upload_to='webay/media/item_pics')),
                ('base_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('start_datetime', models.DateTimeField(verbose_name='%d/%m/%Y %H:%M:%S')),
                ('end_datetime', models.DateTimeField(verbose_name='%d/%m/%Y %H:%M:%S')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dob', models.DateField()),
                ('profile_pic', models.ImageField(default='default.jpg', upload_to='webay/media/profile_pics')),
                ('address', models.CharField(max_length=255)),
                ('mobile', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(message='Mobile number must be a valid 11 digit UK number.', regex='^0\\d{10}$')])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('email_sent', models.BooleanField()),
                ('read_message', models.BooleanField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webay.Item')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notification', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bid_datetime', models.DateTimeField(verbose_name='%d/%m/%Y %H:%M:%S')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webay.Item')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
        ),
    ]
