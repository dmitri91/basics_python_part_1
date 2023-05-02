"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework_part_3.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(999) is True, 'Ожидаем True. quantity продукта больше запрашиваемого'
        assert product.check_quantity(1000) is True, 'Ожидаем True. quantity продукта равно запрашиваемому'
        assert product.check_quantity(1001) is False, 'Ожидаем False. quantity продукта меньше запрашиваемого'

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        product.buy(0)
        assert product.quantity == 1000, 'Некорректно вычисляется количество после покупки продуктов = 0шт'
        product.buy(100)
        assert product.quantity == 900, 'Некорректно вычисляется количество после покупки продуктов = 100шт'
        product.buy(900)
        assert product.quantity == 0, 'Некорректно вычисляется количество после покупки продуктов = 900шт'

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            assert product.buy(1001), 'Тип ошибки при покупки продукта не соответвует ValueError'


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product(self, cart, product):
        assert len(cart.products) == 0, 'Проверка наличия продуктов в корзине в начале добавления. Должна быть пустой'
        cart.add_product(product)
        assert cart.products[product] == 1, 'Ошибка подсчета количества в корзине при дефолтном добавлении продукта(=1)'
        cart.add_product(product, 10)
        assert cart.products[product] == 11, 'Ошибка подсчета количества в корзине при дополнении продукта'
        assert len(cart.products) == 1, 'Ошибка проверки количества типов продуктов в корзине'

    def test_remove_product(self, cart, product):
        cart.add_product(product, 500)
        cart.remove_product(product, 400)
        assert cart.products[product] == 100, 'Ошибка подсчета количества в корзине после удаления продукта(=400)'
        cart.remove_product(product)
        assert len(cart.products) == 0, 'Удаление продукта без указания количества'
        cart.add_product(product, 999)
        cart.remove_product(product, 1099)
        assert len(cart.products) == 0, 'Удаление продукта с указанием количества больше чем в корзине'
        cart.add_product(product, 300)
        cart.remove_product(product, 300)
        assert len(cart.products) == 0, 'Удаление продукта из корзины полностью'

    def test_clear(self,  cart, product):
        cart.add_product(product, 500)
        cart.clear()
        assert len(cart.products) == 0, 'Ошибка при очистки корзины'

    def test_get_total_price(self, cart, product):
        cart.add_product(product, 10)
        assert cart.get_total_price() == 1000, 'Ошибка подсчета стоимости товара в корзине'

    def test_buy_product(self, cart, product):
        cart.add_product(product, 10)
        cart.buy()
        assert len(cart.products) == 0, 'Удаление товара из корзины после покупки'

    def test_product_buy_more_than_available(self, cart, product):
        cart.add_product(product, 1001)
        with pytest.raises(ValueError):
            assert cart.buy(), 'Тип ошибки при покупки продукта не соответвует ValueError'
