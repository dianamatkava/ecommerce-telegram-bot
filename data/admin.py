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
    
    
    