from django.urls import path
from . import views



urlpatterns = [
    path('',views.top,name='top'),
    
    #language（言語別のページ）
    path('languages/<int:pk>',views.language_detail,name='language_detail'),
    path('languages/add',views.language_add,name='languages_add'), #言語を追加ページ
    path('languages/<int:pk>/add',views.snippet_add,name='snippet_add_language'), #言語指定不可の追加ページ
    path('languages/<int:pk>/add/<int:sub_pk>',views.snippet_add,name='snippet_add_language'), #言語指定不可の追加ページ(サブカテゴリー付き)
    
    #subcategory
    path('subcategory/<int:pk>',views.subcategory_detail,name='subcategory_detail'),
    path('subcategory/add',views.subcategory_add,name='subcategory_add'),
    #PromptCategory
    path('promptcategory/add',views.promptcategory_add,name='promptcategory_add'),
    path('promptcategory/<int:pk>',views.promptcategory_detail,name='promptcategory_detail'),
    
    #ImagePromptCategory
    path('imagepromptcategory/add',views.imagepromptcategory_add,name='imagepromptcategory_add'),
    path('imagepromptcategory/<int:pk>',views.imagepromptcategory_detail,name='imagepromptcategory_detail'),
    
    #snippets
    path('snippets/list',views.snippets_list,name='snippets_list'),
    path('snippets/recent',views.recent_snippets,name='recent_snippets'),
    path('snippets/<int:pk>',views.snippet_detail,name='snippet_detail'),
    path('snippets/add',views.snippet_add,name='snippet_add'), #言語指定可能
    path('snippets/<int:pk>/edit',views.snippet_edit,name='snippet_edit'),
    path('snippets/<int:pk>/delete',views.snippet_delete,name='snippet_delete'),
    
    #prompt
    path('prompt/add/<int:pk>',views.prompt_add,name='prompt_add'),
    path('prompt/<int:pk>',views.prompt_detail,name="prompt_detail"),
    path('prompt/<int:pk>/edit',views.prompt_edit,name='prompt_edit'),
    path('prompt/<int:pk>/delete',views.prompt_delete,name='prompt_delete'),
    
    #imageprompt
    path('imageprompt/add/<int:pk>',views.imageprompt_add,name='imageprompt_add'),
    path('imageprompt/<int:pk>',views.imageprompt_detail,name='imageprompt_detail'),
    path('imageprompt/<int:pk>/edit',views.imageprompt_edit,name='imageprompt_edit'),
    path('imageprompt/<int:pk>/delete',views.imageprompt_delete,name='imageprompt_delete'),
    
    path('search/',views.site_search,name='site_search'),
    
]
