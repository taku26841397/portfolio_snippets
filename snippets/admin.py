from django.contrib import admin
from .models import Language,Snippet,Prompt,ImagePrompt,SubCategory,PromptCategory,ImagePromptCategory

admin.site.register(Language)
admin.site.register(Snippet)
admin.site.register(Prompt)
admin.site.register(ImagePrompt)
admin.site.register(SubCategory)
admin.site.register(PromptCategory)
admin.site.register(ImagePromptCategory)
# Register your models here.
