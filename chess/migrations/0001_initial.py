# Generated by Django 3.0.4 on 2020-03-27 20:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('club', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('type', models.CharField(max_length=1)),
                ('time', models.DecimalField(decimal_places=1, default=0, max_digits=5)),
                ('time_add', models.DecimalField(decimal_places=1, default=0, max_digits=5)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.DecimalField(decimal_places=1, max_digits=2)),
                ('pgn', models.TextField(max_length=5000)),
                ('black_player_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='black', to='chess.Player')),
                ('tournament_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chess.Tournament')),
                ('white_player_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='white', to='chess.Player')),
            ],
        ),
    ]
