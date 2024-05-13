from django.contrib import admin
from authentication.models import ImageUpload, Comment, ACModel

class ImageModel(admin.ModelAdmin):
    list_display = ("image",)

class CommentModel(admin.ModelAdmin):
    list_display = ('comment_id','user','comment','date_time',)

class ArticleModel(admin.ModelAdmin):
    list_display = ('articleid','user','title','author','content','date_time','isvalid',)

admin.site.register(ImageUpload,ImageModel)
admin.site.register(Comment,CommentModel)
admin.site.register(ACModel,ArticleModel)

