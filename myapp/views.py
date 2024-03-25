from django.shortcuts import render
from django.http import HttpResponse,HttpResponseBadRequest
from .models import *
from django.contrib.auth import authenticate, login as auth_login

# Create your views here.

def index(request):
    products = Product.objects.all()

    # Pass the products to the template for rendering
    return render(request, 'myapp/index.html', {'products': products})

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, UserProfileForm

def register(request):
      if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            auth_login(request, user)
            return redirect('login')  # Replace 'home' with the actual URL name for your home page
      else:
           user_form = UserRegistrationForm()
           profile_form = UserProfileForm()

      return render(request, 'myapp/register.html', {'user_form': user_form, 'profile_form': profile_form})
      

def login(request):
     if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            auth_login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')  # Redirect superuser to admin dashboard
            else:
                return redirect('category')  # Redirect normal user to user dashboard
        else:
             error_message = 'Invalid login credentials'
             return render(request, 'myapp/login.html', {'error': error_message})
     else:
       return render(request, 'myapp/login.html')

def admin_dashboard(request):
    return render(request,'myapp/admin_dashboard.html')

from .forms import CategoryForm
from django.contrib import messages

def category_add(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect('viewCategory')  # Replace 'home' with the actual URL name for your home page
    else:
        form = CategoryForm()

    return render(request, 'myapp/categoryadd.html', {'form': form})

from .models import Category

def viewCategory(request):
      categories = Category.objects.all()
      print(categories)
      return render(request, 'myapp/viewCategory.html', {'categories': categories})

from django.shortcuts import render, redirect, get_object_or_404

def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    
    category.delete()
    return redirect('viewCategory')

def edit_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('viewCategory')
    else:
        form = CategoryForm(instance=category)

    return render(request, 'myapp/editCategory.html', {'form': form, 'category': category})

from .forms import ProductForm

def addProduct(request):
     if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Redirect to the product detail page or any other desired page
            return redirect('viewProduct')  # Replace 'product_detail' with your actual URL name
     else:
        form = ProductForm()

    # Retrieve categories for the dropdown
     categories = Category.objects.all()
     return render(request, 'myapp/addProduct.html', {'form': form, 'categories': categories})

from .models import Product
def viewProduct(request):
    products = Product.objects.all()
    return render(request, 'myapp/viewProduct.html', {'products': products})


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.delete()
        return redirect('viewProduct')

    
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('viewProduct')
    else:
        form = ProductForm(instance=product)

    categories = Category.objects.all()
    return render(request, 'myapp/editProduct.html', {'form': form, 'product': product, 'categories': categories})    

def userDashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'myapp/userDashboard.html', {'user_profile': user_profile})

def category(request):
    cat = Category.objects.all()
    return render(request, 'myapp/category.html', {'cat': cat})

def products(request):
    category_id = request.GET.get("id")
    products = Product.objects.filter(category=category_id)
    return render(request, "myapp/view_products.html", {"products": products})

from django.contrib.auth import logout
def user_logout(request):
    logout(request)
    return redirect('login')

from django.contrib.auth.decorators import login_required

@login_required
def userProfile(request):
     user_profile = get_object_or_404(UserProfile, user=request.user)
     return render(request, 'myapp/userProfile.html', {'user_profile': user_profile})

@login_required
def userProfileUpdate(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('userProfile')

    else:
        user_form = UserRegistrationForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'myapp/userProfileUpdate.html', {'user_form': user_form, 'profile_form':profile_form})

@login_required
def update_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')

        # Check if the current password is correct
        if request.user.check_password(current_password):
            # Update the password
            request.user.userprofile.update_password(new_password)
            messages.success(request, 'Password updated successfully.')
        else:
            messages.error(request, 'Incorrect current password.')

        return redirect('update_password')

    return render(request, 'myapp/update_password.html')

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user_profile = UserProfile.objects.get(user=request.user)

    # Check if the product is already in the cart
    cart_item, created = Cart.objects.get_or_create(user_profile=user_profile, product=product)

    if not created:
        # If the product is already in the cart, increment the quantity
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, 'Product added to cart successfully.')
    return redirect('view_cart')

def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    user_profile = UserProfile.objects.get(user=request.user)

    # Check if the product is in the cart
    cart_item = Cart.objects.filter(user_profile=user_profile, product=product).first()

    if cart_item:
        # If the product is in the cart, decrement the quantity or remove it if quantity is 1
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

        messages.success(request, 'Product removed from cart successfully.')
    else:
        messages.warning(request, 'Product not found in your cart.')

    # Redirect to the view_cart page
    return redirect('view_cart')

