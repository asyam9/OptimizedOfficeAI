# Generated by Django 4.2.2 on 2023-06-25 12:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reviews', '0006_alter_review_models_imgfile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review_models',
            name='imgfile',
            field=models.ImageField(upload_to='review_images/', validators=[django.core.validators.validate_image_file_extension, django.core.validators.FileExtensionValidator(allowed_extensions=['jpg'], message='jpg 형식의 확장자만 사용 가능합니다.')]),
        ),
        migrations.AlterField(
            model_name='review_models',
            name='ratings',
            field=models.IntegerField(choices=[(1, '★'), (4, '★★★★'), (3, '★★★'), (2, '★★'), (5, '★★★★★')]),
        ),
    ]
