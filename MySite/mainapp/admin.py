from django.contrib import admin
from .models import Company
# Register your models here.

from .models import Room, Topic

admin.site.register(Room)
admin.site.register(Topic)
#admin.site.register(Message)

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'email', 'approved')

    def approve_company(self, request, queryset):
        for company in queryset:
            company.approved = True
            company.save()

        self.message_user(request, "Заявки успешно одобрены.")

    actions = [approve_company]