def view_cart(request):
    user_profile = request.user.userprofile
    cart_items = Cart.objects.filter(user_profile=user_profile)
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
    }

    return render(request, 'myapp/view_cart.html', context)

def update_quantity(request, product_id, action):
    if action not in ['increase', 'decrease']:
        return HttpResponseBadRequest("Invalid action")

    user_profile = request.user.userprofile
    cart_item = get_object_or_404(Cart, user_profile=user_profile, product__id=product_id)

    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    else:
        return HttpResponseBadRequest("Invalid action")

    cart_item.save()

    return redirect('view_cart')

# views.py
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
import razorpay
from .models import UserProfile, Address


razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_SECRET_KEY))

def create_razorpay_order(amount):
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    order = client.order.create({'amount': amount * 100, 'currency': 'INR'})
    return order['id']


def create_address(request):
    user_profile = request.user.userprofile
    cart_items = Cart.objects.filter(user_profile=user_profile)
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        # Get data from the request
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        zip_code = request.POST.get('zip_code')

        # Create an address instance but don't save it yet
        new_address = Address(
            user_profile=user_profile,
            street_address=street_address,
            city=city,
            zip_code=zip_code
        )
        
        # Save the address
        new_address.save()

        # Redirect to Razorpay payment page with total_amount as a parameter
        return redirect('razorpay_payment', total_amount=total_amount)  

    context = {
        'total_amount': total_amount,
    }

    return render(request, 'myapp/address.html', context)
        

def get_razorpay_client():
    return razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_SECRET_KEY))

def razorpay_payment(request, total_amount):
    user_profile = request.user.userprofile
    cart_items = Cart.objects.filter(user_profile=user_profile)
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    # Initialize Razorpay client
    razorpay_client = get_razorpay_client()

    # Create an order
    order_data = {
        'amount': total_amount * 100,  # Razorpay amount is in paisa, so multiply by 100
        'currency': 'INR',
        'payment_capture': 1,  # Automatically capture the payment
    }
    order = razorpay_client.order.create(data=order_data)

    # Additional information for the context
    additional_info = {
        'user_profile': user_profile,
        'cart_items': cart_items,
    }

    context = {
        'order_id': order['id'],
        'total_amount_in_paise': total_amount ,
    }

    return render(request, 'myapp/razorpay_payment.html', context)

from django.utils import timezone

def payment_success(request):
    try:
        # Get the order ID from the query parameters
        order_id = request.GET.get('razorpay_order_id')

        # Check if the order ID is provided
        if not order_id:
            raise ValueError("Order ID is missing from the URL parameters.")

        # Fetch the order details from Razorpay
        order = razorpay_client.order.fetch(order_id)
        
        # Extract relevant information
        total_amount = order['amount'] / 100  # Convert amount from paisa to rupees
        user_profile = request.user.userprofile
        cart_items = Cart.objects.filter(user_profile=user_profile)

        # Create a purchase record
        purchase = Purchase.objects.create(
            order_id=order_id,
            user_profile=user_profile,
            address=user_profile.addresses.last(),  # Assuming you want to use the latest address
            quantity=0  # Initialize quantity to 0
        )

        # Initialize total quantity
        total_quantity = 0

        # Iterate over cart items to create purchase items and update total quantity
        for cart_item in cart_items:
            # Create a purchase item for each product in the cart
            purchase_item = PurchaseItem.objects.create(
                product=cart_item.product,
                purchase=purchase,
                quantity=cart_item.quantity,
                user_profile=user_profile,  # Set the user_profile here
                address=user_profile.addresses.last()  # Assuming you want to use the latest address for each purchase item
            )

            # Accumulate total quantity
            total_quantity += cart_item.quantity

            # Decrease the quantity of the Product
            product = cart_item.product
            product.quantity -= cart_item.quantity
            product.save()

        # Update the total quantity in the Purchase model
        purchase.quantity = total_quantity
        purchase.save()

        # Clear the user's cart
        cart_items.delete()

        # Render the success page with relevant information
        context = {
            'order_id': order_id,
            'total_amount': str(total_amount),  # Convert to string
            'purchase_date': str(purchase.purchase_date),  # Convert to string
        }

        return render(request, 'myapp/payment_success.html', context)

    except Exception as e:
        # Print the error to the console for debugging
        print(f"An error occurred: {e}")

        # Handle any exceptions and redirect to the failure page
        messages.error(request, f"An error occurred: {str(e)}")
        return redirect('payment_failed')


    
    
def payment_failed(request):
    # Add any additional logic or data processing for failed payments
    return render(request, 'myapp/payment_failed.html')


