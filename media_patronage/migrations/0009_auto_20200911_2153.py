# Generated by Django 3.1 on 2020-09-11 21:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media_patronage', '0008_auto_20200905_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='event',
            field=models.ForeignKey(help_text='Wydarzenie, którego dotyczy', on_delete=django.db.models.deletion.CASCADE, to='media_patronage.event', verbose_name='Wydarzenie'),
        ),
        migrations.AlterField(
            model_name='article',
            name='pdf_article',
            field=models.FileField(null=True, upload_to='articles/', verbose_name='PDF'),
        ),
        migrations.AlterField(
            model_name='article',
            name='portal',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='media_patronage.portal', verbose_name='Na jakim portalu opublikowane'),
        ),
        migrations.AlterField(
            model_name='article',
            name='published_date',
            field=models.DateField(verbose_name='Data publikacji'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=250, verbose_name='Tytuł'),
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('send_from_email', models.EmailField(max_length=254)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='media_patronage.event')),
                ('to_who', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addressee', to='media_patronage.person')),
            ],
        ),
    ]