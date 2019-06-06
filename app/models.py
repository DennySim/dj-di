from django.db import models
from django.contrib.auth.models import User, AbstractUser, PermissionsMixin, AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):
    """
    A custom user manager to deal with emails as unique identifiers for auth
    instead of usernames. The default that's used is "UserManager"
    """
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    USERNAME_FIELD = 'email'
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True,
                            verbose_name='Наименование')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class SubCategory(models.Model):
    name = models.CharField(max_length=70, unique=True,
                            verbose_name='Наименование')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='sub_cat',
                                 verbose_name='Категория')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class Product(models.Model):
    name = models.CharField(max_length=70, unique=True,
                            verbose_name='Наименование')
    img = models.FileField(upload_to='products/%Y/%m/%d/')
    description = models.TextField()
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE,
                                     default=None, verbose_name='Подкатегория')
    slug = models.SlugField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Review(models.Model):
    date_time = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    author = models.CharField(max_length=30, default=None, verbose_name='Автор')
    mark = models.IntegerField(default=1, choices=[(i,i) for i in range(1,6)])
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None,
                                related_name='reviews')

    def __str__(self):
        return self.text[:150]

    class Meta:
        verbose_name = 'Обзор'
        verbose_name_plural = 'Обзоры'


class Article(models.Model):

    author = models.CharField(max_length=30, default=None, verbose_name='Автор')
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Содержание')
    pub_date = models.DateField(auto_now_add=True)
    products = models.ManyToManyField(Product, related_name='articles',
                                      verbose_name='Товары')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title


class Order(models.Model):
    products = models.ManyToManyField(Product, related_name='orders',
                                      verbose_name='Товары')
    customer = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='user', verbose_name='Клиент')
    order_date = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата заказа')
    is_ordered = models.BooleanField()

    def __str__(self):
        return 'Заказ №' + str(self.id)

    class Meta:
        ordering = ['-order_date']
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderCountByCustomer(Order):
    class Meta:
        proxy = True
        verbose_name = 'Список ТОП 3 лучших клиентов'
        verbose_name_plural = 'Список ТОП 3 лучших клиентов'


















