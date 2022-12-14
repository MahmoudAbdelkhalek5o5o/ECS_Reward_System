# Generated by Django 3.2 on 2022-09-25 08:39

import Users.models
import activities.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_name', models.CharField(max_length=30)),
                ('activity_description', models.CharField(blank=True, max_length=1024)),
                ('points', models.IntegerField()),
                ('attachment_mandatory', models.BooleanField(default=True)),
                ('evidence_needed', models.CharField(max_length=1024)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(null=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('is_archived', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ActivityCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=30, unique=True)),
                ('description', models.CharField(default='', max_length=255, unique=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(null=True)),
                ('budget', models.IntegerField()),
                ('budget_compare', models.IntegerField()),
                ('is_archived', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Points',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.IntegerField()),
                ('amounts', models.IntegerField()),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(editable=False)),
                ('is_used', models.BooleanField(default=False)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='earned_to', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ActivitySuggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity_name', models.CharField(max_length=30)),
                ('activity_description', models.CharField(max_length=1024)),
                ('justification', models.CharField(blank=True, max_length=30, null=True)),
                ('evidence_needed', models.CharField(blank=True, max_length=1024, null=True)),
                ('is_archived', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activities.activitycategory')),
            ],
        ),
        migrations.CreateModel(
            name='ActivityRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField()),
                ('status', models.CharField(choices=[(activities.models.Status['A'], 'Approved'), (activities.models.Status['P'], 'Pending'), (activities.models.Status['D'], 'Declined')], max_length=10)),
                ('evidence_needed', models.CharField(default='Provide evidence please', max_length=1024)),
                ('proof_of_action', models.FileField(upload_to='proofs/')),
                ('activity_approval_date', models.DateTimeField(null=True)),
                ('is_archived', models.BooleanField(default=False)),
                ('activity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activities.activity')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activities.activitycategory')),
                ('emp', models.ForeignKey(limit_choices_to={'role': Users.models.Role['E']}, on_delete=django.db.models.deletion.CASCADE, related_name='submitter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='activity',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='activities.activitycategory'),
        ),
    ]
