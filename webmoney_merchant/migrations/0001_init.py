# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(verbose_name='Created on', unique=True, editable=False)),
                ('payment_no', models.PositiveIntegerField(verbose_name='Payment on', unique=True, editable=False)),
                ('payment_info', models.CharField(verbose_name='Payment Info', max_length=128, editable=False)),
                ('user', models.ForeignKey(verbose_name='User', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'invoice',
                'verbose_name_plural': 'invoices',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='Created on')),
                ('amount', models.DecimalField(verbose_name='Amount', max_digits=9, decimal_places=2)),
                ('payment_no', models.PositiveIntegerField(unique=True, verbose_name='Payment no')),
                ('mode', models.PositiveSmallIntegerField(verbose_name='Mode', choices=[(0, b'REAL'), (1, b'TEST')])),
                ('sys_invs_no', models.PositiveIntegerField(verbose_name='LMI_SYS_INVS_NO')),
                ('sys_trans_no', models.PositiveIntegerField(verbose_name='LMI_SYS_TRANS_NO')),
                ('sys_trans_date', models.DateTimeField(verbose_name='LMI_SYS_TRANS_DATE')),
                ('payer_purse', models.CharField(max_length=13, verbose_name='Payer purse')),
                ('payer_wm', models.CharField(max_length=12, verbose_name='Payer WM')),
                ('paymer_number', models.CharField(max_length=30, verbose_name='Paymer number', blank=True)),
                ('paymer_email', models.EmailField(max_length=254, verbose_name='Paymer email', blank=True)),
                ('telepat_phonenumber', models.CharField(max_length=30, verbose_name='Phone number', blank=True)),
                ('telepat_orderid', models.CharField(max_length=30, verbose_name='Order id', blank=True)),
                ('payment_creditdays', models.PositiveIntegerField(null=True, verbose_name='Credit days', blank=True)),
                ('invoice', models.OneToOneField(related_name='payment', null=True, blank=True, to='webmoney_merchant.Invoice', verbose_name='Invoice')),
            ],
            options={
                'verbose_name': 'payment',
                'verbose_name_plural': 'payments',
            },
        ),
        migrations.CreateModel(
            name='Purse',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('purse', models.CharField(unique=True, max_length=13, verbose_name='Purse')),
                ('secret_key', models.CharField(max_length=50, verbose_name='Secret key')),
            ],
            options={
                'verbose_name': 'purse',
                'verbose_name_plural': 'purses',
            },
        ),
        migrations.AddField(
            model_name='payment',
            name='payee_purse',
            field=models.ForeignKey(related_name='payments', verbose_name='Payee purse', to='webmoney_merchant.Purse'),
        ),
    ]
