from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Book, CartItem, WishlistItem
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.http import require_POST
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from .models import WishlistItem

def home(request):
    best_sellers = Book.objects.filter(is_bestseller=True)
    return render(request, 'store/home.html', {
        'best_sellers': best_sellers,
        'user': request.user  # optional, for prefill
    })


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, 'store/book_detail.html', {'book': book})


def books_by_category(request, name):
    books = Book.objects.filter(category__iexact=name)
    return render(request, 'store/category.html', {'books': books, 'category': name})

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def cart_view(request):
    items = CartItem.objects.filter(user=request.user)
    total = 0
    for item in items:
        item.subtotal = item.book.price * item.quantity
        total += item.subtotal
    return render(request, 'store/cart.html', {'items': items, 'total': total})

@login_required
def wishlist_view(request):
    items = WishlistItem.objects.filter(user=request.user)
    return render(request, 'store/wishlist.html', {'items': items})

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, book=book)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    messages.success(request, f"{book.title} added to cart.")
    return redirect(request.META.get('HTTP_REFERER', 'home'))





@login_required
def add_to_wishlist(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    WishlistItem.objects.get_or_create(user=request.user, book=book)
    messages.success(request, f"{book.title} added to your wishlist.")
    return redirect('book_detail', book_id=book_id)

@login_required
def move_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, book=book)
    if not created:
        cart_item.quantity += 1
    cart_item.save()

    # Now remove from wishlist
    WishlistItem.objects.filter(user=request.user, book=book).delete()

    messages.success(request, f"{book.title} moved to cart.")
    return redirect('wishlist')


@require_POST
@login_required

def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        item.quantity = quantity
        item.save()
    else:
        item.delete()
    return redirect('cart')

from .models import Order, OrderItem

@login_required
def order_history_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/order_history.html', {'orders': orders})

def remove_from_wishlist(request, book_id):
    WishlistItem.objects.filter(user=request.user, book_id=book_id).delete()
    messages.success(request, "Removed from wishlist.")
    return redirect('wishlist')

def search_books(request):
    query = request.GET.get('q', '')
    results = Book.objects.filter(
        Q(title__icontains=query) |
        Q(author__icontains=query) |
        Q(category__icontains=query)
    )
    return render(request, 'store/search_results.html', {'results': results, 'query': query})

@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user)
    wishlist = WishlistItem.objects.filter(user=request.user)
    return render(request, 'store/profile.html', {
        'user': request.user,
        'orders': orders,
        'wishlist': wishlist
    })



@login_required
def checkout_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.book.price * item.quantity for item in cart_items)
    amount_paise = int(total * 100)

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    payment = client.order.create({
        'amount': amount_paise,
        'currency': 'INR',
        'payment_capture': '1'
    })

    context = {
        'cart_items': cart_items,
        'total': total,
        'amount': amount_paise,
        'razorpay_order_id': payment['id'],
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
    }
    return render(request, 'store/checkout.html', context)


@login_required
def profile_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    wishlist = WishlistItem.objects.filter(user=request.user)
    return render(request, 'store/profile.html', {
        'user': request.user,
        'orders': orders,
        'wishlist': wishlist
    })
    

@csrf_exempt
def payment_success(request):
    # Optional: verify Razorpay signature here
    CartItem.objects.filter(user=request.user).delete()
    messages.success(request, "Payment successful! Your order is confirmed.")
    return redirect('order_history')

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
print(client.order.all())