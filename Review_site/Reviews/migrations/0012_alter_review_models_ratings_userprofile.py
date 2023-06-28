# Generated by Django 4.2.2 on 2023-06-27 18:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Reviews', '0011_alter_review_models_ratings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review_models',
            name='ratings',
            field=models.IntegerField(choices=[(2, '★★'), (4, '★★★★'), (5, '★★★★★'), (3, '★★★'), (1, '★')]),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('viewed_reviews', models.ManyToManyField(related_name='viewed', to='Reviews.review_models')),
            ],
        ),
    ]