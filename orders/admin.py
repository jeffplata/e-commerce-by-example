from django.contrib import admin
from .models import Order, OrderItem
import csv
import datetime
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields =['product']
    
def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; \
        filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)
    
    fields = [field for field in opts.get_fields() 
        if not field.many_to_many and not field.one_to_many]
    # Write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # Write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Export to csv'
    
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated', 
                    'order_detail',
                    'order_pdf',
                   )
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]
    
    def order_detail(self, obj):
        #return '<a href="{}">View</a>'.format(
        #    reverse('orders:admin_order_detail', args=[obj.id]))
        return format_html('<a href="{0}">View</a>', 
            reverse('orders:admin_order_detail', args=[obj.id]))
            
    def order_pdf(self, obj):
        #return '<a href="{}">PDF</a>'.format(
        #    reverse('orders:admin_order_pdf', args=[obj.id]))
        #order_pdf.allow_tags = True
        return format_html('<a href="{0}">PDF</a>',
            reverse('orders:admin_order_pdf', args=[obj.id]))
        order_pdf.short_description = 'PDF bill'
    
admin.site.register(Order, OrderAdmin)


