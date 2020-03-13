'''
向admin页面注册一下模块
1. Category	文章类型
2. Tag		文章标签
3. Post		文章
4. Comment	文章评论
5. Page		自定义页面
'''

from django.contrib import admin
from .models import Category, Tag, Post, Comment, Page

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Page)
