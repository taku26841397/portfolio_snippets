import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from snippets.models import Language, SubCategory

for lang in Language.objects.all():
    if SubCategory.objects.filter(language=lang, name="Base").exists():
        continue

    base = SubCategory.objects.create(
        name="Base",
        language=lang
    )

    lang.default_subcategory = base
    lang.save(update_fields=["default_subcategory"])
