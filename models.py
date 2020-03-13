'''
模块定义
1. Category 文章类型
2. Tag      文章标签
3. Post     文章
4. Comment  文章评论
5. Page     自定义页面
'''

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
import markdown
from hashlib import md5


#对象的状态定义
VALDATION_STATE_CHOICES = (		
    ('draft', 'Draft'),	            #草拟 
    ('valdated', 'Validated'),		#已验证
    ('invalidated', 'Invalidated'),	#已废止
)



class Category(models.Model):
'''文章类型模块定义
'''
    #标题
    title = models.CharField(verbose_name='Title', max_length=63, unique=True)
    #状态
    state = models.CharField(verbose_name='State', max_length=15, choices=VALDATION_STATE_CHOICES, default='draft')
    #创建日期
    create_date = models.DateTimeField(verbose_name='Create Date', auto_now_add=True)
    #更新日期
    update_date = models.DateTimeField(verbose_name='Update Date', auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['state'], name='category_state_idx'),
            models.Index(fields=['create_date'], name='category_create_date_idx'),
            models.Index(fields=['update_date'], name='category_update_date_idx'),
        ]


    def __str__(self):
        return "{}".format(self.title)

    #获取绝对路径
    def get_absolute_url(self):
        return reverse('blog:category', args=(self.id,))

    #获取已关联类型的文章，按发布日期倒序排列。
    def get_post_set(self, state='valdated', order_by='-publish_date'):
        return self.post_set.filter(state=state).order_by(order_by)



class Tag(models.Model):
'''文章标签模块定义
'''
    #标题
    title = models.CharField(verbose_name='Title', max_length=63, unique=True)
    #状态
    state = models.CharField(verbose_name='State', max_length=15, choices=VALDATION_STATE_CHOICES, default='draft')
    #创建日期
    create_date = models.DateTimeField(verbose_name='Create Date', auto_now_add=True)
    #更新日期
    update_date = models.DateTimeField(verbose_name='Update Date', auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['state'], name='tag_state_idx'),
            models.Index(fields=['create_date'], name='tag_create_date_idx'),
            models.Index(fields=['update_date'], name='tag_update_date_idx'),
        ]

    def __str__(self):
        return "{}".format(self.title)

    #获取绝对路径
    def get_absolute_url(self):
        return reverse('blog:tag', args=(self.id,))

    #获取已关联标签的文章，按发布日期倒序排列。
    def get_post_set(self, state='valdated', order_by='-publish_date'):
        return self.post_set.filter(state=state).order_by(order_by)



class Post(models.Model):
'''文章模块定义
文章用markdown语言编写
'''
    #标题
    title = models.CharField(verbose_name='Title', max_length=100)
    #描述
    description = models.CharField(verbose_name='Description', max_length=255)
    #内容
    content = models.TextField(verbose_name='Content')
    #发布日期
    publish_date = models.DateTimeField(verbose_name='Publish Date')
    #创建日期
    create_date = models.DateTimeField(verbose_name='Create Date', auto_now_add=True)
    #修改日期
    update_date = models.DateTimeField(verbose_name='Update Date', auto_now=True)
    #阅读数量
    views = models.PositiveIntegerField(verbose_name='Views', default=0)
    #关联的类型
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=None)
    #关联的标签
    tag = models.ManyToManyField(Tag, verbose_name='Tags', blank=True, default=None)
    #作者
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Author')
    #状态
    state = models.CharField(verbose_name='State', max_length=15, choices=VALDATION_STATE_CHOICES, default='draft')
    

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        #索引定义
        indexes = [
            models.Index(fields=['state'], name='post_state_idx'),
            models.Index(fields=['views'], name='post_views_idx'),
            models.Index(fields=['publish_date'], name='post_publish_date_idx'),
            models.Index(fields=['create_date'], name='post_create_date_idx'),
            models.Index(fields=['update_date'], name='post_update_date_idx'),
            models.Index(fields=['state', 'publish_date'], name='post_sp_idx'),
        ]

    #获取格式化发布日期
    def get_publish_date(self):
        return self.publish_date.strftime("%B %d, %Y at %H:%M %Z")

    #获取格式化发布日期
    def get_post_list_publish_date(self):
        return self.publish_date.strftime("%Y-%m-%d")

    #获取文章内容并使用markdown渲染
    def get_content(self):
        if self.state == 'valdated':
            self.views = self.views + 1
            self.save()
        return mark_safe(markdown.markdown(self.content, extensions=['markdown.extensions.codehilite', 'markdown.extensions.extra']))

    #获取文章作者
    def get_author(self):
        return self.author.username

    #获取文章评论列表
    def get_comment(self, state='valdated', order_by='-publish_date'):
        return self.comment_set.filter(state=state).order_by(order_by)

    #获取文章绝对路径
    def get_absolute_url(self): 
        return reverse('blog:post_detail', args=(self.id,))

    #获取关联的标签
    def get_related_tag(self, state='valdated', order_by='title'):
        return self.tag.filter(state=state).order_by(order_by)

    #获取关联的类型
    def get_related_category(self, state='valdated', order_by='title'):
        return self.category.filter(state=state).order_by(order_by)



