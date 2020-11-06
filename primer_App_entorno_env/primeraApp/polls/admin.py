from django.contrib import admin

# Register your models here.
from .models import Question, Choice

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 2

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question_text','pub_date' )
    list_filter = ['pub_date','question_text']
    search_fields = ['id','question_text']
    #fields = ['pub_date', 'question_text']
    fieldsets = [
        ('Datos basicos', {'fields':['question_text']}),
        ('Informacion fecha', {'fields':['pub_date']})
    ]
    inlines = [ChoiceInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)