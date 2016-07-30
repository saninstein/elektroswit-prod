import PIL
import datetime
import random
import string
from os import remove, path, listdir, rmdir
from django.db import models
from django.core.exceptions import ValidationError
from elektroswit.settings import MEDIA_ROOT
from django.db.models import Max, Q
from django.contrib.auth.models import User

available = (('is', "В наличии"), ('c', "Под заказ"))
cores = ((1, '1'), (2, '2'), (3, '3'), (4, '4'), (6, '6'), (8, '8'), (12, '12'))
modes = ((0, 'Гаджеты'), (1, 'Акссесуары'), (2, 'Для Мастера'), (3, 'Для Дома'))


def get_item(item_inv):
    l = [list(x.objects.filter(pk=item_inv)) for x in (Phone, Tablet, Notebook, Accessories,
                                                        ForMaster, ForHome, Share)]
    item = list()
    for x in l:
        item += x
    if item:
        return item[0]
    return False


def get_linked_items(class_name, pk=1, count=''):
    q = class_name.objects.get(pk=pk)
    links = [rel.get_accessor_name() for rel in q._meta.get_fields() if type(rel) == models.ManyToOneRel]
    l = list()
    for link in links:
        if count != '':
            l.append(getattr(q, link).all()[:count])
        else:
            l.append(getattr(q, link).all())
    return l


