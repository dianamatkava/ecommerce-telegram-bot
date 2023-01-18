from django.contrib import admin
from .models import (
    Category, Tag, Subcategory, Offer,
    OfferDetail, GiftOrder, TgUser, CurrencyDetail
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'ru_name']
    list_display = ['px_id', 'name', 'ru_name']
    list_filter = ['name', 'ru_name']
    search_fields = ['name', 'ru_name']
    list_display_links = ['px_id', 'name']
    
    
@admin.register(Subcategory)
class SubCategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'ru_name', 'category', 'faq']
    list_display = ['px_id', 'name', 'ru_name', 'category', 'faq']
    list_filter = ['category']
    search_fields = ['name', 'ru_name', 'category']
    list_display_links = ['px_id', 'name']
    
    
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ['name', 'description']
    list_display = ['px_id', 'name', 'description']
    list_filter = ['name']
    search_fields = ['name', 'ru_name']
    list_display_links = ['px_id', 'name']
    
    
@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('subcategory','category')
        }),
        ('Prices and Amount', {
            'fields': (
                'sell_cur', 'buy_cur',
                'margin', 'price_per_cur', 
            ),
        }),
        ('User Data', {
            'fields': (
                'username', 'score', 'user_timezone', 
                'payment_method_label', 'description',
                'warranty', 'offer_detail', 'created_at'
            ),
        }),
    )
    
    list_display = [
        'px_id', 'subcategory', 'sell_cur', 'buy_cur', 'margin',
        'username', 'score', 'user_timezone',  'category', 'created_at'
    ]
    list_filter = ['category', 'sell_cur', 'buy_cur', 'username']
    search_fields = ['subcategory', 'category', 'username']
    list_display_links = ['px_id', 'subcategory']    
    readonly_fields = ('created_at', )
    


class OfferInline(admin.StackedInline):
    model = Offer
    fieldsets = (
        (None, {
            'fields': ('subcategory','category')
        }),
        ('Prices and Amount', {
            'fields': (
                'sell_cur', 'buy_cur',
                'margin', 'price_per_cur', 
            ),
        }),
        ('User Data', {
            'fields': (
                'username', 'score', 'user_timezone', 
                'payment_method_label', 'description',
                'warranty', 'offer_detail'
            ),
        }),
    )


@admin.register(OfferDetail)
class OfferDetailAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Amount', {
            'fields': (
                'predefined_amount',
                'fiat_amount_range_min',
                'fiat_amount_range_max'
            )
        }),
        ('User Feedback', {
            'fields': (
                'feedback_positive', 
                'feedback_negative'
            ),
        }),
    )
    inlines = (OfferInline, )


@admin.register(GiftOrder)
class GiftOrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'status', 'offer', 'user',
        'discount', 'amount', 'created_at'
    ]
    list_filter = ['status']
    search_fields = ['user', 'offer', 'id']
    list_display_links = ['id', 'offer']


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = [
        'tg_id', 'username', 'language_code',
        'currency', 'is_admin', 'is_bot'
    ]
    search_fields = ['username', 'tg_id']
    list_display_links = ['tg_id', 'username']


@admin.register(CurrencyDetail)
class CurrencyDetailAdmin(admin.ModelAdmin):
    list_display = ['code', 'country']
    search_fields = ['code', 'country']
    list_display_links = ['code', 'country']
    
    
    
ADMIN_ORDERING = (
    ('data', (
        'Offer', 'GiftOrder', 'OfferDetail', 
        'Tag', 'Subcategory', 'Category', 
        'CurrencyDetail', 'TgUser'
    )),
)

# Creating a sort function
def get_app_list(self, request):
    app_dict = self._build_app_dict(request)
    for app_name, object_list in ADMIN_ORDERING:
        app = app_dict[app_name]
        app['models'].sort(key=lambda x: object_list.index(x['object_name']))
        yield app
        
        
admin.AdminSite.get_app_list = get_app_list
