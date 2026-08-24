from .models import Language

def categories(request):
    return{
        "categories":Language.objects.all()
    }