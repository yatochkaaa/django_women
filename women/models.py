# from transliterate import translit
from django.db import models
from django.urls import reverse
# from django.template.defaultfilters import slugify


class PublishedManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(is_published=Women.Status.PUBLISHED)


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Категория")
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("category", kwargs={"category_slug": self.slug})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return str(self.tag)

    def get_absolute_url(self):
        return reverse("tag", kwargs={"tagpost_slug": self.slug})


class Husband(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    m_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return str(self.name)


class Women(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, "Черновик"
        PUBLISHED = 1, "Опубликовано"

    # Fields
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(
        max_length=255, db_index=True, unique=True, verbose_name="Slug"
    )
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время изменения")
    is_published = models.BooleanField(
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
        default=Status.DRAFT,
        verbose_name="Статус",
    )

    # Relations
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="posts",
        verbose_name="Категории",
    )
    tags = models.ManyToManyField(
        TagPost, blank=True, related_name="tags", verbose_name="Теги"
    )
    husband = models.OneToOneField(
        Husband,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="women",
        verbose_name="Муж",
    )

    # Managers
    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Известные женщины"
        verbose_name_plural = "Известные женщины"
        ordering = ["-time_create"]
        indexes = [models.Index(fields=["-time_create"])]

    def get_absolute_url(self):
        return reverse("post", kwargs={"post_slug": self.slug})

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(translit(self.title, reversed=True))
    #     super().save(*args, **kwargs)
