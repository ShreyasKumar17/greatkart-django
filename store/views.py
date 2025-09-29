from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404
from carts.models import CartItem
from category.models import Category
from orders.models import OrderProduct
from .models import Product, ReviewRating
from carts.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator  
from django.db.models import Q  
from .forms import ReviewForm

# Create your views here.

def store(request, category_slug=None):
    category = None
    products = None

    if category_slug != None:
        category = get_object_or_404(Category, Slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True)
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html',context)

def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__Slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
        
    except Exception as e:
        raise e
    
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user = request.user, product_id = single_product.id).exists() # type: ignore
        except OrderProduct.DoesNotExist:
            orderproduct = None
    
    else:
        orderproduct = None

    #Get the reviews
    reviews = ReviewRating.objects.filter(product=single_product, status=True)


    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'orderproduct': orderproduct,
        'reviews': reviews,
    }
    
    return render(request, 'store/product_detail.html',context)
    

def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            products = Product.objects.order_by('-created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = products.count()
    
    context = {
        'products': products,
        'product_count': product_count,
    }
    return render(request, 'store/store.html', context)




def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER', '/')
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        try:
            # Try to get an existing review
            review_instance = ReviewRating.objects.get(user=request.user, product=product)
        except ReviewRating.DoesNotExist:
            # Create a new empty review object
            review_instance = ReviewRating()

        form = ReviewForm(request.POST, instance=review_instance)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.ip = request.META.get('REMOTE_ADDR')
            review.save()

            if review_instance.id: # type: ignore
                messages.success(request, "Thank you! Your review has been updated.")
            else:
                messages.success(request, "Thank you! Your review has been submitted.")
        else:
            messages.error(request, f"Error: {form.errors}")

        return redirect(url)
