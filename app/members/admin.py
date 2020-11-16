from django.contrib import admin

from members.models import KIUser, KeywordFavorite, Keyword


@admin.register(KIUser)
class KIUserAdmin(admin.ModelAdmin):
    pass


@admin.register(KeywordFavorite)
class KeywordFavoriteAdmin(admin.ModelAdmin):
    pass


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    pass
