from django.contrib import admin
from django.contrib.auth.models import User
from .models import Product


# Unfold admin
from unfold.admin import ModelAdmin
from unfold.forms import AdminOwnPasswordChangeForm, UserChangeForm, UserCreationForm  # type: ignore
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin import register

# Import-export
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm  # type: ignore
from unfold.contrib.filters.admin import (RangeDateFilter, RangeDateTimeFilter)  # type: ignore

# Unfold register and unregister
admin.site.unregister(User)

@register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminOwnPasswordChangeForm  # corrected to lowercase

# Register your models here
@admin.register(Product)
class ProductAdmin(ModelAdmin, ImportExportModelAdmin):
    list_display = ['id', 'product_name', 'price', 'category', 'stock', 'quantity', 'quality', 'description', 'is_active', 'created_at', 'updated_at']
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_filter = ['price', ('created_at', RangeDateTimeFilter), ('updated_at', RangeDateFilter)]
    list_filter_submit = True  # submitting filter
