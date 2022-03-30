# Generated by Django 4.0.3 on 2022-03-21 08:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_product_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0002_order_date_ordered'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='quantity_of_product',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