class Comment(models.Model):
'''评论模块定义
'''
    #评论者昵称
    name = models.CharField(verbose_name='Nick Name', max_length=100)
    #评论者email
    email = models.EmailField(verbose_name='Email', blank=True)
    #评论内容
    content = models.TextField(verbose_name='Content', max_length=254)
    #评论的文章
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Post')
    #发布日期
    publish_date = models.DateTimeField(verbose_name='Publish Date', auto_now_add=True)
    #创建日期
    create_date = models.DateTimeField(verbose_name='Create Date', auto_now_add=True)
    #修改日期
    update_date = models.DateTimeField(verbose_name='Update Date', auto_now=True)
    #状态
    state = models.CharField(max_length=15, choices=VALDATION_STATE_CHOICES, default='draft')


    def __str__(self):
        return "{}: {}...".format(self.name, self.content[:10])

    class Meta:
        #索引定义
        indexes = [
            models.Index(fields=['state'], name='comment_state_idx'),
            models.Index(fields=['publish_date'], name='comment_publish_date_idx'),
            models.Index(fields=['create_date'], name='comment_create_date_idx'),
            models.Index(fields=['update_date'], name='comment_update_date_idx'),
            models.Index(fields=['state', 'publish_date'], name='comment_sp_idx'),
        ]

    #获取格式化发布日期
    def get_publish_date(self):
        return self.publish_date.strftime("%B %d, %Y at %H:%M %Z")

    #根据评论者email格式化头像图标url
    def get_avatar_url(self):
        url = 'https://secure.gravatar.com/avatar?d=identicon'
        if self.email:
            url = "https://secure.gravatar.com/avatar/{}?s=50&d=identicon".format(md5(self.email.encode('utf-8')).hexdigest())
        return url



class Page(models.Model):
'''自定义页面模块定义（测试中）
'''
    #标题
    title = models.CharField(verbose_name='Title', max_length=100)
    #标签
    reference = models.CharField(verbose_name='Reference', max_length=100, unique=True)
    #内容
    content = models.TextField(verbose_name='Content')
    #发布日期
    publish_date = models.DateTimeField(verbose_name='Publish Date')
    #创建日期
    create_date = models.DateTimeField(verbose_name='Create Date', auto_now_add=True)
    #修改日期
    update_date = models.DateTimeField(verbose_name='Update Date', auto_now=True)
    #状态
    state = models.CharField(verbose_name='State', max_length=15, choices=VALDATION_STATE_CHOICES, default='draft')


    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        #索引定义
        indexes = [
            models.Index(fields=['state'], name='page_state_idx'),
            models.Index(fields=['reference'], name='page_reference_idx'),
            models.Index(fields=['publish_date'], name='page_publish_date_idx'),
            models.Index(fields=['create_date'], name='page_create_date_idx'),
            models.Index(fields=['update_date'], name='page_update_date_idx'),
            models.Index(fields=['state', 'publish_date'], name='page_sp_idx'),
        ]


    #获取文章内容并使用markdown渲染
    def get_content(self):
        return mark_safe(markdown.markdown(self.content, extensions=['markdown.extensions.codehilite', 'markdown.extensions.extra']))

    #获取格式化发布日期
    def get_publish_date(self):
        return self.publish_date.strftime("%B %d, %Y at %H:%M %Z")

