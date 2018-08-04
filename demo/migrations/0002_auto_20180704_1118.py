# Generated by Django 2.0.6 on 2018-07-04 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subject',
            options={'verbose_name': '学科', 'verbose_name_plural': '学科'},
        ),
        migrations.AlterModelOptions(
            name='teacher',
            options={'ordering': ('name',), 'verbose_name': '讲师', 'verbose_name_plural': '讲师'},
        ),
        migrations.AddField(
            model_name='teacher',
            name='bad_count',
            field=models.IntegerField(db_column='sbcount', default=0, verbose_name='差评数'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='good_count',
            field=models.IntegerField(db_column='sgcount', default=0, verbose_name='好评数'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='photo',
            field=models.CharField(blank=True, db_column='tphoto', max_length=511, null=True, verbose_name='照片'),
        ),
    ]