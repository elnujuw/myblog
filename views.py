'''blog显示逻辑定义
'''


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.urls import reverse
from .models import Post, Category, Tag, Page

import time, datetime

BLOGTITLE = '菌部落'
BLOGFOOTER = '© {} - {} Junle.'.format(2014, time.strftime("%Y", time.gmtime()))


#页码生成器
def _paginator_generator(object_list, page, row_per_page=30):
    paginator = Paginator(object_list, row_per_page)
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)
    return objects, paginator.page_range


#主页
def index(request):
    context = {
        'blog_title': BLOGTITLE,
        'page_title': BLOGTITLE,
        'footer': BLOGFOOTER,
        'description': "",
    }

    page = request.GET.get('page', 1)
    post_list = Post.objects.filter(state='valdated').order_by('-publish_date')
    posts, page_range = _paginator_generator(post_list, page)
    tags = Tag.objects.filter(state='valdated').order_by('title')

    context['page_range'] = page_range
    context['posts'] = posts
    context['keywords'] = ', '.join([tag.title for tag in tags])
    return render(request, 'blog/index.html', context)


#关于页面，读取Page model的自定义页面
def about(request):
    context = {
        'blog_title': BLOGTITLE,
        'page_title': '{} - {}'.format('About', BLOGTITLE),
        'footer': BLOGFOOTER,
    }

    page = get_object_or_404(Page, reference='about')
    context['page'] = page

    return render(request, 'blog/about.html', context)


#文章页面
def post_detail(request, post_id):
    context = {
        'blog_title': BLOGTITLE,
        'footer': BLOGFOOTER,
    }

    post = get_object_or_404(Post, id=post_id, state='valdated')
    tags = post.get_related_tag(state='valdated', order_by='title')

    context['post'] = post
    context['page_title'] = '{} - {}'.format(post.title, BLOGTITLE)
    context['comment_list'] = post.get_comment(state='valdated', order_by='-publish_date')
    context['tags'] = tags
    context['keywords'] = ', '.join([tag.title for tag in tags])
    context['description'] = post.description
    return render(request, 'blog/post_detail.html', context) 


#添加评论方法
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    name = request.POST['name']
    email = request.POST['email']
    content = request.POST['content']
    post.comment_set.create(name=name, email=email, content=content)
    return HttpResponseRedirect(reverse('blog:post_detail', args=(post.id,)))


#标签列表页面
def tags(request):
    context = {
        'blog_title': BLOGTITLE,
        'footer': BLOGFOOTER,
        'page_title': '{} - {}'.format('Tags', BLOGTITLE),
    }

    page = request.GET.get('page', 1)
    tag_list = Tag.objects.filter(state='valdated').order_by('title')
    paginator = Paginator(tag_list, 30)
    tags, page_range = _paginator_generator(tag_list, page)
    
    context['page_range'] = page_range
    context['tags'] = tags
    context['keywords'] = 'tags'

    return render(request, 'blog/tags.html', context)    


#标签页面
def tag(request, tag_id):
    context = {
        'blog_title': BLOGTITLE,
        'footer': BLOGFOOTER,
    }

    page = request.GET.get('page', 1)
    tag = get_object_or_404(Tag, pk=tag_id, state='valdated')
    post_list = tag.post_set.filter(state='valdated').order_by('-publish_date') 
    posts, page_range = _paginator_generator(post_list, page)

    context['page_range'] = page_range
    context['posts'] = posts
    context['tag'] = tag
    context['keywords'] = tag.title
    context['page_title'] = 'Tag: {} - {}'.format(tag.title, BLOGTITLE)
    return render(request, 'blog/tag.html', context)


#类型列表页面
def categories(request):
    context = {
        'blog_title': BLOGTITLE,
        'footer': BLOGFOOTER,
        'page_title': '{} - {}'.format('Categories', BLOGTITLE),
    }
    page = request.GET.get('page', 1)
    category_list = Category.objects.filter(state='valdated').order_by('title')
    categories, page_range = _paginator_generator(category_list, page)

    context['page_range'] = page_range
    context['categories'] = categories
    context['keywords'] = 'Categories'

    return render(request, 'blog/categories.html', context)


#类型页面
def category(request, category_id):
    context = {
        'blog_title': BLOGTITLE,
        'footer': BLOGFOOTER,
    }

    page = request.GET.get('page', 1)
    category = get_object_or_404(Category, pk=category_id, state='valdated')
    post_list = category.post_set.filter(state='valdated').order_by('-publish_date')
    posts, page_range = _paginator_generator(post_list, page)

    context['page_range'] = page_range
    context['posts'] = posts
    context['category'] = category
    context['keywords'] = category.title
    context['page_title'] = 'category: {} - {}'.format(category.title, BLOGTITLE)
    return render(request, 'blog/category.html', context)

