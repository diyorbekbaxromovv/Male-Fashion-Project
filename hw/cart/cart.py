from main.models import Product
class Cart:
    def __init__(self, request):
        self.session = request.session
        
        cart = self.session.get('session_key')
        
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
            
        self.cart = cart    
        
        
    def add(self, product, quantity):
        product_id = str(product.id)
        prod_count = str(quantity)
        
        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = prod_count 
            
        self.session.modified = True
        
    def __len__(self):
        return len(self.cart)
    
    def get_product(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products
    
    def get_quantity(self):
        return self.cart

    def update(self, product, quantity):
        product_id = str(product)
        prod_count = int(quantity)

        self.cart[product_id] = prod_count
        self.session.modified = True
        return self.cart
    
    def delete(self, product_id):
        product_id = str(product_id)
        
        if product_id in self.cart:
            del self.cart[product_id]
            
        self.session.modified = True 
        
        
    def get_total(self):
        if any(int(value) < 0 for value in self.cart.values()):
            raise ValueError("Hatolik")
    
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        
        total = 0

        for key,value in self.cart.items():
            key=int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (int(value)*product.sale_price)
                    else:
                        total = total + (int(value)*product.price)
        return total
    
    def get_product_total(self,product_id, quantity):
        try:
            product = Product.objects.get(id=product_id)
            if product.is_sale:
                total = quantity * product.sale_price
            else:
                total = quantity * product.price
            return total
        except Product.DoesNotExist:
            return 0
        
        
    def get_all_info(self):
        products = self.get_product()
        quantity = self.get_quantity()     
    
        result = []
        
        for product in products:
            if str(product.id) in quantity:
                data = {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'quantity': quantity[str(product.id)],
                    
                }
                result.append(data)
                
        return result
        
        
    def cart_clear(self):
        self.cart.clear()
        self.session.modified = True
        return self.cart