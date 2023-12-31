# Generated by Django 4.2.5 on 2023-09-20 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_batch', '0002_alter_course_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='course',
            old_name='online',
            new_name='online_active',
        ),
        migrations.AlterField(
            model_name='course',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='thumbnails'),
        ),
    ]
