from django.contrib import admin
from gmah.models import Person, Claim, File, Requests

class WorkerAdmin(admin.ModelAdmin):
    list_display = ('fio','login','tel','mail','raiting')
# class ClientAdmin(admin.ModelAdmin):
    # list_display = ('fio','login','tel','mail','raiting')


class ClaimAdmin(admin.ModelAdmin):
    search_fields = ('id','name', 'description', )
    list_filter = ('owner', 'open_date', 'close_date',)
    date_hierarchy = 'open_date'
    ordering = ('-open_date', 'owner')

# admin.site.register(Note)
# admin.site.register(Resource)
admin.site.register(File)
admin.site.register(Requests)
admin.site.register(Person, WorkerAdmin)
# admin.site.register(ProblemByUser)
# admin.site.register(ProblemByWorker)
# admin.site.register(Categories)
admin.site.register(Claim, ClaimAdmin)
# admin.site.register(RegularTask, RegularTaskAdmin)
# admin.site.register(Joker)
# admin.site.register(Joker_Visit)
