from django.utils.html import mark_safe
from django.db import models

# Create your models here.

DIRECTIONS = [
    ('frontend', 'Frontend'),
    ('backend', 'Backend'),
    ('full_stack', 'Full Stack'),
    ('telegram_bot', 'Telegram bot')
]


class Project(models.Model):
    name = models.CharField(
        max_length=60,
        verbose_name="Loyiha nomi"
    )
    date = models.DateField(
        verbose_name="Vaqt"
    )
    client = models.CharField(
        max_length=200,
        verbose_name="Klient ismi"
    )
    demo_url = models.URLField(
        max_length=100,
        verbose_name="Demo sayt manzili",
        blank=True,
        null=True
    )
    github_url = models.URLField(
        max_length=100,
        verbose_name="Githubdagi manzili",
        null=True,
        blank=True,
    )
    direction = models.CharField(
        max_length=12,
        choices=DIRECTIONS,
        verbose_name="Loyiha yo'nalishi"
    )
    short_description = models.TextField(
        verbose_name="Qisqa ma'lumot"
    )
    full_description = models.TextField(
        verbose_name="To'liq ma'lumot"
    )
    create_at = models.DateTimeField(auto_now_add=True)
    sequence_number = models.IntegerField(
        verbose_name='Tartib raqami',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def get_date(self):
        return self.date.strftime("%d/%m/%Y")

    def __str__(self):
        return self.name + ' || ' + str(self.get_date())


class Image(models.Model):
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        verbose_name="Project",
        related_name='images'
    )
    image = models.ImageField(
        upload_to='project_image/',
        verbose_name="Image",
    )
    status = models.BooleanField(default=False, verbose_name='Holati')
    create_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
