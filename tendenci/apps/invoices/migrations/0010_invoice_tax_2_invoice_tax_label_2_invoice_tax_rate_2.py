# Generated by Django 4.2.13 on 2024-07-16 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0009_invoice_applied_cancellation_fees'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='tax_2',
            field=models.DecimalField(decimal_places=4, default=0, max_digits=15),
        ),
        migrations.AddField(
            model_name='invoice',
            name='tax_label_2',
            field=models.CharField(blank=True, default='', max_length=6),
        ),
        migrations.AddField(
            model_name='invoice',
            name='tax_rate_2',
            field=models.DecimalField(blank=True, decimal_places=5, default=0, max_digits=6),
        ),
    ]
