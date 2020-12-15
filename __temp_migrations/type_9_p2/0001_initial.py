# Generated by Django 2.2.4 on 2019-11-01 14:18

from django.db import migrations, models
import django.db.models.deletion
import otree.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('otree', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_in_subsession', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('p2_cycle', otree.db.models.IntegerField(default=1, null=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_9_p2_group', to='otree.Session')),
            ],
            options={
                'db_table': 'type_9_p2_group',
            },
        ),
        migrations.CreateModel(
            name='Subsession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('session', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='type_9_p2_subsession', to='otree.Session')),
            ],
            options={
                'db_table': 'type_9_p2_subsession',
            },
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_in_group', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('_payoff', otree.db.models.CurrencyField(default=0, null=True)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('_gbat_arrived', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('_gbat_grouped', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('p2_cycle', otree.db.models.IntegerField(default=1, null=True)),
                ('p2_round', otree.db.models.IntegerField(default=1, null=True)),
                ('decision', otree.db.models.StringField(choices=[('Green', 'Green'), ('Red', 'Red')], max_length=10000, null=True)),
                ('group_decision', otree.db.models.StringField(max_length=10000, null=True)),
                ('die_roll', otree.db.models.IntegerField(null=True)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='type_9_p2.Group')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_9_p2_player', to='otree.Participant')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_9_p2_player', to='otree.Session')),
                ('subsession', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='type_9_p2.Subsession')),
            ],
            options={
                'db_table': 'type_9_p2_player',
            },
        ),
        migrations.AddField(
            model_name='group',
            name='subsession',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='type_9_p2.Subsession'),
        ),
    ]