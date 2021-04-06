# Generated by Django 2.2.17 on 2020-12-23 15:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_groups', '0004_auto_20200902_1545'),
        ('corporate_memberships', '0024_corporatemembershiptype_require_approval'),
    ]

    operations = [
        migrations.AddField(
            model_name='corporatemembershiptype',
            name='active_group',
            field=models.ForeignKey(help_text='Group to add representatives upon their applications approval.', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='corp_types_for_active_group', to='user_groups.Group', verbose_name='Group for Reps upon Approval'),
        ),
        migrations.AddField(
            model_name='corporatemembershiptype',
            name='pending_group',
            field=models.ForeignKey(help_text='Group to add representatives upon their applications pending.', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL, related_name='corp_types_for_pending_group', to='user_groups.Group', verbose_name='Group for Reps upon Pending'),
        ),
    ]
