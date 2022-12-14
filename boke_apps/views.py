from django.shortcuts import render, HttpResponse, redirect
from django.core.paginator import Paginator
from django.utils.safestring import mark_safe

from boke_apps.models import poetry2 ,user_data
import requests
from lxml import etree

def fenye(request):#分页
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
        'platform': 'pc',
        'sa': 'pcindex_a_right'
    }
    url = 'https://top.baidu.com/board?'
    responsess = requests.get(url, headers=headers)
    # responsess.encoding = 'utf-8'
    ertee_path = etree.HTML(responsess.text)
    redu_list = []
    for i in range(1, 10):
        re_dic = {}
        text1 = ertee_path.xpath(f'//*[@id="sanRoot"]/main/div[1]/div[1]/div[2]/a[{i}]/div[2]/div[2]/div/div/text()')[
            0].strip(' ')
        url = ertee_path.xpath(f'//*[@id="sanRoot"]/main/div[1]/div[1]/div[2]/a[{i}]/@href')[0]
        re_dic[str(i) + '、' + text1] = url
        redu_list.append(re_dic)
    rebiaoqian_list = [{'python': 2}, {'java': 20}, {'html': 45}, {'css': 75}, {'mysql': 6}, {'js': 56}]
    page = int(request.GET.get('page', 1))
    page_size = 5  # 每页显示10条数据
    start = (page - 1) * page_size
    end = start + 5
    page_queryset = poetry2.objects.all()[start:end]  # 查询数据的前十行
    total_count = poetry2.objects.count()  # 计算数据库里面的数据总条数

    # 计算出总页码
    total_page_count, div = divmod(total_count, page_size)
    if div:
        total_page_count += 1

    # 计算出，显示当前页的前5页，后5页
    plus = 5
    if total_page_count <= plus * 2 + 1:
        # 数据库中的数据比较少，都没达到11页
        start_page = 1
        end_page = total_page_count
    else:
        # 大于11页
        # 当前页<5时（小极值）
        if page <= plus:
            start_page = 1
            end_page = plus * 2
        else:
            # 当前页>5
            # 当前页+5>总页码
            if (page + plus) > total_page_count:
                start_page = total_page_count - plus * 2
                end_page = total_page_count
            else:
                start_page = page - plus
                end_page = page + plus

    # 页码
    page_str_list = []

    # 首页
    prev = '<li><a href="?page={}">首页</a></li>'.format(1)
    page_str_list.append(prev)
    # 上一页
    if page > 1:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(page - 1)
    else:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(1)
    page_str_list.append(prev)

    for i in range(start_page, end_page + 1):
        if i == page:
            ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
        else:
            ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
        page_str_list.append(ele)

    # 下一页
    if page < total_page_count:
        prev = '<li><a href="?page={}">下一页</a></li>'.format(page + 1)
    else:
        prev = '<li><a href="?page={}">下一页</a></li>'.format(total_page_count)
    page_str_list.append(prev)

    # 尾页
    prev = '<li><a href="?page={}">尾页</a></li>'.format(total_page_count)
    page_str_list.append(prev)

    page_string = mark_safe(''.join(page_str_list))
    """
    <li><a href="?page=1">1</a></li>
    <li><a href="?page=2">2</a></li>
    <li><a href="?page=3">3</a></li>
    <li><a href="?page=4">4</a></li>
    <li><a href="?page=5">5</a></li>
    """
    # 总分页

    return redu_list,rebiaoqian_list,page_queryset,page_string
def test(request):
    page = int(request.GET.get('page',1))
    page_size = 5#每页显示10条数据
    start = (page-1)*page_size
    end = start+5
    # from boke_apps.utils.pagination import Pagination
    page_queryset = poetry2.objects.all()[start:end] # 查询数据的前十行
    print(page)
    print(start)
    print(end)
    total_count =poetry2.objects.count()#计算数据库里面的数据总条数

    #计算出总页码
    total_page_count ,div= divmod(total_count,page_size)
    if div:
        total_page_count+=1


    #计算出，显示当前页的前5页，后5页
    plus = 5
    if total_page_count <= plus*2+1:
        #数据库中的数据比较少，都没达到11页
        start_page = 1
        end_page = total_page_count
    else:
        #大于11页
        #当前页<5时（小极值）
        if page<=plus:
            start_page = 1
            end_page = plus*2
        else:
            #当前页>5
            #当前页+5>总页码
            if(page+plus)>total_page_count:
                start_page = total_page_count-plus*2
                end_page = total_page_count
            else:
                start_page = page-plus
                end_page = page+plus

    #页码
    page_str_list=[]

    #首页
    prev = '<li><a href="?page={}">首页</a></li>'.format(1)
    page_str_list.append(prev)
    #上一页
    if page >1:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(page-1)
    else:
        prev = '<li><a href="?page={}">上一页</a></li>'.format(1)
    page_str_list.append(prev)

    for i in range(start_page,end_page+1):
        if i == page:
            ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i,i)
        else:
            ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
        page_str_list.append(ele)


    #下一页
    if page < total_page_count:
        prev = '<li><a href="?page={}">下一页</a></li>'.format(page+1)
    else:
        prev = '<li><a href="?page={}">下一页</a></li>'.format(total_page_count)
    page_str_list.append(prev)

    #尾页
    prev = '<li><a href="?page={}">尾页</a></li>'.format(total_page_count)
    page_str_list.append(prev)

    page_string = mark_safe(''.join(page_str_list))
    """
    <li><a href="?page=1">1</a></li>
    <li><a href="?page=2">2</a></li>
    <li><a href="?page=3">3</a></li>
    <li><a href="?page=4">4</a></li>
    <li><a href="?page=5">5</a></li>
    """

    # current_page = request.GET.get("page", 1)
    # all_count = book_list.count()
    # page_obj = Pagination(current_page=current_page, all_count=all_count, per_page_num=10)
    # page_queryset = book_list[page_obj.start:page_obj.end]
    return render(request, 'test.html', {'page_queryset':page_queryset,'page_string':page_string})

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('user')
        password = request.POST.get('pwd')
        if username == '似海' and password == '942669366':
            redu_list, rebiaoqian_list, page_queryset, page_string = fenye(request)

            return render(request, "home_main.html", {'user_status': 1, "username": username, "redu_list": redu_list,'rebiaoqian_list': rebiaoqian_list,'page_queryset': page_queryset, 'page_string': page_string})

        else:
            return render(request, 'login.html', {'error': '用户和密码输入错误'})

def register(request):
    if request.method == 'GET':
        return render(request,'register.html')
    user1 = request.POST.get('user1')
    pwd = request.POST.get('pwd1')
    user_data.objects.create(user_id=2,user_name = user1,user_pwd = pwd)
    redu_list, rebiaoqian_list, page_queryset, page_string = fenye(request)

    return render(request, "home_main.html", {'user_status':1,"username": user1, "redu_list": redu_list,'rebiaoqian_list': rebiaoqian_list,'page_queryset': page_queryset, 'page_string': page_string})
    # return render(request,'register.html')



def home_main(request):
    redu_list,rebiaoqian_list,page_queryset,page_string = fenye(request)

    return render(request, "home_main.html",{'user_status':0,'login_req': '登录', 'register' :'注册',"redu_list": redu_list, 'rebiaoqian_list': rebiaoqian_list,'page_queryset': page_queryset, 'page_string': page_string})

    # return render(request, 'test.html', {'page_queryset': page_queryset, 'page_string': page_string})
