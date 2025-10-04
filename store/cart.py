class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, book_id):
        book_id = str(book_id)
        if book_id in self.cart:
            self.cart[book_id] += 1
        else:
            self.cart[book_id] = 1
        self.save()

    def remove(self, book_id):
        book_id = str(book_id)
        if book_id in self.cart:
            del self.cart[book_id]
            self.save()

    def save(self):
        self.session.modified = True

    def get_items(self):
        return self.cart