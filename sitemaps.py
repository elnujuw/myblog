'''
sitemap.xml页面设置
'''

from django.contrib.sitemaps import Sitemap
from .models import Post, Tag


class PostSitemap(Sitemap):
'''将已验证的文章添加到sitemap.xml中
'''    
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Post.objects.filter(state='valdated')

    def lastmod(self, obj):
        return obj.update_date


#class TagSitemap(Sitemap):
#    changefreq = "monthly"
#    priority = 0.9
#
#    def items(self):
#        return Tag.objects.filter(state='valdated')
#
#    def lastmod(self, obj):
#        return obj.update_date
