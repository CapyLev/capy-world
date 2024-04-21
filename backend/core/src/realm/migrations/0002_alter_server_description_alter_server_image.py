# Generated by Django 5.0.3 on 2024-04-21 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='server',
            name='image',
            field=models.ImageField(null=True, upload_to='servers_images/'),
        ),
    ]
