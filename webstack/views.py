from collections import defaultdict, OrderedDict

from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView

from .models import Website
from .models import Category

# Create your views here.


class IndexView(ListView):
    template_name = 'webstack/index.html'
    context_object_name = 'all_website_list'

    def get_queryset(self):
        """Return all websites with category."""
        # queryset = Question.objects.order_by('-pub_date')[:5]
        queryset = Category.objects.order_by('-index')
        return queryset


@require_http_methods(["GET"])
def index(request, lang):
    if not lang in ('en', 'cn'):
        return render(request, 'webstack/404.html')
    category_objs = Category.objects.order_by('-index')
    category_dict = defaultdict(list)
    website_dict = defaultdict(list)
    for obj in category_objs:
        if obj.categorys.all():
            for c in obj.categorys.all():
                website_dict[c.name].append(obj)
        else:
            website_dict['未分类'].append(obj)
    print(website_dict)
    print([x.name for x in category_objs])
    website_dict = sorted(website_dict.items(), key=lambda x: {k.name: i for i, k in enumerate(category_objs)}[x[0]])
    print(website_dict)
    context = {
        'categorys': category_objs,
        'websites': website_dict,
    }
    return render(request, f'webstack/{lang}/index.html', context=context)


@require_http_methods(["GET"])
def _index(request):
    categorys = Category.objects.filter()
    websites = Website.objects.filter()
    websites_dict = defaultdict(list)
    for x in categorys:
        print(x.name, x.create_time, x.website_set.all())
    for x in websites:
        if x:
            print(x.name)
            websites_dict[x.categorys].append({
                'name': x.name,
                'url': x.url,
                # 'logo': f"http://favicon.byi.pw/?url={x.url}",
                # 'logo': f"https://www.baidu.com/favicon.ico",
                'logo': x.logo,
                'desc': x.desc,
                'create_time': x.create_time,
            })
    group_websites = [
        {
            'name': category.name,
            'sites': websites_dict.get(category.id),
        } for category in categorys if category
    ]
    filter_group_websites = [x for x in group_websites if x.get('sites')]
    result = {
        'msg': 'ok',
        'code': '200',
        'data': filter_group_websites,
    }
    return JsonResponse(data=result)

