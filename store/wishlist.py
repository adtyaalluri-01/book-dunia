class Wishlist:
    def __init__(self, request):
        self.session = request.session
        wishlist = self.session.get('wishlist')
        if not wishlist:
            wishlist = self.session['wishlist'] = []
        self.wishlist = wishlist

    def add(self, book_id):
        book_id = str(book_id)
        if book_id not in self.wishlist:
            self.wishlist.append(book_id)
            self.save()

    def remove(self, book_id):
        book_id = str(book_id)
        if book_id in self.wishlist:
            self.wishlist.remove(book_id)
            self.save()

    def save(self):
        self.session.modified = True

    def get_items(self):
        return self.wishlist