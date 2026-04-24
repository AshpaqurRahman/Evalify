import random
import string
from django.db import migrations, models


def generate_codes(apps, schema_editor):
    Course = apps.get_model('evalify_app', 'Course')
    used = set()
    chars = string.ascii_uppercase + string.digits
    for course in Course.objects.all():
        if not course.enrollment_code:
            while True:
                code = ''.join(random.choices(chars, k=6))
                if code not in used:
                    used.add(code)
                    course.enrollment_code = code
                    course.save(update_fields=['enrollment_code'])
                    break


class Migration(migrations.Migration):

    dependencies = [
        ('evalify_app', '0013_subquestion_grades'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='enrollment_code',
            field=models.CharField(max_length=8, blank=True, default=''),
            preserve_default=False,
        ),
        migrations.RunPython(generate_codes, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='course',
            name='enrollment_code',
            field=models.CharField(max_length=8, unique=True, blank=True, default=''),
        ),
    ]
