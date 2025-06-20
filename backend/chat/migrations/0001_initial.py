# Generated by Django 5.2.3 on 2025-06-15 13:29

import chat.models
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(db_index=True, default=chat.models.generate_uid, max_length=12, unique=True)),
                ('headline', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='Prompt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                (
                    'status',
                    models.CharField(
                        choices=[('queued', 'Queued'), ('running', 'Running'), ('finished', 'Finished')],
                        default='queued',
                        max_length=10,
                    ),
                ),
                (
                    'result',
                    models.CharField(
                        blank=True, choices=[('success', 'Success'), ('failure', 'Failure')], max_length=10, null=True
                    ),
                ),
                ('input_text', models.TextField()),
                ('output_text', models.TextField(blank=True, default='')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('modified', models.DateTimeField(auto_now=True)),
                (
                    'chat',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name='prompts', to='chat.chat'
                    ),
                ),
            ],
            options={
                'ordering': ['created'],
            },
        ),
    ]
