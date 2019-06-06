from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.http import request
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from .forms import CustomUserCreationForm
from django.conf import settings


from .models import Category, SubCategory, Article, Product, User, Order
from .forms import ReviewForm, ReviewFormset


# Предоставление контекста для меню
def base_view(context):
    context['cats'] = Category.objects.all()


def index(request):

    context = {}
    base_view(context)
    context['articles'] = Article.objects.all()

    return render(request, './resources/index.html', context)


def empty_section(request):

    context = {}
    base_view(context)
    return render(request, './resources/empty_section.html', context)


def cart_view(request):
    if not request.user.is_authenticated:
        # print('REDIRECT TO LOGIN PAGE')
        return redirect('login_form')

    if 'products_in_cart' not in request.session:
        request.session['products_in_cart'] = []

    session_products = request.session['products_in_cart']
    context = {}
    base_view(context)

    if request.method == 'POST':

        # Нажата кнопка 'Заказать' и корзина не пуста
        if 'button' in request.GET and session_products != []:
            order = Order(
                          customer=request.user,
                          is_ordered=True,
                          )
            order.save()

            for id in session_products:
                product = Product.objects.get(id=id)
                order.products.add(product)
            order.save()

            request.session['products_in_cart'] = []
            context['is_ordered'] = 'Ваш заказ оформлен'
            return render(request, './resources/cart.html', context)

        else:
            product_name = request.GET.get('id')

            # Проверка, если страница оформленного заказа была обновлена(F5)
            if product_name is not None:
                request.session.modified = True
                request.session['products_in_cart'].append(product_name)

        return redirect('cart')

    if request.method == 'GET':

        # unique_products = Product.objects.filter(slug__in=session_products)
        unique_products = Product.objects.filter(id__in=session_products)

        products = []

        if session_products is not None:

            for id in session_products:
                product = unique_products.get(id=id)
                products.append(
                    {'name': product.name, 'description': product.description})

        context['products'] = products
        return render(request, './resources/cart.html', context)


class ProductList(ListView):
    model = Product
    paginate_by = 2

    template_name = './resources/product_list.html'
    context_object_name = 'products'

    # Ограничение списка товаров по подкатегории
    def get_queryset(self):
        return Product.objects.filter(
            sub_category__name=self.request.GET.get('sub_category')).order_by('slug')

    # Передача в контекст сайт-меню и названия выбранной подкатегории
    def get_context_data(self):
        context = super().get_context_data()
        base_view(context)
        context['sub_category'] = self.request.GET.get('sub_category')
        return context

    # Альтернативная пагинация
    # def get(self, request, *args, **kwargs):
    #
    #     paginator = Paginator(self.get_queryset(), self.paginate_by)
    #     current_page_number = request.GET.get('page')
    #     current_page = paginator.get_page(current_page_number)
    #     context = {}
    #     base_view(context)
    #     context['sub_category'] = self.request.GET.get('sub_category')
    #     context['products'] = current_page
    #
    #     return render(request, './resources/product_list.html', context)


class ProductView(DetailView):
    model = Product

    context = {}
    base_view(context)

    def post(self, request, *args, **kwargs):

        form = ReviewForm(request.POST)

        if form.is_valid():
            form.save()

        return HttpResponseRedirect(request.get_full_path())

    def get(self, request, *args, **kwargs):

        form = ReviewFormset()
        self.context['product'] = Product.objects.get(id=request.GET.get('id'))
        self.context['form'] = form
        return render(request, './resources/product_view.html', self.context)


def logging_in(request):

    if request.method == 'POST':

        user = authenticate(request,
                            email=request.POST.get('email'),
                            password=request.POST.get('password'))
        login(request, user)
        return redirect('index')

    if request.method == 'GET':

        context = {}
        base_view(context)

        return render(request, './resources/login.html', context)


def logout_action(request):

    logout(request)
    return redirect('index')


def signup(request):

    if request.method == 'POST':
        reg_form = CustomUserCreationForm(request.POST)
        if reg_form.is_valid():
            user = reg_form.save()
            login(request, user)
        return redirect('index')
    else:
        reg_form = CustomUserCreationForm()
        context = {}
        base_view(context)
        context['form'] = reg_form
    return render(
        request,
        './resources/signup.html', context
    )



