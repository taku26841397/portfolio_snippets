from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import TemplateView
from .models import Language,Snippet,Prompt,ImagePrompt,SubCategory,PromptCategory,ImagePromptCategory
from django.contrib import messages

from.constants import AI_MODEL_CHOICES
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from django.core.paginator import Paginator

from django.core.management import call_command
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os

@csrf_exempt
def upload_data(request):
    if request.method == "POST" and request.FILES.get("file"):
        # アップロードされた data.json を一時保存
        f = request.FILES["file"]
        temp_path = "temp_data.json"

        with open(temp_path, "wb+") as dest:
            for chunk in f.chunks():
                dest.write(chunk)

        # loaddata を実行して PostgreSQL に流し込む
        try:
            call_command("loaddata", temp_path)
            os.remove(temp_path)  # 一時ファイルを削除
            return HttpResponse("Data loaded successfully")
        except Exception as e:
            return HttpResponse(f"Error: {e}")

    return HttpResponse("Upload a file via POST")



def login_view(request):
    
    next_url = request.GET.get("next")
    
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.POST.get("next") or next_url or "/") # ログイン後の遷移先

    return render(request, "login.html")



def top(request):
    snippets = Snippet.objects.order_by('-created_at')[:10]
    # message = messages.success(request,"スニペットを削除しました。")
    return render(request,"snippets/top.html",{
        "snippets":snippets,
        
    })
    


def snippets_list(request):
    snippet_qs = Snippet.objects.all().order_by('-created_at')

    paginator = Paginator(snippet_qs, 10)  # 1ページ10件
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'snippets/snippet_list.html', {
        'page_obj': page_obj,
        'snippets': page_obj.object_list,
    })

def recent_snippets(request):
    snippets = Snippet.objects.order_by('-created_at')[:10]
    # message = messages.success(request,"スニペットを削除しました。")
    return render(request,"snippets/snippet.html",{
        "snippets":snippets,
        
    })





#detail

def snippet_detail(request,pk):
    snippet = Snippet.objects.get(pk=pk)
    lang = Language.objects.get(pk=snippet.language.id)
    subcategories = SubCategory.objects.filter(language=lang)
    return render(request,"snippets/snippet_detail.html",{
        "snippet":snippet,
        "subcategories":subcategories,
        
        })


def language_detail(request,pk):
    lang = Language.objects.get(pk=pk)
    snippets = Snippet.objects.filter(language=lang).order_by('-created_at')
    subcategories = SubCategory.objects.filter(language=lang)
    
    if lang.name == "AI":
        view_type = request.GET.get("type","prompt")
        
        if view_type == "prompt":
            print(view_type,"test")
            items = Prompt.objects.filter(language=lang).order_by('-created_at')
            subcategories = PromptCategory.objects.all()
            
        else:
            items = ImagePrompt.objects.filter(language=lang).order_by('-created_at')
            subcategories = ImagePromptCategory.objects.all()
    
        return render(request,"snippets/language_detail.html",{
            "lang":lang,
            "items":items,
            "view_type":view_type,
            "subcategories": subcategories,
            
        })
        
    return render(request,"snippets/language_detail.html",{
        "lang":lang,
        "snippets":snippets,
        "subcategories": subcategories,
    })

def subcategory_detail(request,pk):
    subcategory = SubCategory.objects.get(pk=pk)
    lang = subcategory.language
    snippets = Snippet.objects.filter(SubCategory=pk).order_by('-created_at')
    subcategories = SubCategory.objects.filter(language=lang)
    
    if lang.name == "AI":
        view_type = request.GET.get("type","prompt")
        
        if view_type == "prompt":
            print(view_type,"test")
            subcategory = PromptCategory.objects.get(pk=pk)
        
            subcategories = PromptCategory.objects.all()
            items = Prompt.objects.filter(language=lang).order_by('-created_at')
            
        else:
            subcategories = ImagePromptCategory.objects.all()
            items = ImagePrompt.objects.filter(language=lang).order_by('-created_at')
            
    
        return render(request,"subcategory/subcategory_detail.html",{
            "lang":lang,
            "items":items,
            "view_type":view_type,
            "subcategory":subcategory,
            "subcategories": subcategories,
            
        })
        
    return render(request,"subcategory/subcategory_detail.html",{
        "lang":lang,
        "snippets":snippets,
        "subcategory":subcategory,
        "subcategories": subcategories,
    })
    