def compress_img(path_img, size):
    img = PIL.Image.open(path_img)
    img.thumbnail(size, PIL.Image.ANTIALIAS)
    bg = PIL.Image.new('RGB', size, (255, 255, 255))
    bg.paste(img, ((size[0] - img.size[0]) // 2, (size[1] - img.size[1]) // 2))
    if size == (250, 250):
        thumb_path = path_img.split('.')
        thumb_path = thumb_path[0] + '_thumb.' + thumb_path[1]
        if not path.isfile(thumb_path):
            bg.save(thumb_path)

    else:
        remove(path_img)
        bg.save(path_img)


def get_uniq_name(instance, filename):
    if type(instance) == Slide:
        new_name = 'slides/'
        new_name += ''.join(random.sample(string.ascii_lowercase, 6))
    else:
        new_name = ''.join(random.sample(string.ascii_lowercase, 6))
    new_name += filename[filename.find('.'):]
    return new_name


def upload_path(instance, filename):
    return '{0}/{1}/{2}'.format(instance.link_category.id, instance.name, get_uniq_name(instance, filename))


def get_inv():
    random.seed()
    num = []
    while True:
        inv = random.randint(0, 99999999999)
        a = [Phone.objects, Tablet.objects, Notebook.objects, Accessories.objects, ForMaster.objects, ForHome.objects,
             Share.objects]
        for i in a:
            agr = i.filter(inv=inv).count()
            num.append(agr)
        if max(num) == 0:
            return inv


class Items(models.Model):
    name = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(default='Категория', max_length=100, verbose_name="Название", null=False, blank=False)
    variant = models.IntegerField(default=modes[0], choices=modes)

    def __str__(self):
        return self.name


class Other(models.Model):
    class Meta:
        abstract = True
        ordering = ["-date"]
    name = models.CharField(max_length=100, verbose_name='Название', help_text='Введите название', default='')
    availability = models.CharField(max_length=100, verbose_name='Наличие', choices=available, default=available[0])
    photo = models.ImageField(verbose_name='Главное фото', upload_to=upload_path, blank=False,
                              help_text='Обязательное поле')
    photo1 = models.ImageField(verbose_name='Фото 1', upload_to=upload_path, blank=True)
    photo2 = models.ImageField(verbose_name='Фото 2', upload_to=upload_path, blank=True)
    photo3 = models.ImageField(verbose_name='Фото 3', upload_to=upload_path, blank=True)
    photo4 = models.ImageField(verbose_name='Фото 4', upload_to=upload_path, blank=True)
    photo5 = models.ImageField(verbose_name='Фото 5', upload_to=upload_path, blank=True)
    video = models.URLField(verbose_name='Видеообзор', blank=True, help_text='Введите адрес YouTube видео')
    description = models.TextField(verbose_name='Описание', max_length=1500, blank=True)
    date = models.DateTimeField(auto_now_add=True, editable=False)
    price = models.DecimalField(verbose_name='Цена в розницу', max_digits=20, decimal_places=2,
                                help_text='Обязательное поле')
    price_opt = models.DecimalField(verbose_name='Цена оптом', max_digits=20, decimal_places=2, default=0, help_text='Если не надо - оставить нулём')
    inv = models.IntegerField(editable=False, default=get_inv, primary_key=True)
    likes = models.IntegerField(editable=False, default=0)

    def __str__(self):
        return self.name

    def get_thumb(self):
        url = self.photo.url
        url = url.split('.')
        thumb_url = url[0] + '_thumb.' + url[1]
        return thumb_url

    def delete(self, *args, **kwargs):
        shares = Share.objects.filter((Q(gen_item__exact=self.inv) | Q(sec_item__exact=self.inv)))
        if shares:
            for share in shares:
                share.delete()

        path = '{0}/{1}/{2}/'.format(MEDIA_ROOT, self.link_category_id, self.name)
        print(path)
        try:
            for file in listdir(path):
                remove(path + file)
            rmdir(path)
        except BaseException:
            pass
        super(Other, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(Other, self).save(*args, **kwargs)
        try:
            compress_img(self.photo.path, (250, 250))
            compress_img(self.photo.path, (800, 600))
            photos = [self.photo1, self.photo2,
                      self.photo3, self.photo4,
                      self.photo5]
            for photo in photos:
                if photo != '':
                    compress_img(photo.path, (800, 600))
        except BaseException as e:
            pass
        finally:
            pass

    def get_item(self):
        return '/item/' + str(self.inv)


class Item(models.Model):
    class Meta:
        abstract = True
        ordering = ["-date"]
    name = models.CharField(max_length=100, verbose_name='Название', help_text='Введите название', default='')
    availability = models.CharField(max_length=100, verbose_name='Наличие', choices=available, default=available[0])
    photo = models.ImageField(verbose_name='Главное фото', upload_to=upload_path, blank=False, help_text='Обязательное поле')
    photo1 = models.ImageField(verbose_name='Фото 1', upload_to=upload_path, blank=True)
    photo2 = models.ImageField(verbose_name='Фото 2', upload_to=upload_path, blank=True)
    photo3 = models.ImageField(verbose_name='Фото 3', upload_to=upload_path, blank=True)
    photo4 = models.ImageField(verbose_name='Фото 4', upload_to=upload_path, blank=True)
    photo5 = models.ImageField(verbose_name='Фото 5', upload_to=upload_path, blank=True)
    video = models.URLField(verbose_name='Видеообзор', blank=True, help_text='Введите адрес YouTube видео')
    description = models.TextField(verbose_name='Описание', max_length=1500, blank=True)
    date = models.DateTimeField(auto_now_add=True, editable=False)
    price = models.DecimalField(verbose_name='Цена в розницу', max_digits=20, decimal_places=2, help_text='Обязательное поле')
    price_opt = models.DecimalField(verbose_name='Цена оптом', max_digits=20, decimal_places=2, default=0, help_text='Если не надо - оставить нулём')

    diagonal = models.DecimalField(verbose_name='Диагональ', default=0, max_digits=20, decimal_places=2, blank=True, help_text='Диагональ в дюймах')
    resolution = models.CharField(verbose_name='Разрешение экрана', max_length=50, blank=True, help_text='Вводить через англискую букву \'x\'')
    display_other = models.CharField(verbose_name='Дисплей дополнительно', max_length=200, blank=True)

    wireless = models.CharField(verbose_name='Беспроводные возможности', max_length=500, blank=True)

    interfaces = models.CharField(verbose_name='Интерфейсы и подключения', max_length=500, blank=True)

    battery = models.IntegerField(verbose_name='Ёмкость батареи', default=0, blank=True, help_text='Ёмкость батареи в mah')

    camera = models.IntegerField(verbose_name='Размер камеры', default=0, blank=True, help_text='Размер камеры в МП')
    camera_other = models.CharField(verbose_name='Камера дополнительно', max_length=100, blank=True)

    osystem = models.CharField(verbose_name='Операционная система', max_length=500, blank=True)
    count_core = models.IntegerField(verbose_name='Количесво ядер', choices=cores, default=cores[0])
    core_other = models.CharField(verbose_name='Процессор', max_length=200, blank=True)
    ram = models.IntegerField(verbose_name='Оперативная память', default=0, blank=True, help_text='Размер в МБ')
    memory = models.IntegerField(verbose_name='Внутреняя память', default=0, blank=True, help_text='Размер в ГБ')
    memory_other = models.CharField(verbose_name='Память дополнительно', max_length=200, blank=True)

    other = models.CharField(verbose_name='Дополнительно', max_length=200, blank=True)
    link_items = models.ForeignKey(Items, default=1, editable=False)
    inv = models.IntegerField(editable=False, default=get_inv, primary_key=True)
    likes = models.IntegerField(editable=False, default=0)

    def __str__(self):
        return self.name

    def get_thumb(self):
        url = self.photo.url
        url = url.split('.')
        thumb_url = url[0] + '_thumb.' + url[1]
        return thumb_url

    def delete(self, *args, **kwargs):
        shares = Share.objects.filter((Q(gen_item__exact=self.inv) | Q(sec_item__exact=self.inv)))
        if shares:
            for share in shares:
                share.delete()
        path = '{0}/{1}/{2}/'.format(MEDIA_ROOT, self.link_category_id, self.name)
        print(path)
        try:
            for file in listdir(path):
                remove(path + file)
            rmdir(path)
        except BaseException:
            pass
        super(Item, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super(Item, self).save(*args, **kwargs)
        try:
            compress_img(self.photo.path, (250, 250))
            compress_img(self.photo.path, (800, 600))
            photos = [self.photo1, self.photo2,
                      self.photo3, self.photo4,
                      self.photo5]
            for photo in photos:
                if photo != '':
                    compress_img(photo.path, (800, 600))
        except BaseException as e:
            pass
        finally:
            pass

    def get_item(self):
        return '/item/' + str(self.inv)


class Phone(Item):
    standards = models.CharField(verbose_name='Стандарты и технологии', max_length=500, blank=True)
    front_camera = models.IntegerField(verbose_name='Размер фронтальной камеры', default=0, blank=True, help_text='Размер камеры в МП')
    front_camera_other = models.CharField(verbose_name='Камера фронтальная дополнительно', max_length=100, blank=True)
    sim_count = models.IntegerField(verbose_name='Количество сим', default=1, blank=True)
    link_category = models.ForeignKey(Category, default=1, editable=False)


class Tablet(Item):
    standards = models.CharField(verbose_name='Стандарты и технологии', max_length=100, blank=True)
    front_camera = models.IntegerField(verbose_name='Размер фронтальной камеры', default=0, blank=True)
    front_camera_other = models.CharField(verbose_name='Камера фронтальная дополнительно', max_length=100, blank=True)
    sim_count = models.IntegerField(verbose_name='Количество сим', default=0, blank=True)
    link_category = models.ForeignKey(Category, default=2, editable=False)


class Notebook(Item):
    gpu = models.CharField(verbose_name='Видеокарта', max_length=300, blank=True, default='')
    optical_privod = models.CharField(verbose_name='Оптический привод', max_length=300, blank=True, default='')
    link_category = models.ForeignKey(Category, default=3, editable=False)


class Accessories(Other):
    link_category = models.ForeignKey(Category, limit_choices_to={'variant': 1}, verbose_name='Категория')


class ForMaster(Other):
    link_category = models.ForeignKey(Category, limit_choices_to={'variant': 2})


class ForHome(Other):
    link_category = models.ForeignKey(Category, limit_choices_to={'variant': 3})


class Slide(models.Model):
    img = models.ImageField(upload_to=get_uniq_name, blank=True, verbose_name='Изображение слайда')
    link = models.URLField(verbose_name='Ссылка', blank=True, default='', help_text='Если ссылка не нужна оставить пустым')

    def save(self, *args, **kwargs):
        super(Slide, self).save(*args, **kwargs)
        try:
            path = self.img.path
            img = PIL.Image.open(path)
            resized_image = img.resize((900, 400), PIL.Image.BILINEAR)
            resized_image.save(path)
        except BaseException as e:
            print(e)
        finally:
            pass

    def __str__(self):
        return 'Слайд' + str(self.id)

    def delete(self, *args, **kwargs):
        remove(self.img.path)
        super(Slide, self).delete(*args, **kwargs)


class Share(models.Model):
    name = models.CharField(default='', editable=False, max_length=600)
    price = models.DecimalField(default=0, max_digits=20, decimal_places=2, editable=False)
    inv = models.IntegerField(editable=False, null=False, default=get_inv, primary_key=True, unique=True)
    gen_item = models.IntegerField(blank=False)
    sec_item = models.IntegerField(blank=False)
    discount = models.IntegerField(blank=False)

    def clean(self):
        if self.gen_item == self.sec_item:
            raise ValidationError('Первый и второй не могут быть равны')

    def save(self, *args, **kwargs):
        gen_item = get_item(self.gen_item)
        sec_item = get_item(self.sec_item)
        self.name = '{0} + {1} (скидка: -{2}%)'.format(gen_item.name, sec_item.name, str(self.discount))
        self.price = gen_item.price + (sec_item.price - (sec_item.price / 100 * self.discount))
        super(Share, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Client(models.Model):
    email = models.EmailField(unique=True)
    discount = models.IntegerField(default=0, verbose_name='Скидка')


class Order(models.Model):
    class Meta:
        ordering = ['-id']
    email = models.EmailField(verbose_name='e-mail', help_text='На ваш e-mail будут отправлены реквизиты')
    phone = models.CharField(verbose_name='Номер телефона', max_length=30, blank=True)
    items = models.BinaryField(default=b'none', editable=False)
    message = models.TextField(verbose_name='Сообщение', blank=True)
    date = models.DateField(auto_now_add=True)
    link_client = models.ForeignKey(Client, blank=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today())

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'User profiles'


class Info(models.Model):
    text = models.TextField(blank=False, default='')
