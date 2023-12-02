from django.core.files import File
from django.db import models
from datetime import timezone, datetime
from qrcode import QRCode
from qrcode import constants as qrcode_constants
from io import BytesIO

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


class Comment(models.Model):
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    full_name = models.CharField(
        max_length=200,
        verbose_name='User ismi familiyasi'
    )
    text = models.TextField(max_length=1000, verbose_name='User fikri')
    status = models.BooleanField(default=True, verbose_name='Holati')
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ' || '.join([self.project.name, self.full_name])

    def get_date(self):
        return self.create_at.strftime("%d/%m/%Y")

    def date_difference(self):
        time_delta = datetime.now(timezone.utc) - self.create_at
        if time_delta.days == 0:
            if time_delta.seconds < 60:
                return f'{time_delta.seconds} sekund'

            if time_delta.seconds < 3600:
                return f'{time_delta.seconds // 60} minut {time_delta.seconds % 60} sekund'

            return f'{time_delta.seconds // 3600} soat'
        return f'{time_delta.days} kun'

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class MyLink(models.Model):
    description = models.TextField(verbose_name="Short desription", blank=True)
    link = models.URLField(verbose_name="Link")
    qr_image = models.ImageField(
        upload_to='qr_images/', verbose_name="image of QR kod", blank=True, null=True)
    created_at = models.DateTimeField(
        verbose_name="Added time", auto_now_add=True)
    is_private = models.BooleanField(default=False, verbose_name="Is Private")

    def __str__(self):
        return self.description[:20]

    def save(self, *args, **kwargs):
        if self.link != self.__class__.objects.get(pk=self.pk).link:
            self.qr_image.delete()

        qr = QRCode(
            version=1,
            error_correction=qrcode_constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.link)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer)
        self.qr_image.save(f'{self.id}.png', File(buffer), save=False)

        super(MyLink, self).save(*args, **kwargs)
