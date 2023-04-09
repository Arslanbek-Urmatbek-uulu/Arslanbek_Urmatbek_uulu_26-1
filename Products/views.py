from django.shortcuts import render, redirect
from Products.forms import ProductCreateForm, CommentCreateForm
from Products.models import Product, Comment
from Products.constants import PAGINATION_LIMIT
from django.views.generic import ListView, CreateView, DetailView


class MainPageCBV(ListView):
    model = Product
    template_name = 'layouts/index.html'


class ProductsCBV(ListView):
    model = Product
    template_name = 'products/products.html'

    def get(self, request, **kwargs):
        products = self.get_queryset().order_by('-modified_date')
        search = request.GET.get('search')
        page = int(request.GET.get('page', 1))

        if search:
            products = products.filter(title__icontains=search) | products.filter(description__icontains=search)

        max_page = products.__len__() / PAGINATION_LIMIT
        if round(max_page) < max_page:
            max_page = round(max_page) + 1
        else:
            max_page = round(max_page)

        products = products[PAGINATION_LIMIT * (page - 1):PAGINATION_LIMIT * page]

        context = {
            'products': products,
            'user': request.user,
            'pages': range(1, max_page + 1)
        }

        return render(request, self.template_name, context=context)


class ProductsDetailCBV(DetailView, CreateView):
    model = Product
    template_name = 'products/detail.html'
    form_class = CommentCreateForm
    pk_url_kwarg = 'id'

    def get_context_data(self, *, objects_list=None, **kwargs):
        return {
            'product': self.get_object(),
            'comments': Comment.objects.filter(product=self.get_object()),
            'form': kwargs.get('form', self.form_class)
        }

    def post(self, request, **kwargs):
        form = CommentCreateForm(data=request.POST)

        if form.is_valid():
            Comment.objects.create(
                text=form.cleaned_data.get('text'),
                product_id=self.get_object().id
            )

            return redirect(f'/products/{self.get_object().id}')

        return render(request, self.template_name, context=self.get_context_data(form=form))


class ProductCreateCBV(ListView, CreateView):
    model = Product
    template_name = 'products/create.html'
    form_class = ProductCreateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'form': kwargs['form'] if kwargs.get('form') else self.form_class
        }

    def get(self, request, **kwargs):
        return render(request, self.template_name, context=self.get_context_data())

    def post(self, request, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            self.model.objects.create(
                title=form.cleaned_data.get('title'),
                description=form.cleaned_data.get('description'),
                rate=form.cleaned_data.get('rate'),
                image=form.cleaned_data.get('image')
            )
            return redirect('/products/')
        return render(request, self.template_name, context=self.get_context_data(form=form))
