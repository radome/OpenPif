from django.contrib import admin
from models import Item, Category, Bill, BillItem, BillItemExtra, Location

def make_enabled(modeladmin, request, queryset):
    queryset.update(enabled=True)

def make_disabled(modeladmin, request, queryset):
    queryset.update(enabled=False)

make_enabled.short_description = "Abilita items selezionati"
make_disabled.short_description = "Disabilita items selezionati"

class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'category', 'extra', 'quantity', 'priority',
                           'price', 'enabled']}),
    ]
    list_display = ('name', 'price', 'is_available', 'quantity', 'category',
                    'extra_verbose', 'priority', 'enabled')
    search_fields = ['name', 'id']
    list_filter = ['category', 'enabled', 'extra']
    actions = [make_enabled, make_disabled]

    def extra_verbose(self, obj):
        return 'Si' if obj.extra else 'No'
    extra_verbose.short_description = 'Aggiunta'


class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name', 'priority', 'enabled', 'printable']}),
    ]
    list_display = ('name', 'priority', 'enabled', 'printable')
    search_fields = ['name']
    list_filter = ['enabled']
    actions = [make_enabled, make_disabled]


class LocationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['description', 'enabled']}),
    ]
    list_display = ('description', 'enabled')
    search_fields = ['description']
    list_filter = ['enabled']
    actions = [make_enabled, make_disabled]


class BillItemInline(admin.StackedInline):
    model = BillItem
    extra = 1
    show_change_link = True


class BillItemExtraInline(admin.TabularInline):
    model = BillItemExtra
    extra = 1


class BillItemAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['bill', 'item', 'quantity', 'item_price',
                           'category', 'note']}),
    ]
    inlines = [BillItemExtraInline]
    list_display = ('item', 'quantity', 'bill')
    list_filter = ['bill']


class BillAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['customer_name', 'customer_id', 'total', 'server',
            'deleted_by']})
    ]
    inlines = [BillItemInline]
    list_display = ('customer_name', 'customer_id', 'id', 'server', 'date',
            'total', 'is_committed')
    search_fields = ['customer_name', 'customer_id', 'id', 'date', 'server']


admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Bill, BillAdmin)
admin.site.register(BillItem, BillItemAdmin)