def promptcategory_detail(request,pk):
    prompt_category = PromptCategory.objects.get(pk=pk)
    lang = prompt_category.language
    items = Prompt.objects.filter(prompt_category=pk).order_by('-created_at')
    prompt_categories = PromptCategory.objects.all()
    
    
        
        
    return render(request,"promptcategory/promptcategory_detail.html",{
        "items":items,
        "lang":lang,
        "subcategory":prompt_category,
        "subcategories": prompt_categories,
    })
    
def imagepromptcategory_detail(request,pk):
    prompt_category = ImagePromptCategory.objects.get(pk=pk)
    lang = prompt_category.language
    items = ImagePrompt.objects.filter(image_prompt_category=pk).order_by('-created_at')
    prompt_categories = ImagePromptCategory.objects.all()
    
    
        
        
    return render(request,"imagepromptcategory/imagepromptcategory_detail.html",{
        "items":items,
        "lang":lang,
        "subcategory":prompt_category,
        "subcategories": prompt_categories,
    })
    
    
@login_required
def subcategory_add(request):
    if request.method == "POST":
        name = request.POST.get("name")
        language_id = request.POST.get("language")
        language = Language.objects.get(pk=language_id)
        
        if name:
            SubCategory.objects.create(
                name=name,
                language = language,
                )
            return redirect("language_detail",pk=language_id)
    
    return render(request,"subcategory/subcategory_add.html")

