# Generated by Django 3.2.12 on 2024-02-14 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DAWActivity', '0003_auto_20240203_1851'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tradeoffer',
            name='offers',
        ),
        migrations.RemoveField(
            model_name='tradeoffer',
            name='offersResource',
        ),
        migrations.RemoveField(
            model_name='tradeoffer',
            name='wants',
        ),
        migrations.RemoveField(
            model_name='tradeoffer',
            name='wantsResource',
        ),
        migrations.AddField(
            model_name='tradeoffer',
            name='offeredFood',
            field=models.IntegerField(default=0, verbose_name='Offered food'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tradeoffer',
            name='offeredStone',
            field=models.IntegerField(default=0, verbose_name='Offered stone'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tradeoffer',
            name='offeredWood',
            field=models.IntegerField(default=0, verbose_name='Offered wood'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tradeoffer',
            name='wantedFood',
            field=models.IntegerField(default=0, verbose_name='Wanted food'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tradeoffer',
            name='wantedStone',
            field=models.IntegerField(default=0, verbose_name='Wanted stone'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tradeoffer',
            name='wantedWood',
            field=models.IntegerField(default=0, verbose_name='Wanted wood'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='upgrade',
            name='level',
            field=models.IntegerField(default=0, verbose_name='Level to upgrade to'),
            preserve_default=False,
        ),
    ]