from django.contrib import admin
from blog.models import Post, Category, Tag, Likes, PostComment, Comment, CommentLike

# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Likes)
admin.site.register(PostComment)
admin.site.register(Comment)
admin.site.register(CommentLike)