@login_required
def language_add(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Language.objects.create(name=name)
            return redirect("languages_add")
    
    return render(request,"snippets/language_add.html")
            
@login_required
def snippet_add(request,pk=None,sub_pk=None):
    # subcategories =SubCategory.objects.all()
    fixed_lang = None
    fixed_sub = None
    subcategories = SubCategory.objects.all()
    if pk:
        fixed_lang = get_object_or_404(Language,pk=pk)
        subcategories = SubCategory.objects.filter(language_id=fixed_lang)
    if sub_pk:
        fixed_sub = get_object_or_404(SubCategory,pk=sub_pk)
    

    if request.method =="POST":
        title = request.POST.get("title")
        code = request.POST.get("code")
        description = request.POST.get("description")
        subcategory_id = request.POST.get("subcategory")
        
        
        subcategory =None
        if subcategory_id:
            subcategory = SubCategory.objects.get(pk=subcategory_id)
        
        
        if fixed_lang:
            Snippet.objects.create(
                title = title,
                code = code,
                description = description,
                language = fixed_lang,
                SubCategory = subcategory
                
            )
            
            if sub_pk:
                return redirect("subcategory_detail", pk=sub_pk)
            
            return redirect("language_detail", pk=fixed_lang.pk)
        language_id = request.POST.get("language")
        
        
        if title and language_id:
            lang = Language.objects.get(pk=language_id)
            Snippet.objects.create(
                title =title,
                code =code,
                description = description,
                language = lang,
                SubCategory = subcategory
            )
            return redirect("top")
    
        
    return render(request,"snippets/snippet_form.html",{
        "fixed_lang":fixed_lang,
        "fixed_sub":fixed_sub,
        "snippet":None,
        "button_label":"追加する",
        "title":"スニペットの追加",
        "subcategories":subcategories,
        
    })
    
@login_required
def snippet_edit(request,pk):
    snippet = get_object_or_404(Snippet,pk=pk)
    # subcategories = SubCategory.objects.filter(language=snippet.language)
    subcategories = SubCategory.objects.all()

    if request.method == "POST":
        snippet.title = request.POST.get("title")
        snippet.code = request.POST.get("code")
        snippet.description = request.POST.get("description")
        language_id = request.POST.get("language")
        subcategory_id = request.POST.get("subcategory")
        
        if language_id:
            snippet.language = Language.objects.get(pk=language_id)
        
        snippet.SubCategory = None
        if  subcategory_id:
            snippet.SubCategory = SubCategory.objects.get(pk=subcategory_id)
            
            
        snippet.save()
        return redirect("snippet_detail",pk=snippet.pk)    
    
    
    return render(request,"snippets/snippet_form.html",{
        "snippet":snippet,
        "title":"スニペットの編集",
        "button_label":"確定",
        "subcategories":subcategories
    })
    
    
    
def snippet_delete(request,pk):
    snippet = get_object_or_404(Snippet,pk=pk)
    if request.method == "POST":
        snippet.delete()
        messages.success(request,"スニペットを削除しました。")
        return redirect("language_detail",pk=snippet.language.pk)

    return render(request,"common/delete_confirm.html",{
        "title":"スニペット削除",
        "message":f"「{snippet.title}」を削除しますか？",
        "back_url":reverse("snippet_detail",args=[pk]),
        "delete_url":reverse("snippet_delete",args=[pk]),
        "snippet":snippet,
        
    })
    
    
@login_required
def prompt_add(request,pk):
    subcategories = PromptCategory.objects.all()
    lang = Language.objects.get(pk=pk)
    
    # GET のときに subcategory を受け取る
    initial_subcategory_id = request.GET.get("subcategory")
    
    if request.method == 'POST':
        title = request.POST.get("title")
        prompt = request.POST.get("prompt")
        description = request.POST.get("description")
        subcategory_id = request.POST.get("prompt_category")
        
        subcategory = None
        if subcategory_id:
            subcategory = PromptCategory.objects.get(pk=subcategory_id)
            
        
        Prompt.objects.create(
            title = title,
            prompt = prompt,
            description = description,
            language = lang,
            prompt_category = subcategory 
        )
        if initial_subcategory_id:
            return redirect("promptcategory_detail",pk=initial_subcategory_id)
        
        return redirect("language_detail",pk=pk)
    
    return render(request,"prompt/prompt_form.html",{
        "prompt":None,
        "lang":lang,
        "title":"プロンプトの追加",
        "button_label":"追加",
        "subcategories":subcategories,
        "initial_subcategory_id":initial_subcategory_id
    })

def prompt_detail(request,pk):
    subcategories = PromptCategory.objects.all()
    prompt = Prompt.objects.get(pk=pk)
    
    return render(request,"prompt/prompt_detail.html",{
        "prompt":prompt,
        "subcategories":subcategories,
    })
@login_required
def prompt_edit(request,pk):
    prompt = get_object_or_404(Prompt,pk=pk)
    subcategories = PromptCategory.objects.all()
    
    initial_subcategory_id = (
    str(prompt.prompt_category.pk)
    if prompt.prompt_category else ""
)

    if request.method == "POST":
        prompt.title = request.POST.get("title")
        prompt.prompt = request.POST.get("prompt")
        prompt.description = request.POST.get("description")
        prompt.prompt_category = None
        
        category_id = request.POST.get("prompt_category")
        
        if category_id:
            prompt.prompt_category = PromptCategory.objects.get(pk=category_id)
            
            
        prompt.save()
        
        return redirect("prompt_detail",pk=pk)
    
    return render(request,"prompt/prompt_form.html",{
        "prompt":prompt,
        "title":"プロンプトの編集",
        "button_label":"確定",
        "subcategories":subcategories,
        "initial_subcategory_id":initial_subcategory_id
    })


def prompt_delete(request,pk):
    prompt = get_object_or_404(Prompt,pk=pk)
    if request.method == "POST":
        prompt.delete()
    
        return redirect("language_detail",pk=prompt.language.pk)
    
    return render(request,"prompt/prompt_delete.html",{
        "prompt":prompt
    })
    
def imageprompt_delete(request,pk):
    prompt = get_object_or_404(ImagePrompt,pk=pk)
    if request.method == "POST":
        prompt.delete()
    
        return redirect("language_detail",pk=prompt.language.pk)
    
    return render(request,"prompt/imageprompt_delete.html",{
        "imageprompt":prompt
    })
@login_required  
def promptcategory_add(request):
    language = Language.objects.get(name="AI")
    if request.method == "POST":
        name = request.POST.get("name")
        
        
        if name:
            PromptCategory.objects.create(
                name=name,
                language = language,
                )
            return redirect("promptcategory_add")
    
    return render(request,"promptcategory/promptcategory_add.html",{
        "language":language
    })



@login_required
def imageprompt_add(request,pk):
    subcategories = ImagePromptCategory.objects.all()
    lang=Language.objects.get(pk=pk)
    
    # GET のときに subcategory を受け取る
    initial_subcategory_id = request.GET.get("subcategory")

    if request.method == 'POST':
        title = request.POST.get("title")
        ai_model = request.POST.get("ai_model")
        prompt = request.POST.get("prompt")
        base_image = request.FILES.get("base_image")
        generated_image = request.FILES.get("generated_image")
        category_id = request.POST.get("image_category")
        
        image_prompt_category =None
        if category_id:
            image_prompt_category = ImagePromptCategory.objects.get(pk=category_id)
            
        imageprompt = ImagePrompt.objects.create(
            title = title,
            ai_model = ai_model,
            prompt = prompt,
            base_image = base_image,
            generated_image = generated_image,
            language = lang,
            image_prompt_category = image_prompt_category
        )    
        imageprompt.save()
        
        if initial_subcategory_id:
            return redirect("imagepromptcategory_detail",pk=initial_subcategory_id)
        
        return redirect("language_detail",pk=pk)
    
    return render(request,"imageprompt/imageprompt_form.html",{
        "lang":lang,
        "imageprompt":None,
        "AI_MODEL_CHOICES":AI_MODEL_CHOICES,
        "title":"画像プロンプトの追加",
        "button_label":"追加",
        "subcategories":subcategories,
        "initial_subcategory_id":initial_subcategory_id
    })

def imageprompt_detail(request,pk):
    subcategories = ImagePromptCategory.objects.all()
    imageprompt = get_object_or_404(ImagePrompt,pk=pk)
    
    return render(request,"imageprompt/imageprompt_detail.html",{
        "imageprompt":imageprompt,
        "subcategories":subcategories,
    })
@login_required
def imageprompt_edit(request,pk):
    subcategories = ImagePromptCategory.objects.all()
    imageprompt = get_object_or_404(ImagePrompt,pk=pk)
    
    initial_subcategory_id = (
    str(imageprompt.image_prompt_category.pk)
    if imageprompt.image_prompt_category else ""
)

    if request.method == 'POST':
        imageprompt.title = request.POST.get("title")
        imageprompt.ai_model = request.POST.get("ai_model")
        imageprompt.prompt = request.POST.get("prompt")
        imageprompt.description = request.POST.get("description")
        imageprompt.title = request.POST.get("title")

        base_image = request.FILES.get("base_image")
        if base_image:
            
            imageprompt.base_image = base_image
            
        generated_image = request.FILES.get("generated_image")
        if generated_image:
            
            imageprompt.generated_image = generated_image 
        category_id =request.POST.get("image_category")
        imageprompt.image_prompt_category = None
        if category_id:
            imageprompt.image_prompt_category = ImagePromptCategory.objects.get(pk=category_id)
            
        imageprompt.save()

        return redirect("imageprompt_detail", pk=pk)
    return render(request,"imageprompt/imageprompt_form.html",{
        "imageprompt":imageprompt,
        "AI_MODEL_CHOICES":AI_MODEL_CHOICES,
        "title":"画像プロンプトの編集",
        "button_label":"確定",
        "subcategories":subcategories,
        "initial_subcategory_id":initial_subcategory_id
        
    })
    
@login_required
def imagepromptcategory_add(request):
    if request.method == "POST":
        name = request.POST.get("name")
        language_id = "8"
        language = Language.objects.get(pk=language_id)
        if name:
            ImagePromptCategory.objects.create(
                name=name,
                language = language,
                )
            return redirect("imagepromptcategory_add")
    
    return render(request,"imagepromptcategory/imagepromptcategory_add.html")



def site_search(request):
    query = request.GET.get("q","")
    
    snippet_results = Snippet.objects.filter(title__icontains=query)
    prompt_results = Prompt.objects.filter(title__icontains=query)
    imageprompt_results = ImagePrompt.objects.filter(title__icontains=query)
    
    return render(request,"snippets/search_result.html",{
        "query":query,
        "snippet_results":snippet_results,
        "prompt_results":prompt_results,
        "imageprompt_results":imageprompt_results
    })

# Create your views here.
