# Generated by Django 4.1 on 2025-02-25 01:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tour', '0003_alter_booking_options_alter_package_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='tour.package'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='package',
            name='availability',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='package',
            name='duration',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='package',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='packages/'),
        ),
        migrations.AlterField(
            model_name='package',
            name='vendor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='packages', to='tour.vendor'),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='company_name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
