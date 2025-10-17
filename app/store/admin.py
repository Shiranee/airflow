# """
# Django admin customization.
# """
# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.utils.translation import gettext_lazy as _
# from django.utils.html import format_html
# from django.urls import reverse

# from store import models as store
# from employee.admin import EmployeeStoreInline
# from employee import models as employee


# class StoreAdressInline(admin.StackedInline):
#     model = store.StoreAdresses
#     extra = 0

#     fieldsets = (
#         ('Address Information', {
#             'fields': (
#                 ('status', 'zip_code', 'state'),
#                 ('city', 'neighborhood'),
#                 ('street', 'number'),
#                 'complement'
#             )
#         }),
#     )


# class StoreSocialInline(admin.StackedInline):
#     model = store.StoreSocial
#     extra = 0

#     fieldsets = (
#         ('Social Information', {
#             'fields': (
#                 ('status', 'name', 'url', 'coupon_id'),
#             )
#         }),
#         ('Contacts', {
#             'fields': (
#                 ('email', 'phone', 'whatsapp', 'instagram', 'facebook'),
#             )
#         }),
#         ('Expedient', {
#             'fields': (
#                 ('working_days', 'working_hours'),
#             )
#         }),
#         ('Photos', {
#             'fields': (
#                 ('cover_photo', 'store_photo'),
#             )
#         }),
#     )


# class StoresAdmin(admin.ModelAdmin):
# 		inlines = [EmployeeStoreInline, StoreAdressInline, StoreSocialInline]
# 		list_display = ('id', 'status', 'name', 'cnpj', 'name_legal', 'inaugurated_at', 'created_at')
# 		search_fields = ('id', 'name', 'cnpj')

# 		fieldsets = (
# 				('Basic Information', {
# 						'fields': (
# 								('status', 'name'),
# 								('name_legal',),
# 						)
# 				}),
# 				('Identification', {
# 						'fields': (
# 								('cnpj', 'cigam_id', 'franchise_id'),
# 						)
# 				}),
# 				('Dates', {
# 						'fields': ('inaugurated_at',)
# 				}),
# 				('System Information', {
# 						'fields': (
# 								('created_at', 'updated_at'),
# 								('deleted_at',),
# 						),
# 						'classes': ('collapse',)
# 				}),
# 		)

# 		readonly_fields = ('created_at', 'updated_at')

# admin.site.register(store.Stores, StoresAdmin)