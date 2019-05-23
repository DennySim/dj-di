from django.contrib import admin
from django.db.models import Count
from django.db import models
from django import forms
from .models import Product, Article, Category, SubCategory, Order,\
    OrderCountByCustomer, Review, User


class ReviewAdmin(admin.ModelAdmin):
    radio_fields = {'mark': admin.VERTICAL}


class ReviewAdminInline(admin.StackedInline):
    model = Review
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sub_category')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ReviewAdminInline, ]


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'pub_date')


class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


class SubCategoryAdminInline(admin.TabularInline):
    model = SubCategory
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    inlines = [SubCategoryAdminInline,]


class OrderAdmin(admin.ModelAdmin):

    formfield_overrides = {
        models.ManyToManyField: {'widget': forms.CheckboxSelectMultiple},
    }
    list_display = ('id', 'customer', 'order_date', 'is_ordered')


class OrderCountByCustomerAdmin(admin.ModelAdmin):

    change_list_template = 'admin/order_count_by_customer.html'
    readonly_fields = ('customer', 'products', 'is_ordered')

    def changelist_view(self, request):

        response = super().changelist_view(
            request
        )

        metrics = {
                'total_orders': Count('customer')
            }

        qs = Order\
            .objects.values('customer__email')\
            .annotate(**metrics)\
            .order_by('customer')[:3]

        response.context_data['summary'] = qs

        return response


class CustomUserAdmin(admin.ModelAdmin):
    model = User


admin.site.register(User, CustomUserAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Article, ArticleAdmin)

admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderCountByCustomer, OrderCountByCustomerAdmin)