def add_data(request):
    poetrys_data1 = ['两情若是久长时，又岂在朝朝暮暮。——秦观《鹊桥仙》', '入我相思门，知我相思苦，长相思兮长相忆，短相思兮无穷极。——李白《三五七言》',
                    '曾经沧海难为水，除却巫山不是云。——元稹《离思五首其四》', '君若扬路尘，妾若浊水泥，浮沈各异势，会合何时谐？——曹植《明月上高楼》',
                    '凄凉别后两应同，最是不胜清怨月明中。——纳兰性德《虞美人》', '自君之出矣，明镜暗不治。思君如流水，何有穷已时。——徐干《室思》',
                    '相见争如不见，有情何似无情。——司马光《西江月》', '落红不是无情物，化作春泥更护花。——龚自珍《己亥杂诗》',
                    '天不老，情难绝。心似双丝网，中有千千结。——张先《千秋岁》', '似此星辰非昨夜，为谁风露立中宵。——黄景仁《绮怀诗二首其一》',
                    '直道相思了无益，未妨惆怅是清狂。——李商隐《无题六首其三》', '十年生死两茫茫，不思量，自难忘，千里孤坟，无处话凄凉。——苏轼《江城子》',
                    '今夕何夕，见此良人。——佚名《诗经唐风绸缪》', '天长地久有时尽，此恨绵绵无绝期。——白居易《长恨歌》',
                    '在天愿作比翼鸟，在地愿为连理枝。——白居易《长恨歌》', '重叠泪痕缄锦字，人生只有情难死。——文廷式《蝶恋花》',
                    '一个是阆苑仙葩，一个是美玉无瑕。若说没奇缘，今生偏又遇著他；若说有奇缘，如何心事终虚话？——曹雪芹《枉凝眉》', '春蚕到死丝方尽，蜡炬成灰泪始干。——李商隐《无题》',
                    '他生莫作有情痴，人间无地著相思。——况周颐《减字浣溪沙》', '尊前拟把归期说，未语春容先惨咽。——欧阳修《玉楼春》',
                    '关关雎鸠，在河之洲。窈宨淑女，君子好逑。——佚名《诗经周南关雎》', '人生自是有情痴，此恨不关风与月。——欧阳修《玉楼春》',
                    '此去经年，应是良辰好景虚设。便纵有，千种风情，更与何人说。——柳永《雨霖铃》'
                    ]
    poetrys_data = ['两情若是久长时，又岂在朝朝暮暮。——秦观《鹊桥仙》', '入我相思门，知我相思苦，长相思兮长相忆，短相思兮无穷极。——李白《三五七言》',
                    '曾经沧海难为水，除却巫山不是云。——元稹《离思五首其四》', '君若扬路尘，妾若浊水泥，浮沈各异势，会合何时谐？——曹植《明月上高楼》',
                    '凄凉别后两应同，最是不胜清怨月明中。——纳兰性德《虞美人》', '自君之出矣，明镜暗不治。思君如流水，何有穷已时。——徐干《室思》',
                    '相见争如不见，有情何似无情。——司马光《西江月》', '落红不是无情物，化作春泥更护花。——龚自珍《己亥杂诗》',
                    '天不老，情难绝。心似双丝网，中有千千结。——张先《千秋岁》', '似此星辰非昨夜，为谁风露立中宵。——黄景仁《绮怀诗二首其一》',
                    '直道相思了无益，未妨惆怅是清狂。——李商隐《无题六首其三》', '十年生死两茫茫，不思量，自难忘，千里孤坟，无处话凄凉。——苏轼《江城子》',
                    '今夕何夕，见此良人。——佚名《诗经唐风绸缪》', '天长地久有时尽，此恨绵绵无绝期。——白居易《长恨歌》',
                    '在天愿作比翼鸟，在地愿为连理枝。——白居易《长恨歌》', '重叠泪痕缄锦字，人生只有情难死。——文廷式《蝶恋花》',
                    '一个是阆苑仙葩，一个是美玉无瑕。若说没奇缘，今生偏又遇著他；若说有奇缘，如何心事终虚话？——曹雪芹《枉凝眉》', '春蚕到死丝方尽，蜡炬成灰泪始干。——李商隐《无题》',
                    '他生莫作有情痴，人间无地著相思。——况周颐《减字浣溪沙》', '尊前拟把归期说，未语春容先惨咽。——欧阳修《玉楼春》',
                    '关关雎鸠，在河之洲。窈宨淑女，君子好逑。——佚名《诗经周南关雎》', '人生自是有情痴，此恨不关风与月。——欧阳修《玉楼春》',
                    '此去经年，应是良辰好景虚设。便纵有，千种风情，更与何人说。——柳永《雨霖铃》',
                    '两情若是久长时，又岂在朝朝暮暮。——秦观《鹊桥仙》', '入我相思门，知我相思苦，长相思兮长相忆，短相思兮无穷极。——李白《三五七言》',
                    '曾经沧海难为水，除却巫山不是云。——元稹《离思五首其四》', '君若扬路尘，妾若浊水泥，浮沈各异势，会合何时谐？——曹植《明月上高楼》',
                    '凄凉别后两应同，最是不胜清怨月明中。——纳兰性德《虞美人》', '自君之出矣，明镜暗不治。思君如流水，何有穷已时。——徐干《室思》',
                    '相见争如不见，有情何似无情。——司马光《西江月》', '落红不是无情物，化作春泥更护花。——龚自珍《己亥杂诗》',
                    '天不老，情难绝。心似双丝网，中有千千结。——张先《千秋岁》', '似此星辰非昨夜，为谁风露立中宵。——黄景仁《绮怀诗二首其一》',
                    '直道相思了无益，未妨惆怅是清狂。——李商隐《无题六首其三》', '十年生死两茫茫，不思量，自难忘，千里孤坟，无处话凄凉。——苏轼《江城子》',
                    '今夕何夕，见此良人。——佚名《诗经唐风绸缪》', '天长地久有时尽，此恨绵绵无绝期。——白居易《长恨歌》',
                    '在天愿作比翼鸟，在地愿为连理枝。——白居易《长恨歌》', '重叠泪痕缄锦字，人生只有情难死。——文廷式《蝶恋花》',
                    '一个是阆苑仙葩，一个是美玉无瑕。若说没奇缘，今生偏又遇著他；若说有奇缘，如何心事终虚话？——曹雪芹《枉凝眉》', '春蚕到死丝方尽，蜡炬成灰泪始干。——李商隐《无题》',
                    '他生莫作有情痴，人间无地著相思。——况周颐《减字浣溪沙》', '尊前拟把归期说，未语春容先惨咽。——欧阳修《玉楼春》',
                    '关关雎鸠，在河之洲。窈宨淑女，君子好逑。——佚名《诗经周南关雎》', '人生自是有情痴，此恨不关风与月。——欧阳修《玉楼春》',
                    '此去经年，应是良辰好景虚设。便纵有，千种风情，更与何人说。——柳永《雨霖铃》',
                    '两情若是久长时，又岂在朝朝暮暮。——秦观《鹊桥仙》', '入我相思门，知我相思苦，长相思兮长相忆，短相思兮无穷极。——李白《三五七言》',
                    '曾经沧海难为水，除却巫山不是云。——元稹《离思五首其四》', '君若扬路尘，妾若浊水泥，浮沈各异势，会合何时谐？——曹植《明月上高楼》',
                    '凄凉别后两应同，最是不胜清怨月明中。——纳兰性德《虞美人》', '自君之出矣，明镜暗不治。思君如流水，何有穷已时。——徐干《室思》',
                    '相见争如不见，有情何似无情。——司马光《西江月》', '落红不是无情物，化作春泥更护花。——龚自珍《己亥杂诗》',
                    '天不老，情难绝。心似双丝网，中有千千结。——张先《千秋岁》', '似此星辰非昨夜，为谁风露立中宵。——黄景仁《绮怀诗二首其一》',
                    '直道相思了无益，未妨惆怅是清狂。——李商隐《无题六首其三》', '十年生死两茫茫，不思量，自难忘，千里孤坟，无处话凄凉。——苏轼《江城子》',
                    '今夕何夕，见此良人。——佚名《诗经唐风绸缪》', '天长地久有时尽，此恨绵绵无绝期。——白居易《长恨歌》',
                    '在天愿作比翼鸟，在地愿为连理枝。——白居易《长恨歌》', '重叠泪痕缄锦字，人生只有情难死。——文廷式《蝶恋花》',
                    '一个是阆苑仙葩，一个是美玉无瑕。若说没奇缘，今生偏又遇著他；若说有奇缘，如何心事终虚话？——曹雪芹《枉凝眉》', '春蚕到死丝方尽，蜡炬成灰泪始干。——李商隐《无题》',
                    '他生莫作有情痴，人间无地著相思。——况周颐《减字浣溪沙》', '尊前拟把归期说，未语春容先惨咽。——欧阳修《玉楼春》',
                    '关关雎鸠，在河之洲。窈宨淑女，君子好逑。——佚名《诗经周南关雎》', '人生自是有情痴，此恨不关风与月。——欧阳修《玉楼春》',
                    '此去经年，应是良辰好景虚设。便纵有，千种风情，更与何人说。——柳永《雨霖铃》',
                    '两情若是久长时，又岂在朝朝暮暮。——秦观《鹊桥仙》', '入我相思门，知我相思苦，长相思兮长相忆，短相思兮无穷极。——李白《三五七言》',
                    '曾经沧海难为水，除却巫山不是云。——元稹《离思五首其四》', '君若扬路尘，妾若浊水泥，浮沈各异势，会合何时谐？——曹植《明月上高楼》',
                    '凄凉别后两应同，最是不胜清怨月明中。——纳兰性德《虞美人》', '自君之出矣，明镜暗不治。思君如流水，何有穷已时。——徐干《室思》',
                    '相见争如不见，有情何似无情。——司马光《西江月》', '落红不是无情物，化作春泥更护花。——龚自珍《己亥杂诗》',
                    '天不老，情难绝。心似双丝网，中有千千结。——张先《千秋岁》', '似此星辰非昨夜，为谁风露立中宵。——黄景仁《绮怀诗二首其一》',
                    '直道相思了无益，未妨惆怅是清狂。——李商隐《无题六首其三》', '十年生死两茫茫，不思量，自难忘，千里孤坟，无处话凄凉。——苏轼《江城子》',
                    '今夕何夕，见此良人。——佚名《诗经唐风绸缪》', '天长地久有时尽，此恨绵绵无绝期。——白居易《长恨歌》',
                    '在天愿作比翼鸟，在地愿为连理枝。——白居易《长恨歌》', '重叠泪痕缄锦字，人生只有情难死。——文廷式《蝶恋花》',
                    '一个是阆苑仙葩，一个是美玉无瑕。若说没奇缘，今生偏又遇著他；若说有奇缘，如何心事终虚话？——曹雪芹《枉凝眉》', '春蚕到死丝方尽，蜡炬成灰泪始干。——李商隐《无题》',
                    '他生莫作有情痴，人间无地著相思。——况周颐《减字浣溪沙》', '尊前拟把归期说，未语春容先惨咽。——欧阳修《玉楼春》',
                    '关关雎鸠，在河之洲。窈宨淑女，君子好逑。——佚名《诗经周南关雎》', '人生自是有情痴，此恨不关风与月。——欧阳修《玉楼春》',
                    '此去经年，应是良辰好景虚设。便纵有，千种风情，更与何人说。——柳永《雨霖铃》',
                    '两情若是久长时，又岂在朝朝暮暮。——秦观《鹊桥仙》', '入我相思门，知我相思苦，长相思兮长相忆，短相思兮无穷极。——李白《三五七言》',
                    '曾经沧海难为水，除却巫山不是云。——元稹《离思五首其四》', '君若扬路尘，妾若浊水泥，浮沈各异势，会合何时谐？——曹植《明月上高楼》',
                    '凄凉别后两应同，最是不胜清怨月明中。——纳兰性德《虞美人》', '自君之出矣，明镜暗不治。思君如流水，何有穷已时。——徐干《室思》',
                    '相见争如不见，有情何似无情。——司马光《西江月》', '落红不是无情物，化作春泥更护花。——龚自珍《己亥杂诗》',
                    '天不老，情难绝。心似双丝网，中有千千结。——张先《千秋岁》', '似此星辰非昨夜，为谁风露立中宵。——黄景仁《绮怀诗二首其一》',
                    '直道相思了无益，未妨惆怅是清狂。——李商隐《无题六首其三》', '十年生死两茫茫，不思量，自难忘，千里孤坟，无处话凄凉。——苏轼《江城子》',
                    '今夕何夕，见此良人。——佚名《诗经唐风绸缪》', '天长地久有时尽，此恨绵绵无绝期。——白居易《长恨歌》',
                    '在天愿作比翼鸟，在地愿为连理枝。——白居易《长恨歌》', '重叠泪痕缄锦字，人生只有情难死。——文廷式《蝶恋花》',
                    '一个是阆苑仙葩，一个是美玉无瑕。若说没奇缘，今生偏又遇著他；若说有奇缘，如何心事终虚话？——曹雪芹《枉凝眉》', '春蚕到死丝方尽，蜡炬成灰泪始干。——李商隐《无题》',
                    '他生莫作有情痴，人间无地著相思。——况周颐《减字浣溪沙》', '尊前拟把归期说，未语春容先惨咽。——欧阳修《玉楼春》',
                    '关关雎鸠，在河之洲。窈宨淑女，君子好逑。——佚名《诗经周南关雎》', '人生自是有情痴，此恨不关风与月。——欧阳修《玉楼春》',
                    '此去经年，应是良辰好景虚设。便纵有，千种风情，更与何人说。——柳永《雨霖铃》',
                    '两情若是久长时，又岂在朝朝暮暮。——秦观《鹊桥仙》', '入我相思门，知我相思苦，长相思兮长相忆，短相思兮无穷极。——李白《三五七言》',
                    '曾经沧海难为水，除却巫山不是云。——元稹《离思五首其四》', '君若扬路尘，妾若浊水泥，浮沈各异势，会合何时谐？——曹植《明月上高楼》',
                    '凄凉别后两应同，最是不胜清怨月明中。——纳兰性德《虞美人》', '自君之出矣，明镜暗不治。思君如流水，何有穷已时。——徐干《室思》',
                    '相见争如不见，有情何似无情。——司马光《西江月》', '落红不是无情物，化作春泥更护花。——龚自珍《己亥杂诗》',
                    '天不老，情难绝。心似双丝网，中有千千结。——张先《千秋岁》', '似此星辰非昨夜，为谁风露立中宵。——黄景仁《绮怀诗二首其一》',
                    '直道相思了无益，未妨惆怅是清狂。——李商隐《无题六首其三》', '十年生死两茫茫，不思量，自难忘，千里孤坟，无处话凄凉。——苏轼《江城子》',
                    '今夕何夕，见此良人。——佚名《诗经唐风绸缪》', '天长地久有时尽，此恨绵绵无绝期。——白居易《长恨歌》',
                    '在天愿作比翼鸟，在地愿为连理枝。——白居易《长恨歌》', '重叠泪痕缄锦字，人生只有情难死。——文廷式《蝶恋花》',
                    '一个是阆苑仙葩，一个是美玉无瑕。若说没奇缘，今生偏又遇著他；若说有奇缘，如何心事终虚话？——曹雪芹《枉凝眉》', '春蚕到死丝方尽，蜡炬成灰泪始干。——李商隐《无题》',
                    '他生莫作有情痴，人间无地著相思。——况周颐《减字浣溪沙》', '尊前拟把归期说，未语春容先惨咽。——欧阳修《玉楼春》',
                    '关关雎鸠，在河之洲。窈宨淑女，君子好逑。——佚名《诗经周南关雎》', '人生自是有情痴，此恨不关风与月。——欧阳修《玉楼春》',
                    '此去经年，应是良辰好景虚设。便纵有，千种风情，更与何人说。——柳永《雨霖铃》',
                    '两情若是久长时，又岂在朝朝暮暮。——秦观《鹊桥仙》', '入我相思门，知我相思苦，长相思兮长相忆，短相思兮无穷极。——李白《三五七言》',
                    '曾经沧海难为水，除却巫山不是云。——元稹《离思五首其四》', '君若扬路尘，妾若浊水泥，浮沈各异势，会合何时谐？——曹植《明月上高楼》',
                    '凄凉别后两应同，最是不胜清怨月明中。——纳兰性德《虞美人》', '自君之出矣，明镜暗不治。思君如流水，何有穷已时。——徐干《室思》',
                    '相见争如不见，有情何似无情。——司马光《西江月》', '落红不是无情物，化作春泥更护花。——龚自珍《己亥杂诗》',
                    '天不老，情难绝。心似双丝网，中有千千结。——张先《千秋岁》', '似此星辰非昨夜，为谁风露立中宵。——黄景仁《绮怀诗二首其一》',
                    '直道相思了无益，未妨惆怅是清狂。——李商隐《无题六首其三》', '十年生死两茫茫，不思量，自难忘，千里孤坟，无处话凄凉。——苏轼《江城子》',
                    '今夕何夕，见此良人。——佚名《诗经唐风绸缪》', '天长地久有时尽，此恨绵绵无绝期。——白居易《长恨歌》',
                    '在天愿作比翼鸟，在地愿为连理枝。——白居易《长恨歌》', '重叠泪痕缄锦字，人生只有情难死。——文廷式《蝶恋花》',
                    '一个是阆苑仙葩，一个是美玉无瑕。若说没奇缘，今生偏又遇著他；若说有奇缘，如何心事终虚话？——曹雪芹《枉凝眉》', '春蚕到死丝方尽，蜡炬成灰泪始干。——李商隐《无题》',
                    '他生莫作有情痴，人间无地著相思。——况周颐《减字浣溪沙》', '尊前拟把归期说，未语春容先惨咽。——欧阳修《玉楼春》',
                    '关关雎鸠，在河之洲。窈宨淑女，君子好逑。——佚名《诗经周南关雎》', '人生自是有情痴，此恨不关风与月。——欧阳修《玉楼春》',
                    '此去经年，应是良辰好景虚设。便纵有，千种风情，更与何人说。——柳永《雨霖铃》',
                    '两情若是久长时，又岂在朝朝暮暮。——秦观《鹊桥仙》', '入我相思门，知我相思苦，长相思兮长相忆，短相思兮无穷极。——李白《三五七言》',
                    '曾经沧海难为水，除却巫山不是云。——元稹《离思五首其四》', '君若扬路尘，妾若浊水泥，浮沈各异势，会合何时谐？——曹植《明月上高楼》',
                    '凄凉别后两应同，最是不胜清怨月明中。——纳兰性德《虞美人》', '自君之出矣，明镜暗不治。思君如流水，何有穷已时。——徐干《室思》',
                    '相见争如不见，有情何似无情。——司马光《西江月》', '落红不是无情物，化作春泥更护花。——龚自珍《己亥杂诗》',
                    '天不老，情难绝。心似双丝网，中有千千结。——张先《千秋岁》', '似此星辰非昨夜，为谁风露立中宵。——黄景仁《绮怀诗二首其一》',
                    '直道相思了无益，未妨惆怅是清狂。——李商隐《无题六首其三》', '十年生死两茫茫，不思量，自难忘，千里孤坟，无处话凄凉。——苏轼《江城子》',
                    '今夕何夕，见此良人。——佚名《诗经唐风绸缪》', '天长地久有时尽，此恨绵绵无绝期。——白居易《长恨歌》',
                    '在天愿作比翼鸟，在地愿为连理枝。——白居易《长恨歌》', '重叠泪痕缄锦字，人生只有情难死。——文廷式《蝶恋花》',
                    '一个是阆苑仙葩，一个是美玉无瑕。若说没奇缘，今生偏又遇著他；若说有奇缘，如何心事终虚话？——曹雪芹《枉凝眉》', '春蚕到死丝方尽，蜡炬成灰泪始干。——李商隐《无题》',
                    '他生莫作有情痴，人间无地著相思。——况周颐《减字浣溪沙》', '尊前拟把归期说，未语春容先惨咽。——欧阳修《玉楼春》',
                    '关关雎鸠，在河之洲。窈宨淑女，君子好逑。——佚名《诗经周南关雎》', '人生自是有情痴，此恨不关风与月。——欧阳修《玉楼春》',
                    '此去经年，应是良辰好景虚设。便纵有，千种风情，更与何人说。——柳永《雨霖铃》',
                    '两情若是久长时，又岂在朝朝暮暮。——秦观《鹊桥仙》', '入我相思门，知我相思苦，长相思兮长相忆，短相思兮无穷极。——李白《三五七言》',
                    '曾经沧海难为水，除却巫山不是云。——元稹《离思五首其四》', '君若扬路尘，妾若浊水泥，浮沈各异势，会合何时谐？——曹植《明月上高楼》',
                    '凄凉别后两应同，最是不胜清怨月明中。——纳兰性德《虞美人》', '自君之出矣，明镜暗不治。思君如流水，何有穷已时。——徐干《室思》',
                    '相见争如不见，有情何似无情。——司马光《西江月》', '落红不是无情物，化作春泥更护花。——龚自珍《己亥杂诗》',
                    '天不老，情难绝。心似双丝网，中有千千结。——张先《千秋岁》', '似此星辰非昨夜，为谁风露立中宵。——黄景仁《绮怀诗二首其一》',
                    '直道相思了无益，未妨惆怅是清狂。——李商隐《无题六首其三》', '十年生死两茫茫，不思量，自难忘，千里孤坟，无处话凄凉。——苏轼《江城子》',
                    '今夕何夕，见此良人。——佚名《诗经唐风绸缪》', '天长地久有时尽，此恨绵绵无绝期。——白居易《长恨歌》',
                    '在天愿作比翼鸟，在地愿为连理枝。——白居易《长恨歌》', '重叠泪痕缄锦字，人生只有情难死。——文廷式《蝶恋花》',
                    '一个是阆苑仙葩，一个是美玉无瑕。若说没奇缘，今生偏又遇著他；若说有奇缘，如何心事终虚话？——曹雪芹《枉凝眉》', '春蚕到死丝方尽，蜡炬成灰泪始干。——李商隐《无题》',
                    '他生莫作有情痴，人间无地著相思。——况周颐《减字浣溪沙》', '尊前拟把归期说，未语春容先惨咽。——欧阳修《玉楼春》',
                    '关关雎鸠，在河之洲。窈宨淑女，君子好逑。——佚名《诗经周南关雎》', '人生自是有情痴，此恨不关风与月。——欧阳修《玉楼春》',
                    '此去经年，应是良辰好景虚设。便纵有，千种风情，更与何人说。——柳永《雨霖铃》',
                    '两情若是久长时，又岂在朝朝暮暮。——秦观《鹊桥仙》', '入我相思门，知我相思苦，长相思兮长相忆，短相思兮无穷极。——李白《三五七言》',
                    '曾经沧海难为水，除却巫山不是云。——元稹《离思五首其四》', '君若扬路尘，妾若浊水泥，浮沈各异势，会合何时谐？——曹植《明月上高楼》',
                    '凄凉别后两应同，最是不胜清怨月明中。——纳兰性德《虞美人》', '自君之出矣，明镜暗不治。思君如流水，何有穷已时。——徐干《室思》',
                    '相见争如不见，有情何似无情。——司马光《西江月》', '落红不是无情物，化作春泥更护花。——龚自珍《己亥杂诗》',
                    '天不老，情难绝。心似双丝网，中有千千结。——张先《千秋岁》', '似此星辰非昨夜，为谁风露立中宵。——黄景仁《绮怀诗二首其一》',
                    '直道相思了无益，未妨惆怅是清狂。——李商隐《无题六首其三》', '十年生死两茫茫，不思量，自难忘，千里孤坟，无处话凄凉。——苏轼《江城子》',
                    '今夕何夕，见此良人。——佚名《诗经唐风绸缪》', '天长地久有时尽，此恨绵绵无绝期。——白居易《长恨歌》',
                    '在天愿作比翼鸟，在地愿为连理枝。——白居易《长恨歌》', '重叠泪痕缄锦字，人生只有情难死。——文廷式《蝶恋花》',
                    '一个是阆苑仙葩，一个是美玉无瑕。若说没奇缘，今生偏又遇著他；若说有奇缘，如何心事终虚话？——曹雪芹《枉凝眉》', '春蚕到死丝方尽，蜡炬成灰泪始干。——李商隐《无题》',
                    '他生莫作有情痴，人间无地著相思。——况周颐《减字浣溪沙》', '尊前拟把归期说，未语春容先惨咽。——欧阳修《玉楼春》',
                    '关关雎鸠，在河之洲。窈宨淑女，君子好逑。——佚名《诗经周南关雎》', '人生自是有情痴，此恨不关风与月。——欧阳修《玉楼春》',
                    '此去经年，应是良辰好景虚设。便纵有，千种风情，更与何人说。——柳永《雨霖铃》',
                    '两情若是久长时，又岂在朝朝暮暮。——秦观《鹊桥仙》', '入我相思门，知我相思苦，长相思兮长相忆，短相思兮无穷极。——李白《三五七言》',
                    '曾经沧海难为水，除却巫山不是云。——元稹《离思五首其四》', '君若扬路尘，妾若浊水泥，浮沈各异势，会合何时谐？——曹植《明月上高楼》',
                    '凄凉别后两应同，最是不胜清怨月明中。——纳兰性德《虞美人》', '自君之出矣，明镜暗不治。思君如流水，何有穷已时。——徐干《室思》',
                    '相见争如不见，有情何似无情。——司马光《西江月》', '落红不是无情物，化作春泥更护花。——龚自珍《己亥杂诗》',
                    '天不老，情难绝。心似双丝网，中有千千结。——张先《千秋岁》', '似此星辰非昨夜，为谁风露立中宵。——黄景仁《绮怀诗二首其一》',
                    '直道相思了无益，未妨惆怅是清狂。——李商隐《无题六首其三》', '十年生死两茫茫，不思量，自难忘，千里孤坟，无处话凄凉。——苏轼《江城子》',
                    '今夕何夕，见此良人。——佚名《诗经唐风绸缪》', '天长地久有时尽，此恨绵绵无绝期。——白居易《长恨歌》',
                    '在天愿作比翼鸟，在地愿为连理枝。——白居易《长恨歌》', '重叠泪痕缄锦字，人生只有情难死。——文廷式《蝶恋花》',
                    '一个是阆苑仙葩，一个是美玉无瑕。若说没奇缘，今生偏又遇著他；若说有奇缘，如何心事终虚话？——曹雪芹《枉凝眉》', '春蚕到死丝方尽，蜡炬成灰泪始干。——李商隐《无题》',
                    '他生莫作有情痴，人间无地著相思。——况周颐《减字浣溪沙》', '尊前拟把归期说，未语春容先惨咽。——欧阳修《玉楼春》',
                    '关关雎鸠，在河之洲。窈宨淑女，君子好逑。——佚名《诗经周南关雎》', '人生自是有情痴，此恨不关风与月。——欧阳修《玉楼春》',
                    '此去经年，应是良辰好景虚设。便纵有，千种风情，更与何人说。——柳永《雨霖铃》',
                    '两情若是久长时，又岂在朝朝暮暮。——秦观《鹊桥仙》', '入我相思门，知我相思苦，长相思兮长相忆，短相思兮无穷极。——李白《三五七言》',
                    '曾经沧海难为水，除却巫山不是云。——元稹《离思五首其四》', '君若扬路尘，妾若浊水泥，浮沈各异势，会合何时谐？——曹植《明月上高楼》',
                    '凄凉别后两应同，最是不胜清怨月明中。——纳兰性德《虞美人》', '自君之出矣，明镜暗不治。思君如流水，何有穷已时。——徐干《室思》',
                    '相见争如不见，有情何似无情。——司马光《西江月》', '落红不是无情物，化作春泥更护花。——龚自珍《己亥杂诗》',
                    '天不老，情难绝。心似双丝网，中有千千结。——张先《千秋岁》', '似此星辰非昨夜，为谁风露立中宵。——黄景仁《绮怀诗二首其一》',
                    '直道相思了无益，未妨惆怅是清狂。——李商隐《无题六首其三》', '十年生死两茫茫，不思量，自难忘，千里孤坟，无处话凄凉。——苏轼《江城子》',
                    '今夕何夕，见此良人。——佚名《诗经唐风绸缪》', '天长地久有时尽，此恨绵绵无绝期。——白居易《长恨歌》',
                    '在天愿作比翼鸟，在地愿为连理枝。——白居易《长恨歌》', '重叠泪痕缄锦字，人生只有情难死。——文廷式《蝶恋花》',
                    '一个是阆苑仙葩，一个是美玉无瑕。若说没奇缘，今生偏又遇著他；若说有奇缘，如何心事终虚话？——曹雪芹《枉凝眉》', '春蚕到死丝方尽，蜡炬成灰泪始干。——李商隐《无题》',
                    '他生莫作有情痴，人间无地著相思。——况周颐《减字浣溪沙》', '尊前拟把归期说，未语春容先惨咽。——欧阳修《玉楼春》',
                    '关关雎鸠，在河之洲。窈宨淑女，君子好逑。——佚名《诗经周南关雎》', '人生自是有情痴，此恨不关风与月。——欧阳修《玉楼春》',
                    '此去经年，应是良辰好景虚设。便纵有，千种风情，更与何人说。——柳永《雨霖铃》',
                    '两情若是久长时，又岂在朝朝暮暮。——秦观《鹊桥仙》', '入我相思门，知我相思苦，长相思兮长相忆，短相思兮无穷极。——李白《三五七言》',
                    '曾经沧海难为水，除却巫山不是云。——元稹《离思五首其四》', '君若扬路尘，妾若浊水泥，浮沈各异势，会合何时谐？——曹植《明月上高楼》',
                    '凄凉别后两应同，最是不胜清怨月明中。——纳兰性德《虞美人》', '自君之出矣，明镜暗不治。思君如流水，何有穷已时。——徐干《室思》',
                    '相见争如不见，有情何似无情。——司马光《西江月》', '落红不是无情物，化作春泥更护花。——龚自珍《己亥杂诗》',
                    '天不老，情难绝。心似双丝网，中有千千结。——张先《千秋岁》', '似此星辰非昨夜，为谁风露立中宵。——黄景仁《绮怀诗二首其一》',
                    '直道相思了无益，未妨惆怅是清狂。——李商隐《无题六首其三》', '十年生死两茫茫，不思量，自难忘，千里孤坟，无处话凄凉。——苏轼《江城子》',
                    '今夕何夕，见此良人。——佚名《诗经唐风绸缪》', '天长地久有时尽，此恨绵绵无绝期。——白居易《长恨歌》',
                    '在天愿作比翼鸟，在地愿为连理枝。——白居易《长恨歌》', '重叠泪痕缄锦字，人生只有情难死。——文廷式《蝶恋花》',
                    '一个是阆苑仙葩，一个是美玉无瑕。若说没奇缘，今生偏又遇著他；若说有奇缘，如何心事终虚话？——曹雪芹《枉凝眉》', '春蚕到死丝方尽，蜡炬成灰泪始干。——李商隐《无题》',
                    '他生莫作有情痴，人间无地著相思。——况周颐《减字浣溪沙》', '尊前拟把归期说，未语春容先惨咽。——欧阳修《玉楼春》',
                    '关关雎鸠，在河之洲。窈宨淑女，君子好逑。——佚名《诗经周南关雎》', '人生自是有情痴，此恨不关风与月。——欧阳修《玉楼春》',
                    '此去经年，应是良辰好景虚设。便纵有，千种风情，更与何人说。——柳永《雨霖铃》',
                    '两情若是久长时，又岂在朝朝暮暮。——秦观《鹊桥仙》', '入我相思门，知我相思苦，长相思兮长相忆，短相思兮无穷极。——李白《三五七言》',
                    '曾经沧海难为水，除却巫山不是云。——元稹《离思五首其四》', '君若扬路尘，妾若浊水泥，浮沈各异势，会合何时谐？——曹植《明月上高楼》',
                    '凄凉别后两应同，最是不胜清怨月明中。——纳兰性德《虞美人》', '自君之出矣，明镜暗不治。思君如流水，何有穷已时。——徐干《室思》',
                    '相见争如不见，有情何似无情。——司马光《西江月》', '落红不是无情物，化作春泥更护花。——龚自珍《己亥杂诗》',
                    '天不老，情难绝。心似双丝网，中有千千结。——张先《千秋岁》', '似此星辰非昨夜，为谁风露立中宵。——黄景仁《绮怀诗二首其一》',
                    '直道相思了无益，未妨惆怅是清狂。——李商隐《无题六首其三》', '十年生死两茫茫，不思量，自难忘，千里孤坟，无处话凄凉。——苏轼《江城子》',
                    '今夕何夕，见此良人。——佚名《诗经唐风绸缪》', '天长地久有时尽，此恨绵绵无绝期。——白居易《长恨歌》',
                    '在天愿作比翼鸟，在地愿为连理枝。——白居易《长恨歌》', '重叠泪痕缄锦字，人生只有情难死。——文廷式《蝶恋花》',
                    '一个是阆苑仙葩，一个是美玉无瑕。若说没奇缘，今生偏又遇著他；若说有奇缘，如何心事终虚话？——曹雪芹《枉凝眉》', '春蚕到死丝方尽，蜡炬成灰泪始干。——李商隐《无题》',
                    '他生莫作有情痴，人间无地著相思。——况周颐《减字浣溪沙》', '尊前拟把归期说，未语春容先惨咽。——欧阳修《玉楼春》',
                    '关关雎鸠，在河之洲。窈宨淑女，君子好逑。——佚名《诗经周南关雎》', '人生自是有情痴，此恨不关风与月。——欧阳修《玉楼春》',
                    '此去经年，应是良辰好景虚设。便纵有，千种风情，更与何人说。——柳永《雨霖铃》',
                    '两情若是久长时，又岂在朝朝暮暮。——秦观《鹊桥仙》', '入我相思门，知我相思苦，长相思兮长相忆，短相思兮无穷极。——李白《三五七言》',
                    '曾经沧海难为水，除却巫山不是云。——元稹《离思五首其四》', '君若扬路尘，妾若浊水泥，浮沈各异势，会合何时谐？——曹植《明月上高楼》',
                    '凄凉别后两应同，最是不胜清怨月明中。——纳兰性德《虞美人》', '自君之出矣，明镜暗不治。思君如流水，何有穷已时。——徐干《室思》',
                    '相见争如不见，有情何似无情。——司马光《西江月》', '落红不是无情物，化作春泥更护花。——龚自珍《己亥杂诗》',
                    '天不老，情难绝。心似双丝网，中有千千结。——张先《千秋岁》', '似此星辰非昨夜，为谁风露立中宵。——黄景仁《绮怀诗二首其一》',
                    '直道相思了无益，未妨惆怅是清狂。——李商隐《无题六首其三》', '十年生死两茫茫，不思量，自难忘，千里孤坟，无处话凄凉。——苏轼《江城子》',
                    '今夕何夕，见此良人。——佚名《诗经唐风绸缪》', '天长地久有时尽，此恨绵绵无绝期。——白居易《长恨歌》',
                    '在天愿作比翼鸟，在地愿为连理枝。——白居易《长恨歌》', '重叠泪痕缄锦字，人生只有情难死。——文廷式《蝶恋花》',
                    '一个是阆苑仙葩，一个是美玉无瑕。若说没奇缘，今生偏又遇著他；若说有奇缘，如何心事终虚话？——曹雪芹《枉凝眉》', '春蚕到死丝方尽，蜡炬成灰泪始干。——李商隐《无题》',
                    '他生莫作有情痴，人间无地著相思。——况周颐《减字浣溪沙》', '尊前拟把归期说，未语春容先惨咽。——欧阳修《玉楼春》',
                    '关关雎鸠，在河之洲。窈宨淑女，君子好逑。——佚名《诗经周南关雎》', '人生自是有情痴，此恨不关风与月。——欧阳修《玉楼春》',
                    '此去经年，应是良辰好景虚设。便纵有，千种风情，更与何人说。——柳永《雨霖铃》',
                    '两情若是久长时，又岂在朝朝暮暮。——秦观《鹊桥仙》', '入我相思门，知我相思苦，长相思兮长相忆，短相思兮无穷极。——李白《三五七言》',
                    '曾经沧海难为水，除却巫山不是云。——元稹《离思五首其四》', '君若扬路尘，妾若浊水泥，浮沈各异势，会合何时谐？——曹植《明月上高楼》',
                    '凄凉别后两应同，最是不胜清怨月明中。——纳兰性德《虞美人》', '自君之出矣，明镜暗不治。思君如流水，何有穷已时。——徐干《室思》',
                    '相见争如不见，有情何似无情。——司马光《西江月》', '落红不是无情物，化作春泥更护花。——龚自珍《己亥杂诗》',
                    '天不老，情难绝。心似双丝网，中有千千结。——张先《千秋岁》', '似此星辰非昨夜，为谁风露立中宵。——黄景仁《绮怀诗二首其一》',
                    '直道相思了无益，未妨惆怅是清狂。——李商隐《无题六首其三》', '十年生死两茫茫，不思量，自难忘，千里孤坟，无处话凄凉。——苏轼《江城子》',
                    '今夕何夕，见此良人。——佚名《诗经唐风绸缪》', '天长地久有时尽，此恨绵绵无绝期。——白居易《长恨歌》',
                    '在天愿作比翼鸟，在地愿为连理枝。——白居易《长恨歌》', '重叠泪痕缄锦字，人生只有情难死。——文廷式《蝶恋花》',
                    '一个是阆苑仙葩，一个是美玉无瑕。若说没奇缘，今生偏又遇著他；若说有奇缘，如何心事终虚话？——曹雪芹《枉凝眉》', '春蚕到死丝方尽，蜡炬成灰泪始干。——李商隐《无题》',
                    '他生莫作有情痴，人间无地著相思。——况周颐《减字浣溪沙》', '尊前拟把归期说，未语春容先惨咽。——欧阳修《玉楼春》',
                    '关关雎鸠，在河之洲。窈宨淑女，君子好逑。——佚名《诗经周南关雎》', '人生自是有情痴，此恨不关风与月。——欧阳修《玉楼春》',
                    '此去经年，应是良辰好景虚设。便纵有，千种风情，更与何人说。——柳永《雨霖铃》',
                    '两情若是久长时，又岂在朝朝暮暮。——秦观《鹊桥仙》', '入我相思门，知我相思苦，长相思兮长相忆，短相思兮无穷极。——李白《三五七言》',
                    '曾经沧海难为水，除却巫山不是云。——元稹《离思五首其四》', '君若扬路尘，妾若浊水泥，浮沈各异势，会合何时谐？——曹植《明月上高楼》',
                    '凄凉别后两应同，最是不胜清怨月明中。——纳兰性德《虞美人》', '自君之出矣，明镜暗不治。思君如流水，何有穷已时。——徐干《室思》',
                    '相见争如不见，有情何似无情。——司马光《西江月》', '落红不是无情物，化作春泥更护花。——龚自珍《己亥杂诗》',
                    '天不老，情难绝。心似双丝网，中有千千结。——张先《千秋岁》', '似此星辰非昨夜，为谁风露立中宵。——黄景仁《绮怀诗二首其一》',
                    '直道相思了无益，未妨惆怅是清狂。——李商隐《无题六首其三》', '十年生死两茫茫，不思量，自难忘，千里孤坟，无处话凄凉。——苏轼《江城子》',
                    '今夕何夕，见此良人。——佚名《诗经唐风绸缪》', '天长地久有时尽，此恨绵绵无绝期。——白居易《长恨歌》',
                    '在天愿作比翼鸟，在地愿为连理枝。——白居易《长恨歌》', '重叠泪痕缄锦字，人生只有情难死。——文廷式《蝶恋花》',
                    '一个是阆苑仙葩，一个是美玉无瑕。若说没奇缘，今生偏又遇著他；若说有奇缘，如何心事终虚话？——曹雪芹《枉凝眉》', '春蚕到死丝方尽，蜡炬成灰泪始干。——李商隐《无题》',
                    '他生莫作有情痴，人间无地著相思。——况周颐《减字浣溪沙》', '尊前拟把归期说，未语春容先惨咽。——欧阳修《玉楼春》',
                    '关关雎鸠，在河之洲。窈宨淑女，君子好逑。——佚名《诗经周南关雎》', '人生自是有情痴，此恨不关风与月。——欧阳修《玉楼春》',
                    '此去经年，应是良辰好景虚设。便纵有，千种风情，更与何人说。——柳永《雨霖铃》',
                    '两情若是久长时，又岂在朝朝暮暮。——秦观《鹊桥仙》', '入我相思门，知我相思苦，长相思兮长相忆，短相思兮无穷极。——李白《三五七言》',
                    '曾经沧海难为水，除却巫山不是云。——元稹《离思五首其四》', '君若扬路尘，妾若浊水泥，浮沈各异势，会合何时谐？——曹植《明月上高楼》',
                    '凄凉别后两应同，最是不胜清怨月明中。——纳兰性德《虞美人》', '自君之出矣，明镜暗不治。思君如流水，何有穷已时。——徐干《室思》',
                    '相见争如不见，有情何似无情。——司马光《西江月》', '落红不是无情物，化作春泥更护花。——龚自珍《己亥杂诗》',
                    '天不老，情难绝。心似双丝网，中有千千结。——张先《千秋岁》', '似此星辰非昨夜，为谁风露立中宵。——黄景仁《绮怀诗二首其一》',
                    '直道相思了无益，未妨惆怅是清狂。——李商隐《无题六首其三》', '十年生死两茫茫，不思量，自难忘，千里孤坟，无处话凄凉。——苏轼《江城子》',
                    '今夕何夕，见此良人。——佚名《诗经唐风绸缪》', '天长地久有时尽，此恨绵绵无绝期。——白居易《长恨歌》',
                    '在天愿作比翼鸟，在地愿为连理枝。——白居易《长恨歌》', '重叠泪痕缄锦字，人生只有情难死。——文廷式《蝶恋花》',
                    '一个是阆苑仙葩，一个是美玉无瑕。若说没奇缘，今生偏又遇著他；若说有奇缘，如何心事终虚话？——曹雪芹《枉凝眉》', '春蚕到死丝方尽，蜡炬成灰泪始干。——李商隐《无题》',
                    '他生莫作有情痴，人间无地著相思。——况周颐《减字浣溪沙》', '尊前拟把归期说，未语春容先惨咽。——欧阳修《玉楼春》',
                    '关关雎鸠，在河之洲。窈宨淑女，君子好逑。——佚名《诗经周南关雎》', '人生自是有情痴，此恨不关风与月。——欧阳修《玉楼春》',
                    '此去经年，应是良辰好景虚设。便纵有，千种风情，更与何人说。——柳永《雨霖铃》',
                    '两情若是久长时，又岂在朝朝暮暮。——秦观《鹊桥仙》', '入我相思门，知我相思苦，长相思兮长相忆，短相思兮无穷极。——李白《三五七言》',
                    '曾经沧海难为水，除却巫山不是云。——元稹《离思五首其四》', '君若扬路尘，妾若浊水泥，浮沈各异势，会合何时谐？——曹植《明月上高楼》',
                    '凄凉别后两应同，最是不胜清怨月明中。——纳兰性德《虞美人》', '自君之出矣，明镜暗不治。思君如流水，何有穷已时。——徐干《室思》',
                    '相见争如不见，有情何似无情。——司马光《西江月》', '落红不是无情物，化作春泥更护花。——龚自珍《己亥杂诗》',
                    '天不老，情难绝。心似双丝网，中有千千结。——张先《千秋岁》', '似此星辰非昨夜，为谁风露立中宵。——黄景仁《绮怀诗二首其一》',
                    '直道相思了无益，未妨惆怅是清狂。——李商隐《无题六首其三》', '十年生死两茫茫，不思量，自难忘，千里孤坟，无处话凄凉。——苏轼《江城子》',
                    '今夕何夕，见此良人。——佚名《诗经唐风绸缪》', '天长地久有时尽，此恨绵绵无绝期。——白居易《长恨歌》',
                    '在天愿作比翼鸟，在地愿为连理枝。——白居易《长恨歌》', '重叠泪痕缄锦字，人生只有情难死。——文廷式《蝶恋花》',
                    '一个是阆苑仙葩，一个是美玉无瑕。若说没奇缘，今生偏又遇著他；若说有奇缘，如何心事终虚话？——曹雪芹《枉凝眉》', '春蚕到死丝方尽，蜡炬成灰泪始干。——李商隐《无题》',
                    '他生莫作有情痴，人间无地著相思。——况周颐《减字浣溪沙》', '尊前拟把归期说，未语春容先惨咽。——欧阳修《玉楼春》',
                    '关关雎鸠，在河之洲。窈宨淑女，君子好逑。——佚名《诗经周南关雎》', '人生自是有情痴，此恨不关风与月。——欧阳修《玉楼春》',
                    '此去经年，应是良辰好景虚设。便纵有，千种风情，更与何人说。——柳永《雨霖铃》',
                    '两情若是久长时，又岂在朝朝暮暮。——秦观《鹊桥仙》', '入我相思门，知我相思苦，长相思兮长相忆，短相思兮无穷极。——李白《三五七言》',
                    '曾经沧海难为水，除却巫山不是云。——元稹《离思五首其四》', '君若扬路尘，妾若浊水泥，浮沈各异势，会合何时谐？——曹植《明月上高楼》',
                    '凄凉别后两应同，最是不胜清怨月明中。——纳兰性德《虞美人》', '自君之出矣，明镜暗不治。思君如流水，何有穷已时。——徐干《室思》',
                    '相见争如不见，有情何似无情。——司马光《西江月》', '落红不是无情物，化作春泥更护花。——龚自珍《己亥杂诗》',
                    '天不老，情难绝。心似双丝网，中有千千结。——张先《千秋岁》', '似此星辰非昨夜，为谁风露立中宵。——黄景仁《绮怀诗二首其一》',
                    '直道相思了无益，未妨惆怅是清狂。——李商隐《无题六首其三》', '十年生死两茫茫，不思量，自难忘，千里孤坟，无处话凄凉。——苏轼《江城子》',
                    '今夕何夕，见此良人。——佚名《诗经唐风绸缪》', '天长地久有时尽，此恨绵绵无绝期。——白居易《长恨歌》',
                    '在天愿作比翼鸟，在地愿为连理枝。——白居易《长恨歌》', '重叠泪痕缄锦字，人生只有情难死。——文廷式《蝶恋花》',
                    '一个是阆苑仙葩，一个是美玉无瑕。若说没奇缘，今生偏又遇著他；若说有奇缘，如何心事终虚话？——曹雪芹《枉凝眉》', '春蚕到死丝方尽，蜡炬成灰泪始干。——李商隐《无题》',
                    '他生莫作有情痴，人间无地著相思。——况周颐《减字浣溪沙》', '尊前拟把归期说，未语春容先惨咽。——欧阳修《玉楼春》',
                    '关关雎鸠，在河之洲。窈宨淑女，君子好逑。——佚名《诗经周南关雎》', '人生自是有情痴，此恨不关风与月。——欧阳修《玉楼春》',
                    '此去经年，应是良辰好景虚设。便纵有，千种风情，更与何人说。——柳永《雨霖铃》',
                    '两情若是久长时，又岂在朝朝暮暮。——秦观《鹊桥仙》', '入我相思门，知我相思苦，长相思兮长相忆，短相思兮无穷极。——李白《三五七言》',
                    '曾经沧海难为水，除却巫山不是云。——元稹《离思五首其四》', '君若扬路尘，妾若浊水泥，浮沈各异势，会合何时谐？——曹植《明月上高楼》',
                    '凄凉别后两应同，最是不胜清怨月明中。——纳兰性德《虞美人》', '自君之出矣，明镜暗不治。思君如流水，何有穷已时。——徐干《室思》',
                    '相见争如不见，有情何似无情。——司马光《西江月》', '落红不是无情物，化作春泥更护花。——龚自珍《己亥杂诗》',
                    '天不老，情难绝。心似双丝网，中有千千结。——张先《千秋岁》', '似此星辰非昨夜，为谁风露立中宵。——黄景仁《绮怀诗二首其一》',
                    '直道相思了无益，未妨惆怅是清狂。——李商隐《无题六首其三》', '十年生死两茫茫，不思量，自难忘，千里孤坟，无处话凄凉。——苏轼《江城子》',
                    '今夕何夕，见此良人。——佚名《诗经唐风绸缪》', '天长地久有时尽，此恨绵绵无绝期。——白居易《长恨歌》',
                    '在天愿作比翼鸟，在地愿为连理枝。——白居易《长恨歌》', '重叠泪痕缄锦字，人生只有情难死。——文廷式《蝶恋花》',
                    '一个是阆苑仙葩，一个是美玉无瑕。若说没奇缘，今生偏又遇著他；若说有奇缘，如何心事终虚话？——曹雪芹《枉凝眉》', '春蚕到死丝方尽，蜡炬成灰泪始干。——李商隐《无题》',
                    '他生莫作有情痴，人间无地著相思。——况周颐《减字浣溪沙》', '尊前拟把归期说，未语春容先惨咽。——欧阳修《玉楼春》',
                    '关关雎鸠，在河之洲。窈宨淑女，君子好逑。——佚名《诗经周南关雎》', '人生自是有情痴，此恨不关风与月。——欧阳修《玉楼春》',
                    '此去经年，应是良辰好景虚设。便纵有，千种风情，更与何人说。——柳永《雨霖铃》',
                    '两情若是久长时，又岂在朝朝暮暮。——秦观《鹊桥仙》', '入我相思门，知我相思苦，长相思兮长相忆，短相思兮无穷极。——李白《三五七言》',
                    '曾经沧海难为水，除却巫山不是云。——元稹《离思五首其四》', '君若扬路尘，妾若浊水泥，浮沈各异势，会合何时谐？——曹植《明月上高楼》',
                    '凄凉别后两应同，最是不胜清怨月明中。——纳兰性德《虞美人》', '自君之出矣，明镜暗不治。思君如流水，何有穷已时。——徐干《室思》',
                    '相见争如不见，有情何似无情。——司马光《西江月》', '落红不是无情物，化作春泥更护花。——龚自珍《己亥杂诗》',
                    '天不老，情难绝。心似双丝网，中有千千结。——张先《千秋岁》', '似此星辰非昨夜，为谁风露立中宵。——黄景仁《绮怀诗二首其一》',
                    '直道相思了无益，未妨惆怅是清狂。——李商隐《无题六首其三》', '十年生死两茫茫，不思量，自难忘，千里孤坟，无处话凄凉。——苏轼《江城子》',
                    '今夕何夕，见此良人。——佚名《诗经唐风绸缪》', '天长地久有时尽，此恨绵绵无绝期。——白居易《长恨歌》',
                    '在天愿作比翼鸟，在地愿为连理枝。——白居易《长恨歌》', '重叠泪痕缄锦字，人生只有情难死。——文廷式《蝶恋花》',
                    '一个是阆苑仙葩，一个是美玉无瑕。若说没奇缘，今生偏又遇著他；若说有奇缘，如何心事终虚话？——曹雪芹《枉凝眉》', '春蚕到死丝方尽，蜡炬成灰泪始干。——李商隐《无题》',
                    '他生莫作有情痴，人间无地著相思。——况周颐《减字浣溪沙》', '尊前拟把归期说，未语春容先惨咽。——欧阳修《玉楼春》',
                    '关关雎鸠，在河之洲。窈宨淑女，君子好逑。——佚名《诗经周南关雎》', '人生自是有情痴，此恨不关风与月。——欧阳修《玉楼春》',
                    '此去经年，应是良辰好景虚设。便纵有，千种风情，更与何人说。——柳永《雨霖铃》',
                    '两情若是久长时，又岂在朝朝暮暮。——秦观《鹊桥仙》', '入我相思门，知我相思苦，长相思兮长相忆，短相思兮无穷极。——李白《三五七言》',
                    '曾经沧海难为水，除却巫山不是云。——元稹《离思五首其四》', '君若扬路尘，妾若浊水泥，浮沈各异势，会合何时谐？——曹植《明月上高楼》',
                    '凄凉别后两应同，最是不胜清怨月明中。——纳兰性德《虞美人》', '自君之出矣，明镜暗不治。思君如流水，何有穷已时。——徐干《室思》',
                    '相见争如不见，有情何似无情。——司马光《西江月》', '落红不是无情物，化作春泥更护花。——龚自珍《己亥杂诗》',
                    '天不老，情难绝。心似双丝网，中有千千结。——张先《千秋岁》', '似此星辰非昨夜，为谁风露立中宵。——黄景仁《绮怀诗二首其一》',
                    '直道相思了无益，未妨惆怅是清狂。——李商隐《无题六首其三》', '十年生死两茫茫，不思量，自难忘，千里孤坟，无处话凄凉。——苏轼《江城子》',
                    '今夕何夕，见此良人。——佚名《诗经唐风绸缪》', '天长地久有时尽，此恨绵绵无绝期。——白居易《长恨歌》',
                    '在天愿作比翼鸟，在地愿为连理枝。——白居易《长恨歌》', '重叠泪痕缄锦字，人生只有情难死。——文廷式《蝶恋花》',
                    '一个是阆苑仙葩，一个是美玉无瑕。若说没奇缘，今生偏又遇著他；若说有奇缘，如何心事终虚话？——曹雪芹《枉凝眉》', '春蚕到死丝方尽，蜡炬成灰泪始干。——李商隐《无题》',
                    '他生莫作有情痴，人间无地著相思。——况周颐《减字浣溪沙》', '尊前拟把归期说，未语春容先惨咽。——欧阳修《玉楼春》',
                    '关关雎鸠，在河之洲。窈宨淑女，君子好逑。——佚名《诗经周南关雎》', '人生自是有情痴，此恨不关风与月。——欧阳修《玉楼春》',
                    '此去经年，应是良辰好景虚设。便纵有，千种风情，更与何人说。——柳永《雨霖铃》',
                    '两情若是久长时，又岂在朝朝暮暮。——秦观《鹊桥仙》', '入我相思门，知我相思苦，长相思兮长相忆，短相思兮无穷极。——李白《三五七言》',
                    '曾经沧海难为水，除却巫山不是云。——元稹《离思五首其四》', '君若扬路尘，妾若浊水泥，浮沈各异势，会合何时谐？——曹植《明月上高楼》',
                    '凄凉别后两应同，最是不胜清怨月明中。——纳兰性德《虞美人》', '自君之出矣，明镜暗不治。思君如流水，何有穷已时。——徐干《室思》',
                    '相见争如不见，有情何似无情。——司马光《西江月》', '落红不是无情物，化作春泥更护花。——龚自珍《己亥杂诗》',
                    '天不老，情难绝。心似双丝网，中有千千结。——张先《千秋岁》', '似此星辰非昨夜，为谁风露立中宵。——黄景仁《绮怀诗二首其一》',
                    '直道相思了无益，未妨惆怅是清狂。——李商隐《无题六首其三》', '十年生死两茫茫，不思量，自难忘，千里孤坟，无处话凄凉。——苏轼《江城子》',
                    '今夕何夕，见此良人。——佚名《诗经唐风绸缪》', '天长地久有时尽，此恨绵绵无绝期。——白居易《长恨歌》',
                    '在天愿作比翼鸟，在地愿为连理枝。——白居易《长恨歌》', '重叠泪痕缄锦字，人生只有情难死。——文廷式《蝶恋花》',
                    '一个是阆苑仙葩，一个是美玉无瑕。若说没奇缘，今生偏又遇著他；若说有奇缘，如何心事终虚话？——曹雪芹《枉凝眉》', '春蚕到死丝方尽，蜡炬成灰泪始干。——李商隐《无题》',
                    '他生莫作有情痴，人间无地著相思。——况周颐《减字浣溪沙》', '尊前拟把归期说，未语春容先惨咽。——欧阳修《玉楼春》',
                    '关关雎鸠，在河之洲。窈宨淑女，君子好逑。——佚名《诗经周南关雎》', '人生自是有情痴，此恨不关风与月。——欧阳修《玉楼春》',
                    '此去经年，应是良辰好景虚设。便纵有，千种风情，更与何人说。——柳永《雨霖铃》',
                    '两情若是久长时，又岂在朝朝暮暮。——秦观《鹊桥仙》', '入我相思门，知我相思苦，长相思兮长相忆，短相思兮无穷极。——李白《三五七言》',
                    '曾经沧海难为水，除却巫山不是云。——元稹《离思五首其四》', '君若扬路尘，妾若浊水泥，浮沈各异势，会合何时谐？——曹植《明月上高楼》',
                    '凄凉别后两应同，最是不胜清怨月明中。——纳兰性德《虞美人》', '自君之出矣，明镜暗不治。思君如流水，何有穷已时。——徐干《室思》',
                    '相见争如不见，有情何似无情。——司马光《西江月》', '落红不是无情物，化作春泥更护花。——龚自珍《己亥杂诗》',
                    '天不老，情难绝。心似双丝网，中有千千结。——张先《千秋岁》', '似此星辰非昨夜，为谁风露立中宵。——黄景仁《绮怀诗二首其一》',
                    '直道相思了无益，未妨惆怅是清狂。——李商隐《无题六首其三》', '十年生死两茫茫，不思量，自难忘，千里孤坟，无处话凄凉。——苏轼《江城子》',
                    '今夕何夕，见此良人。——佚名《诗经唐风绸缪》', '天长地久有时尽，此恨绵绵无绝期。——白居易《长恨歌》',
                    '在天愿作比翼鸟，在地愿为连理枝。——白居易《长恨歌》', '重叠泪痕缄锦字，人生只有情难死。——文廷式《蝶恋花》',
                    '一个是阆苑仙葩，一个是美玉无瑕。若说没奇缘，今生偏又遇著他；若说有奇缘，如何心事终虚话？——曹雪芹《枉凝眉》', '春蚕到死丝方尽，蜡炬成灰泪始干。——李商隐《无题》',
                    '他生莫作有情痴，人间无地著相思。——况周颐《减字浣溪沙》', '尊前拟把归期说，未语春容先惨咽。——欧阳修《玉楼春》',
                    '关关雎鸠，在河之洲。窈宨淑女，君子好逑。——佚名《诗经周南关雎》', '人生自是有情痴，此恨不关风与月。——欧阳修《玉楼春》',
                    '此去经年，应是良辰好景虚设。便纵有，千种风情，更与何人说。——柳永《雨霖铃》',
                    '两情若是久长时，又岂在朝朝暮暮。——秦观《鹊桥仙》', '入我相思门，知我相思苦，长相思兮长相忆，短相思兮无穷极。——李白《三五七言》',
                    '曾经沧海难为水，除却巫山不是云。——元稹《离思五首其四》', '君若扬路尘，妾若浊水泥，浮沈各异势，会合何时谐？——曹植《明月上高楼》',
                    '凄凉别后两应同，最是不胜清怨月明中。——纳兰性德《虞美人》', '自君之出矣，明镜暗不治。思君如流水，何有穷已时。——徐干《室思》',
                    '相见争如不见，有情何似无情。——司马光《西江月》', '落红不是无情物，化作春泥更护花。——龚自珍《己亥杂诗》',
                    '天不老，情难绝。心似双丝网，中有千千结。——张先《千秋岁》', '似此星辰非昨夜，为谁风露立中宵。——黄景仁《绮怀诗二首其一》',
                    '直道相思了无益，未妨惆怅是清狂。——李商隐《无题六首其三》', '十年生死两茫茫，不思量，自难忘，千里孤坟，无处话凄凉。——苏轼《江城子》',
                    '今夕何夕，见此良人。——佚名《诗经唐风绸缪》', '天长地久有时尽，此恨绵绵无绝期。——白居易《长恨歌》',
                    '在天愿作比翼鸟，在地愿为连理枝。——白居易《长恨歌》', '重叠泪痕缄锦字，人生只有情难死。——文廷式《蝶恋花》',
                    '一个是阆苑仙葩，一个是美玉无瑕。若说没奇缘，今生偏又遇著他；若说有奇缘，如何心事终虚话？——曹雪芹《枉凝眉》', '春蚕到死丝方尽，蜡炬成灰泪始干。——李商隐《无题》',
                    '他生莫作有情痴，人间无地著相思。——况周颐《减字浣溪沙》', '尊前拟把归期说，未语春容先惨咽。——欧阳修《玉楼春》',
                    '关关雎鸠，在河之洲。窈宨淑女，君子好逑。——佚名《诗经周南关雎》', '人生自是有情痴，此恨不关风与月。——欧阳修《玉楼春》',
                    '此去经年，应是良辰好景虚设。便纵有，千种风情，更与何人说。——柳永《雨霖铃》',
                    '两情若是久长时，又岂在朝朝暮暮。——秦观《鹊桥仙》', '入我相思门，知我相思苦，长相思兮长相忆，短相思兮无穷极。——李白《三五七言》',
                    '曾经沧海难为水，除却巫山不是云。——元稹《离思五首其四》', '君若扬路尘，妾若浊水泥，浮沈各异势，会合何时谐？——曹植《明月上高楼》',
                    '凄凉别后两应同，最是不胜清怨月明中。——纳兰性德《虞美人》', '自君之出矣，明镜暗不治。思君如流水，何有穷已时。——徐干《室思》',
                    '相见争如不见，有情何似无情。——司马光《西江月》', '落红不是无情物，化作春泥更护花。——龚自珍《己亥杂诗》',
                    '天不老，情难绝。心似双丝网，中有千千结。——张先《千秋岁》', '似此星辰非昨夜，为谁风露立中宵。——黄景仁《绮怀诗二首其一》',
                    '直道相思了无益，未妨惆怅是清狂。——李商隐《无题六首其三》', '十年生死两茫茫，不思量，自难忘，千里孤坟，无处话凄凉。——苏轼《江城子》',
                    '今夕何夕，见此良人。——佚名《诗经唐风绸缪》', '天长地久有时尽，此恨绵绵无绝期。——白居易《长恨歌》',
                    '在天愿作比翼鸟，在地愿为连理枝。——白居易《长恨歌》', '重叠泪痕缄锦字，人生只有情难死。——文廷式《蝶恋花》',
                    '一个是阆苑仙葩，一个是美玉无瑕。若说没奇缘，今生偏又遇著他；若说有奇缘，如何心事终虚话？——曹雪芹《枉凝眉》', '春蚕到死丝方尽，蜡炬成灰泪始干。——李商隐《无题》',
                    '他生莫作有情痴，人间无地著相思。——况周颐《减字浣溪沙》', '尊前拟把归期说，未语春容先惨咽。——欧阳修《玉楼春》',
                    '关关雎鸠，在河之洲。窈宨淑女，君子好逑。——佚名《诗经周南关雎》', '人生自是有情痴，此恨不关风与月。——欧阳修《玉楼春》',
                    '此去经年，应是良辰好景虚设。便纵有，千种风情，更与何人说。——柳永《雨霖铃》',
                    '两情若是久长时，又岂在朝朝暮暮。——秦观《鹊桥仙》', '入我相思门，知我相思苦，长相思兮长相忆，短相思兮无穷极。——李白《三五七言》',
                    '曾经沧海难为水，除却巫山不是云。——元稹《离思五首其四》', '君若扬路尘，妾若浊水泥，浮沈各异势，会合何时谐？——曹植《明月上高楼》',
                    '凄凉别后两应同，最是不胜清怨月明中。——纳兰性德《虞美人》', '自君之出矣，明镜暗不治。思君如流水，何有穷已时。——徐干《室思》',
                    '相见争如不见，有情何似无情。——司马光《西江月》', '落红不是无情物，化作春泥更护花。——龚自珍《己亥杂诗》',
                    '天不老，情难绝。心似双丝网，中有千千结。——张先《千秋岁》', '似此星辰非昨夜，为谁风露立中宵。——黄景仁《绮怀诗二首其一》',
                    '直道相思了无益，未妨惆怅是清狂。——李商隐《无题六首其三》', '十年生死两茫茫，不思量，自难忘，千里孤坟，无处话凄凉。——苏轼《江城子》',
                    '今夕何夕，见此良人。——佚名《诗经唐风绸缪》', '天长地久有时尽，此恨绵绵无绝期。——白居易《长恨歌》',
                    '在天愿作比翼鸟，在地愿为连理枝。——白居易《长恨歌》', '重叠泪痕缄锦字，人生只有情难死。——文廷式《蝶恋花》',
                    '一个是阆苑仙葩，一个是美玉无瑕。若说没奇缘，今生偏又遇著他；若说有奇缘，如何心事终虚话？——曹雪芹《枉凝眉》', '春蚕到死丝方尽，蜡炬成灰泪始干。——李商隐《无题》',
                    '他生莫作有情痴，人间无地著相思。——况周颐《减字浣溪沙》', '尊前拟把归期说，未语春容先惨咽。——欧阳修《玉楼春》',
                    '关关雎鸠，在河之洲。窈宨淑女，君子好逑。——佚名《诗经周南关雎》', '人生自是有情痴，此恨不关风与月。——欧阳修《玉楼春》',
                    '此去经年，应是良辰好景虚设。便纵有，千种风情，更与何人说。——柳永《雨霖铃》'
                    ]
    for poetrys1 in range(len(poetrys_data)):
        poetry2.objects.create(poetrys_id=poetrys1 + 1, poetrys=poetrys_data[poetrys1])
    # poetry2.objects.create(poetrys_id = 1,poetrys = '两情若是久长时，又岂在朝朝暮暮。——秦观《鹊桥仙》')
    return HttpResponse('添加成功！')


def delete_data(request):
    poetry2.objects.filter(poetrys_id=1).delete()
    return HttpResponse('删除成功！')


def update_data(request):
    poetry2.objects.filter(poetrys_id=1).update(poetrys='富强，民主')
    return HttpResponse('修改成功！')


def select_data(request):
    # data_all =  poetry2.objects.all()#查询全部
    # for i in data_all:
    #     print(i.poetrys_id)
    #     print(i.poetrys)
    # select_d = poetry2.objects.filter(poetrys_id = 10)#按条件查找
    # for i in select_d:
    #     print(i.poetrys)
    data_all = poetry2.objects.all()[:5]  # 查询数据的前十行
    for i in data_all:
        print(i.poetrys_id)
        print(i.poetrys)

    return HttpResponse('查询成功！')