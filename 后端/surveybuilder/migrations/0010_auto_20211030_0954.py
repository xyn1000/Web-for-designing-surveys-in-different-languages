# Generated by Django 3.2.7 on 2021-10-30 09:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surveybuilder', '0009_draganddropchoice_draganddropquestion_likertchoice_likertscalequestion'),
    ]

    operations = [
        migrations.CreateModel(
            name='DragAndDropCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.IntegerField(default=None)),
                ('title', models.CharField(default='', max_length=5000)),
            ],
        ),
        migrations.RemoveField(
            model_name='likertscalequestion',
            name='question',
        ),
        migrations.RenameField(
            model_name='draganddropquestion',
            old_name='options',
            new_name='choices',
        ),
        migrations.AddField(
            model_name='draganddropquestion',
            name='cards',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='LikertChoice',
        ),
        migrations.DeleteModel(
            name='LikertScaleQuestion',
        ),
        migrations.AddField(
            model_name='draganddropcard',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surveybuilder.draganddropquestion'),
        ),
    ]