from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph
from django.core.files.base import ContentFile
from django.shortcuts import render
from .models import Purchase

def purchase_history(request):
    user_profile = request.user.userprofile
    purchase_history = Purchase.objects.filter(user_profile=user_profile)

    context = {
        'user_profile': user_profile,
        'purchase_history': purchase_history,
    }

    return render(request, 'myapp/purchase_history.html', context)

def generate_purchase_pdf(purchase):
    # Create a PDF buffer
    buffer = BytesIO()

    # Create a PDF document object
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading1']
    normal_style = styles['Normal']
    product_style = ParagraphStyle(name='ProductStyle', parent=normal_style, leftIndent=20)

    # Create content for the PDF
    content = []

    # Add title
    title_text = f"Purchase Details for Order ID: {purchase.order_id}"
    content.append(Paragraph(title_text, title_style))

    # Add purchase details
    content.append(Paragraph(f"Order ID: {purchase.order_id}", normal_style))
    content.append(Paragraph(f"Purchase Date: {purchase.purchase_date}", normal_style))
    content.append(Paragraph(f"Address: {purchase.address.street_address}, {purchase.address.city}, {purchase.address.zip_code}", normal_style))
    content.append(Paragraph(f"Total Quantity: {purchase.quantity}", normal_style))

    # Add product details
    content.append(Paragraph("Product Details:", heading_style))
    for item in purchase.purchaseitem_set.all():
        product_details = f"<b>Product:</b> {item.product.name}<br/><b>Price:</b> {item.product.price}<br/><b>Quantity:</b> {item.quantity}<br/>"
        content.append(Paragraph(product_details, product_style))

    # Build the PDF
    doc.build(content)

    # Rewind the buffer to the beginning
    buffer.seek(0)

    # Create a ContentFile from the buffer
    pdf_file = ContentFile(buffer.getvalue())

    return pdf_file


def download_purchase_pdf(request, purchase_id):
    try:
        purchase = Purchase.objects.get(pk=purchase_id)
        pdf_file = generate_purchase_pdf(purchase)

        # Set response content type
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        
        # Set content disposition (downloadable)
        response['Content-Disposition'] = f'attachment; filename=Purchase_{purchase.order_id}.pdf'

        return response
    except Purchase.DoesNotExist:
        return HttpResponse("Purchase not found.", status=404)
    



def delete_purchase(request, purchase_id):
    try:
        purchase = Purchase.objects.get(id=purchase_id)
        # Check if the purchase belongs to the logged-in user
        if purchase.user_profile.user == request.user:
            purchase.delete()
            messages.success(request, 'Purchase deleted successfully.')
        else:
            messages.error(request, 'You are not authorized to delete this purchase.')
    except Purchase.DoesNotExist:
        messages.error(request, 'Purchase does not exist.')
    
    return redirect('purchase_history')

def purchase_detail(request, purchase_id):
    purchase = Purchase.objects.get(pk=purchase_id)
    response = HttpResponse(content_type='application/pdf')

    # Call the function to generate the PDF for the specific purchase
    generate_purchase_pdf(response, purchase)

    return response

def all_purchases(request):
    # Get all purchases with related data
    all_purchases = Purchase.objects.select_related('user_profile', 'address').prefetch_related('products')

    # Create a list to store purchase details
    purchase_details = []

    # Extract information for each purchase
    for purchase in all_purchases:
        purchase_info = {
            'order_id': purchase.order_id,
            'username': purchase.user_profile.user.username,
            'products': [purchase_item.product.name for purchase_item in purchase.purchaseitem_set.all()],
            'quantity': purchase.quantity,
            'purchase_date': purchase.purchase_date,
            'address': str(purchase.address),  # Assuming Address model has a __str__ method defined
        }
        purchase_details.append(purchase_info)

    # Pass the details to the template
    context = {
        'purchase_details': purchase_details,
    }

    return render(request, 'myapp/all_purchases.html', context)

def admin_logout(request):
    logout(request)
    return redirect('login')

def user_list(request):
     user_profiles = UserProfile.objects.all()

    # Pass the user profiles to the template
     return render(request, 'myapp/userList.html', {'user_profiles': user_profiles})
 
 
 
def search(request):
    query = request.GET.get('q')

    if query:
        # Search for categories and products that match the query
        categories = Category.objects.filter(name__icontains=query)
        products = Product.objects.filter(name__icontains=query)
    else:
        categories = Category.objects.all()
        products = Product.objects.all()

    context = {
        'query': query,
        'categories': categories,
        'products': products,
    }

    return render(request, 'myapp/search.html', context)
