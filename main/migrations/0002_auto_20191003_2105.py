# Generated by Django 2.2.6 on 2019-10-03 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='Recruit',
            new_name='recruit',
        ),
        migrations.AddField(
            model_name='recruit',
            name='planet',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='main.Planet'),
            preserve_default=False,
        ),
    ]