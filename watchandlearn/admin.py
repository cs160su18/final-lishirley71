from django.contrib import admin
from watchandlearn.models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# User: admin
# Password: adminpassword
# Email: admin@admin.com


class WordResource(resources.ModelResource):

    class Meta:
        model = Word

class WordAdmin(ImportExportModelAdmin):
    resource_class = WordResource


# Register your models here.

admin.site.register(Profile)
admin.site.register(Word, WordAdmin)
admin.site.register(Episode)
admin.site.register(Series)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Topic)
admin.site.register(Interest)

