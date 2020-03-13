'''blog url定义
'''

from django.urls import path
from django.contrib.sitemaps.views import sitemap
from . import views
from .sitemaps import PostSitemap#, TagSitemap

#sitemap.xml
sitemaps = {
    'posts': PostSitemap,
}

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/addcomment/', views.add_comment, name='add_comment'),
    path('tags/', views.tags, name='tags'),
    path('tags/<int:tag_id>/', views.tag, name='tag'),
    path('categories/', views.categories, name='categories'),
    path('categories/<int:category_id>/', views.category, name='category'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]

