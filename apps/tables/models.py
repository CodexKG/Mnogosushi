from django.db import models
from io import BytesIO
from django.core.files import File
import uuid, qrcode

from apps.products.models import Product

# Create your models here.
class Table(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name="Заголовок"
    )
    number = models.IntegerField(
        verbose_name="Номер стола",
        unique=True,
        blank=True, null=True
    )
    qr_code_image = models.ImageField(
        verbose_name="QR код",
        upload_to="qr_codes/",
        blank=True, null=True
    )
    created = models.DateTimeField(
        verbose_name="Дата добавления",
        auto_now_add=True
    )

    def __str__(self):
        return str(self.number)
    
    def save(self, *args, **kwargs):
        if not self.number:
            self.number = str(uuid.uuid4().int)[:5]  # Генерируем UUID и оставляем только первые 20 цифр
            print("GENERATE UUID")
            print(self.number)
        if not self.qr_code_image:  # Генерируем QR-код только если он еще не существует
            self.generate_qr_code()
        super().save(*args, **kwargs)

    def generate_qr_code(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(f"http://mnogosushi.kg/menu/{self.number}/")
        qr.make(fit=True)

        buffer = BytesIO()
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(buffer, "PNG")

        # Сохранение файла QR-кода в поле qr_code_image
        filename = f"table_{self.number}_qr.png"
        self.qr_code_image.save(filename, File(buffer), save=False)

    class Meta:
        verbose_name = "Стол"
        verbose_name_plural = "Столы"

class TableOrder(models.Model):
    menu_table = models.ForeignKey(Table, on_delete=models.SET_NULL, verbose_name="Стол", blank=True, null=True)
    session_key = models.CharField(max_length=40, unique=True, verbose_name="Ключ сессии")
    items = models.ManyToManyField(Product, through='TableOrderItem', verbose_name="Товары")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата формирования заказа")

    def __str__(self):
        return f"{self.session_key}"
    
    class Meta:
        verbose_name = "Корзина (меню)"
        verbose_name_plural = "Корзины (меню)"

class TableOrderItem(models.Model):
    table = models.ForeignKey(TableOrder, on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество товара")
    total = models.PositiveBigIntegerField(default=0, verbose_name="Итоговая цена товаров")

    def __str__(self):
        return f"{self.table}"
    
    class Meta:
        verbose_name = "Товар в корзине (меню)"
        verbose_name_plural = "Товары в корзине (меню)"