from django.db import models
from .constants import AI_MODEL_CHOICES

class Language(models.Model):
    name = models.CharField(max_length=50)
    default_subcategory = models.ForeignKey(
        'SubCategory',
        null= True,
        blank= True,
        on_delete= models.SET_NULL,
        related_name= 'default_for_language'
    )
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Base がまだない場合だけ作る
        if not SubCategory.objects.filter(language=self, name="Base").exists():
            base = SubCategory.objects.create(
                name="Base",
                language=self
            )
            self.default_subcategory = base
            super().save(update_fields=["default_subcategory"])
    
    
    
    def __str__(self):
        return self.name
# Create your models here.

class SubCategory(models.Model):
    language = models.ForeignKey(Language,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.language.name} / {self.name}"

class PromptCategory(models.Model):
    name = models.CharField(max_length=128)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    is_base = models.BooleanField(default=False)
    
    def __str__(self):
            return f"{self.language.name} / {self.name}"

class ImagePromptCategory(models.Model):
    name = models.CharField(max_length=128)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    is_base = models.BooleanField(default=False)
    
    def __str__(self):
            return f"{self.language.name} / {self.name}"



class Snippet(models.Model):
    title = models.CharField(max_length=128)
    code = models.TextField(blank=True)
    description = models.TextField(blank=True)
    
    language = models.ForeignKey(Language,on_delete=models.CASCADE)
    SubCategory = models.ForeignKey(SubCategory,on_delete=models.SET_NULL,null=True,blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Prompt(models.Model):
    title = models.CharField(max_length=100)
    prompt = models.TextField()
    description = models.TextField(blank=True)
    
    language = models.ForeignKey(Language,on_delete=models.CASCADE)
    prompt_category = models.ForeignKey(PromptCategory,on_delete=models.SET_NULL,null=True,blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title



class ImagePrompt(models.Model):
    title = models.CharField(max_length=100)
    ai_model = models.CharField(max_length=50,
                                choices=AI_MODEL_CHOICES,
                                default="anything")
    prompt = models.TextField()
    description = models.TextField(blank=True)
    base_image = models.ImageField(upload_to='base_images/')
    generated_image = models.ImageField(upload_to='generated_images/')
    
    language = models.ForeignKey(Language,on_delete=models.CASCADE)
    image_prompt_category = models.ForeignKey(ImagePromptCategory,on_delete=models.SET_NULL,null=True,blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title or "No Title"
