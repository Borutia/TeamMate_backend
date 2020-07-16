from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Profile(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        unique=True,
    )
    phone_number = models.CharField(
        verbose_name='Номер телефона',
        max_length=11,
        blank=True,
        null=True,
    )
    name = models.CharField(
        verbose_name="Имя",
        max_length=80,
        null=False,
        blank=False,
    )
    family = models.CharField(
        verbose_name="Фамилия",
        max_length=80,
        null=False,
        blank=False,
    )
    middle_name = models.CharField(
        verbose_name="Отчество",
        max_length=80,
        null=False,
        blank=False,
    )
    birthday = models.DateField(
        verbose_name="Дата рождения",
        auto_now_add=False,
        null=False,
        blank=False,
    )
    sex = models.CharField(
        verbose_name='Пол',
        max_length=1,
        blank=False,
        null=False,
        default='M'
    )
    town = models.CharField(
        verbose_name='Город проживания',
        max_length=150,
        null=False,
        blank=False,
        default='Не заполнено'
    )
    photo = models.FileField(
        verbose_name="Аватар пользователя",
        upload_to="UsersAvatars",
        max_length=256,
        null=True,
        blank=True,
    )
    speciality = models.CharField(
        verbose_name='Специальность',
        max_length=200,
        blank=True,
        null=True,
    )
    o_sebe = models.TextField(
        verbose_name='Коротко о себе',
        blank=True,
        null=True,
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг пользователя',
        null=True,
        blank=True,
        default=0
    )
    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"
        ordering = ["id"]

    def __str__(self):
        return self.name

class WorkPlace(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        unique=True,
    )
    country = models.CharField(
        verbose_name='Страна в которой работал',
        max_length=100,
        null=False,
        blank=False,
        default='ошибка заполнения',
    )
    town = models.CharField(
        verbose_name='Город в котором работал',
        max_length=100,
        null=False,
        blank=False,
        default='ошибка заполнения',
    )
    organization = models.CharField(
        verbose_name='Организация',
        max_length=100,
        null=False,
        blank=False,
        default='ошибка заполнения',
    )
    position = models.CharField(
        verbose_name='Должность',
        max_length=100,
        null=False,
        blank=False,
        default='ошибка заполнения',
    )
    work_start = models.IntegerField(
        verbose_name='Начало работы',
        null=False,
        blank=False,
        default=0,
    )
    work_end = models.IntegerField(
        verbose_name='Конец работы',
        null=False,
        blank=False,
        default=0,
    )
    def __str__(self):
        return self.id


class ProfileRating(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        unique=True,
    )
    rater = models.ForeignKey(
        User,
        verbose_name="Оценивший",
        on_delete=models.CASCADE,
        related_name='rater',
        null=False,
        blank=False,
        unique=True,
    )
    rating_type = models.CharField(
        verbose_name='Тип рейтинга',
        max_length=20,
        null=False,
        blank=False
    )
    rating = models.IntegerField(
        verbose_name='Оценка стрессоустойчивости',
        null=True,
        blank=True,
        default=5,
    )
    class Meta:
        verbose_name = "Рейтинг пользователя"
        verbose_name_plural = "Рейтинг пользователя"
        ordering = ["id"]

    def __str__(self):
        return self.id

class Education(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        unique=True,
    )
    ed_country = models.CharField(
        verbose_name='Страна в которой получено образование',
        max_length=100,
        null=True,
        blank=True,
    )
    ed_town = models.CharField(
        verbose_name='Город в котором получено образование',
        max_length=150,
        null=True,
        blank=True,
    )
    vuz = models.CharField(
        verbose_name='Название ВУЗа',
        max_length=200,
        null=True,
        blank=True,
    )
    specialty = models.CharField(
        verbose_name='Специальность',
        max_length=200,
        null=True,
        blank=True,
    )
    ed_start = models.IntegerField(
        verbose_name='Год начала обучения',
    )
    ed_end = models.IntegerField(
        verbose_name='Год окончания обучения',
    )
    class Meta:
        verbose_name = "Образование"
        verbose_name_plural = "Образования"
        ordering = ["id"]

    def __str__(self):
        return self.user


