from daos.product_dao import ProductDAO
from models.product import Product

dao = ProductDAO()

def test_product_select():
    product_list = dao.select_all()
    assert len(product_list) >= 3

def test_product_insert():
    product = Product(None, 'iPhone 15', 'Apple', 1199.00)
    dao.insert(product)
    product_list = dao.select_all()
    names = [p.name for p in product_list]
    assert product.name in names

def test_product_update():
    product = Product(1, 'iPhone 15', 'Apple', 1199.00)
    assigned_id = dao.insert(product)

    corrected_price = 1099.00
    product.id = assigned_id
    product.price = corrected_price

    dao.update(product)

    product_list = dao.select_all()
    prices = [p.price for p in product_list]
    assert corrected_price in prices

def test_product_delete():
    product = Product(1, 'iPhone 15', 'Apple', 1199.00)
    dao.delete(product.id)
    product_list = dao.select_all()
    assert product not in product_list