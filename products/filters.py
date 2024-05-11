from .models import Product
from inquiry.models import ForeignProduct
#---------------------------
def shop_products():
        foreign_products = ForeignProduct.objects.all()
        foreign_products_ids = [o.id for o in foreign_products]
        products = Product.objects.all()
        products_ids = [o.id for o in products if not o.id in foreign_products_ids]

        products_filtered = products.filter(id__in=products_ids)
        return products_filtered
#---------------------------