import json
import os
from store.models import DATABASE


def filtering_category(database: dict[str, dict],
                       category_key: [None, str] = None,
                       ordering_key: [None, str] = "rating",
                       reverse: bool = False):
    """
    Функция фильтрации данных по параметрам

    :param database: База данных. (словарь словарей. При проверке в качестве database будет передаваться словарь DATABASE из models.py)
    :param category_key: [Опционально] Ключ для группировки категории. Если нет ключа, то рассматриваются все товары.
    :param ordering_key: [Опционально] Ключ по которому будет произведена сортировка результата.
    :param reverse: [Опционально] Выбор направления сортировки:
        False - сортировка по возрастанию;
        True - сортировка по убыванию.
    :return: list[dict] список товаров с их характеристиками, попавших под условия фильтрации. Если нет таких элементов,
    то возвращается пустой список
    """
    if category_key is not None:
        result = [product for product in DATABASE.values() if category_key == product['category']]
    else:
        result = list(DATABASE.values())
    if ordering_key is not None:
        result.sort(key=lambda x: x[ordering_key], reverse=reverse)
    print(result)
    return result


def view_in_cart() -> dict:
    """
    Просматривает содержимое cart.json

    :return: Содержимое 'cart.json'
    """
    if os.path.exists('cart.json'):  # Если файл существует
        with open('cart.json', encoding='utf-8') as f:
            return json.load(f)

    cart = {'products': {}}  # Создаём пустую корзину
    with open('cart.json', mode='x', encoding='utf-8') as f:  # Создаём файл и записываем туда пустую корзину
        json.dump(cart, f)

    return cart


def add_to_cart(id_product: str) -> bool:
    """
    Добавляет продукт в корзину. Если в корзине нет данного продукта, то добавляет его с количеством равное 1.
    Если в корзине есть такой продукт, то добавляет количеству данного продукта + 1.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного добавления, а False в случае неуспешного добавления(товара по id_product
    не существует).
    """

    cart = view_in_cart()
    if id_product in DATABASE.keys():
        if id_product in cart["products"].keys():
            cart["products"][id_product] += 1
        else:
            cart["products"][id_product] = 1
        with open('cart.json', mode='w', encoding='utf-8') as f:
            json.dump(cart, f)
    if id_product not in DATABASE.keys():
        return False

    return True


def remove_from_cart(id_product: str) -> bool:
    """
    Добавляет позицию продукта из корзины. Если в корзине есть такой продукт, то удаляется ключ в словаре
    с этим продуктом.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного удаления, а False в случае неуспешного удаления(товара по id_product
    не существует).
    """
    cart = view_in_cart()
    if id_product in cart['products'].keys():
        del cart['products'][id_product]
        with open('cart.json', mode='w', encoding='utf-8') as f:
            json.dump(cart, f)
    else:
        return False

    return True


if __name__ == "__main__":
    # from store.models import DATABASE
    #
    # test = [
    #     {'name': 'Клубника', 'discount': None, 'price_before': 500.0,
    #      'price_after': 500.0,
    #      'description': 'Сладкая и ароматная клубника, полная витаминов, чтобы сделать ваш день ярче.',
    #      'rating': 5.0, 'review': 200, 'sold_value': 700,
    #      'weight_in_stock': 400,
    #      'category': 'Фрукты', 'id': 2, 'url': 'store/images/product-2.jpg',
    #      'html': 'strawberry'},
    #
    #     {'name': 'Яблоки', 'discount': None, 'price_before': 130.0,
    #      'price_after': 130.0,
    #      'description': 'Сочные и сладкие яблоки - идеальная закуска для здорового перекуса.',
    #      'rating': 4.7, 'review': 30, 'sold_value': 70, 'weight_in_stock': 200,
    #      'category': 'Фрукты', 'id': 10, 'url': 'store/images/product-10.jpg',
    #      'html': 'apple'}
    # ]
    #
    # print(filtering_category(DATABASE, 'Фрукты', 'rating', True) == test)  # True
    print(view_in_cart())  # {'products': {}}
    print(add_to_cart('1'))  # True
    print(add_to_cart('0'))  # False
    print(add_to_cart('1'))  # True
    print(add_to_cart('2'))  # True
    print(view_in_cart())  # {'products': {'1': 2, '2': 1}}
    print(remove_from_cart('0'))  # False
    print(remove_from_cart('1'))  # True
    print(view_in_cart())  # {'products': {'2': 1}}
    print(add_to_cart('1'))
