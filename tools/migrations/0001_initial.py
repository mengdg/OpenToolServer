# Generated by Django 3.1.7 on 2021-04-14 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DebugTalk',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_time', models.DateTimeField(auto_now=True, null=True)),
                ('debugtalk', models.TextField(default='#debugtalk.py')),
            ],
            options={
                'verbose_name': 'debugtalk',
                'verbose_name_plural': 'debugtalk',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_time', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=64)),
                ('label', models.CharField(max_length=64)),
                ('state', models.IntegerField(default=1)),
                ('sort', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'project',
                'verbose_name_plural': 'project',
            },
        ),
        migrations.CreateModel(
            name='Tools',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_time', models.DateTimeField(auto_now=True, null=True)),
                ('image', models.CharField(default='https://tse2-mm.cn.bing.net/th/id/OIP.b545z5yupv4crcnaiIW6rgHaHa?pid=Api&rs=1', max_length=2048)),
                ('card_router', models.CharField(max_length=64, unique=True)),
                ('name', models.CharField(db_index=True, max_length=64)),
                ('describe', models.TextField(default='???')),
                ('state', models.IntegerField(default=1)),
                ('sort', models.IntegerField(default=0)),
                ('params', models.CharField(max_length=2048)),
                ('function_meta', models.CharField(max_length=2048)),
                ('debugtalk', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tools.debugtalk')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tools.project')),
            ],
            options={
                'verbose_name': 'tools',
                'verbose_name_plural': 'tools',
            },
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_time', models.DateTimeField(auto_now=True, null=True)),
                ('uid', models.CharField(db_index=True, max_length=64, unique=True)),
                ('name', models.CharField(db_index=True, max_length=64)),
                ('email', models.CharField(max_length=64, null=True)),
                ('mobile', models.CharField(max_length=16, null=True)),
                ('avatar', models.CharField(max_length=256)),
                ('identity', models.CharField(default=['viewer'], max_length=256)),
                ('state', models.IntegerField(default=1)),
            ],
            options={
                'verbose_name': '??????',
                'verbose_name_plural': '??????',
            },
        ),
        migrations.CreateModel(
            name='Wisdom',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_time', models.DateTimeField(auto_now=True, null=True)),
                ('text', models.TextField()),
            ],
            options={
                'verbose_name': 'wisdom',
                'verbose_name_plural': 'wisdom',
            },
        ),
        migrations.CreateModel(
            name='ToolVisitor',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_time', models.DateTimeField(auto_now=True, null=True)),
                ('tool', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tools.tools')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tools.users', to_field='uid')),
            ],
            options={
                'verbose_name': 'tool_visitor',
                'verbose_name_plural': 'tool_visitor',
            },
        ),
        migrations.AddField(
            model_name='tools',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tools.users', to_field='uid'),
        ),
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_time', models.DateTimeField(auto_now=True, null=True)),
                ('event', models.CharField(db_index=True, max_length=128)),
                ('content', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tools.users', to_field='uid')),
            ],
            options={
                'verbose_name': 'logs',
                'verbose_name_plural': 'logs',
            },
        ),
        migrations.AddField(
            model_name='debugtalk',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tools.users', to_field='uid'),
        ),
        migrations.CreateModel(
            name='BackupDebugTalk',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('create_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_time', models.DateTimeField(auto_now=True, null=True)),
                ('backup_debugtalk', models.TextField(default='#debugtalk.py')),
                ('debugtalk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tools.debugtalk')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tools.users', to_field='uid')),
            ],
            options={
                'verbose_name': 'backup_debugtalk',
                'verbose_name_plural': 'backup_debugtalk',
            },
        ),
    ]
