from django.contrib import admin

# Register your models here.
from registration.models import FbAuth


class AllFieldsAdmin(admin.ModelAdmin):

    """
    A model admin that displays all field in admin excpet Many to many and pk field
    """

    def __init__(self, model, admin_site):
        self.list_display = [field.name for field in model._meta.fields
                             if field.name not in ["id"]]
        super(AllFieldsAdmin, self).__init__(model, admin_site)

admin.site.register(FbAuth)