class Skill(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    skill = models.CharField(
        verbose_name="Навык",
        max_length=150,
    )
    class Meta:
        verbose_name = "Навык пользователя"
        verbose_name_plural = "Навыки пользователей"
        ordering = ["id"]

    def __str__(self):
        return self.name

class PersonalQuality(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    quality = models.CharField(
        verbose_name = 'Личное качество',
        max_length=50,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Личное качество пользователя"
        verbose_name_plural = "Личные качества пользователей"
        ordering = ["id"]

    def __str__(self):
        return self.user

class UserResorce(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    resource = models.CharField(
        verbose_name="Название ресурса",
        max_length=256,
        null=False,
        blank=False,
    )
    quantity = models.IntegerField(
        verbose_name='Количество ресурсов',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Ресурс пользователя"
        verbose_name_plural = "Ресурсы пользователя"
        ordering = ["id"]

    def __str__(self):
        return self.id

class Project(models.Model):
    owner = models.ForeignKey(
        User,
        verbose_name="Владелец",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    project_name = models.CharField(
        verbose_name="Название проекта",
        max_length=256,
        null=False,
        blank=False,
    )
    dsc = models.TextField(
        verbose_name="Описание проекта",
    )
    town = models.CharField(
        verbose_name='Город',
        max_length=150,
        blank=False,
        null=False,
        default='Ошибка заполнения',
    )
    organization = models.CharField(
        verbose_name='Организация',
        max_length=150,
        blank=False,
        null=False,
        default='Ошибка заполнения',
    )
    deadline = models.DateField(
        verbose_name='Дата сдачи проекта',
        blank=True,
        null=True,
    )
    status = models.CharField(
        verbose_name='Статус проекта',
        max_length=20,
        blank=True,
        null=True,
        default='В разработке',
    )
    max_members = models.IntegerField(
        verbose_name='Размер команды',
        null=False,
        blank=False,
        default=1,
    )
    now_members = models.IntegerField(
        verbose_name='Текущее колличество членов команды',
        null=False,
        blank=False,
        default=1,
    )
    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"
        ordering = ["id"]

    def __str__(self):
        return self.project_name

class ProjectQuality(models.Model):
    project = models.ForeignKey(
        Project,
        verbose_name="Проект",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    quality = models.CharField(
        verbose_name='Необходимое личное качество',
        max_length=100,
        blank=False,
        null=False,
    )
    class Meta:
        verbose_name = "Качество предъявляемое к претенденту"
        verbose_name_plural = "Качества предъявляемые к претендентам"
        ordering = ["project"]

    def __str__(self):
        return self.id

class ProjectSkill(models.Model):
    project = models.ForeignKey(
        Project,
        verbose_name="Проект",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    skill = models.CharField(
        verbose_name='Необходимый навык',
        max_length=100,
        blank=False,
        null=False,
    )
    class Meta:
        verbose_name = "Необходимый навык"
        verbose_name_plural = "Необходимые навыки"
        ordering = ["project"]

    def __str__(self):
        return self.id

class ProjectResource(models.Model):
    project = models.ForeignKey(
        Project,
        verbose_name="Проект",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    type = models.CharField(
        verbose_name="Название ресурса",
        max_length=100,
        null=False,
        blank=False,
        default='Ошибка заполнения',
    )
    dsc = models.CharField(
        verbose_name="Название ресурса",
        max_length=256,
        null=False,
        blank=False,
        default='Ошибка заполнения',
    )

    class Meta:
        verbose_name = "Ресурс проекта"
        verbose_name_plural = "Ресурсы проекта"
        ordering = ["id"]

    def __str__(self):
        return self.id

class Members(models.Model):
    project = models.ForeignKey(
        Project,
        verbose_name="Проект",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    class Meta:
        verbose_name = "Участник"
        verbose_name_plural = "Участники"
        ordering = ["id"]

    def __str__(self):
        return self.id

class HeadReview(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    reviewer = models.ForeignKey(
        User,
        verbose_name="Руководитель",
        related_name='review_user',
        on_delete=models.CASCADE,
        null=False,
        blank=False,
    )
    review = models.CharField(
        verbose_name='Отзыв',
        max_length=512,
        null=False,
        blank=False,
    )
    positive = models.IntegerField(
        verbose_name='Позитивность отзыва',
        null=False,
        blank=False,
        default=1
    )
    class Meta:
        verbose_name = "Отзыв руководителя"
        verbose_name_plural = "Отзывы руководителей"
        ordering = ["id"]

    def __str__(self):
        return self.id
