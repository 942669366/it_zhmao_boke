# """
#
# 自定义分页组件
#
# """
from django.utils.safestring import mark_safe
#
#
# class Pagetions(object):
#     def __init__(self, request, queryset, page_param='page', page_size=10, plus=3):
#         page = int(request.GET.get(page_param, "1"))
#         # if page.isdecimal:
#         #     page = int(page)
#         # else:
#         #     page = 1
#
#         self.page = page
#         self.page_size = page_size
#
#         self.start = (page - 1) * page_size  # 开始数据
#         self.end = page * page_size  # 结束数据
#
#         self.page_queryset = queryset[self.start: self.end]
#
#         # 查询数据库中所有数据的  个数
#         total_count = queryset.count()
#         # 总页码
#         total_page_count, div = divmod(total_count, page_size)
#         if div:
#             total_page_count += 1
#         self.total_page_count = total_page_count
#         self.plus = plus
#
#     def html(self):
#         # 计算页码显示 前后页数
#
#         # 极致的判断
#         if self.total_page_count <= 2 * self.plus + 1:
#             start_page = 1
#             end_page = self.total_page_count
#         else:
#
#             # 第一页的极值处理方式 当数据小于 3
#             if self.page <= self.plus:
#                 start_page = 1
#                 end_page = 2 * self.plus + 1
#             else:
#                 # 最后一页极值 处理方式
#                 if self.page + self.plus > self.total_page_count:
#                     end_page = self.total_page_count
#                     start_page = self.total_page_count - 2 * self.plus
#                 else:
#                     start_page = self.page - self.plus
#                     end_page = self.page + self.plus
#
#         # 页码
#         page_str_list = []
#
#         # 首页
#         page_str_list.append('<li class="hidden-xs"><a href="?page={}"> 首页 </a></li>'.format(1))
#         # 上一页
#         if self.page > 1:
#             pev = '<li><a href="?page={}"> 上一页 </a></li>'.format(self.page - 1)
#         else:
#             pev = '<li><a href="?page={}"> 上一页 </a></li>'.format(1)
#         page_str_list.append(pev)
#
#         # 中间页面
#         for i in range(start_page, end_page + 1):
#             if i == self.page:
#                 ele = '<li class="active"><a href="?page={}">{}</a></li>'.format(i, i)
#             else:
#                 ele = '<li><a href="?page={}">{}</a></li>'.format(i, i)
#             page_str_list.append(ele)
#
#         # 下一页
#         if self.page < self.total_page_count:
#             pev = '<li><a href="?page={}"> 下一页 </a></li>'.format(self.page + 1)
#         else:
#             pev = '<li><a href="?page={}"> 下一页 </a></li>'.format(self.total_page_count)
#         page_str_list.append(pev)
#
#         # 尾页
#         page_str_list.append('<li class="hidden-xs"><a href="?page={}"> 尾页 </a></li>'.format(self.total_page_count))
#
#         # 调转页面
#         search_str ='''
#                 <form method="get">
#                     <div class="col-sm-3 hidden-xs">
#                         <div class="input-group">
#                           <input type="text" name="page" class="form-control" placeholder="搜索">
#                           <span class="input-group-btn">
#                             <button class="btn btn-default" type="submit">跳转</button>
#                           </span>
#                         </div>
#                     </div>
#                 </form>
#             '''
#         page_str_list.append(search_str)
#         # mark_safe() 需要导包
#         page_string = mark_safe(''.join(page_str_list))
#         return page_string


class Pagination(object):
    def __init__(self, current_page, all_count, per_page_num=2, pager_count=11):

        try:
            current_page = int(current_page)
        except Exception as e:
            current_page = 1

        if current_page < 1:
            current_page = 1

            self.current_page = current_page

            self.all_count = all_count
            self.per_page_num = per_page_num

        # 总页码
        all_pager, tmp = divmod(all_count, per_page_num)
        if tmp:
            all_pager += 1
        self.all_pager = all_pager

        self.pager_count = pager_count
        self.pager_count_half = int((pager_count - 1) / 2)


    @property
    def start(self):
        return (self.current_page - 1) * self.per_page_num


    @property
    def end(self):
        return self.current_page * self.per_page_num


    def page_html(self):
        # 如果总页码 < 11个：
        if self.all_pager <= self.pager_count:
            pager_start = 1
            pager_end = self.all_pager + 1
        # 总页码 > 11
        else:
            # 当前页如果<=页面上最多显示11/2个页码
            if self.current_page <= self.pager_count_half:
                pager_start = 1
                pager_end = self.pager_count + 1

            # 当前页大于5
            else:
            # 页码翻到最后
                if (self.current_page + self.pager_count_half) > self.all_pager:
                    pager_end = self.all_pager + 1
                    pager_start = self.all_pager - self.pager_count + 1
                else:
                    pager_start = self.current_page - self.pager_count_half
                    pager_end = self.current_page + self.pager_count_half + 1

        page_html_list = []
        # 添加前面的nav和ul标签
        page_html_list.append('''
        <nav aria-label='Page navigation' style="text-align: center;">
        <ul class='pagination'>
        ''')
        first_page = '<li><a href="?page=%s">首页</a></li>' % (1)
        page_html_list.append(first_page)

        if self.current_page <= 1:
            prev_page = '<li class="disabled"><a href="#">上一页</a></li>'
        else:
            prev_page = '<li><a href="?page=%s">上一页</a></li>' % (self.current_page - 1,)

        page_html_list.append(prev_page)

        for i in range(pager_start, pager_end):
            if i == self.current_page:
                temp = '<li class="active"><a href="?page=%s">%s</a></li>' % (i, i,)
            else:
                temp = '<li><a href="?page=%s">%s</a></li>' % (i, i,)
            page_html_list.append(temp)

        if self.current_page >= self.all_pager:
            next_page = '<li class="disabled"><a href="#">下一页</a></li>'
        else:
            next_page = '<li><a href="?page=%s">下一页</a></li>' % (self.current_page + 1,)
        page_html_list.append(next_page)

        last_page = '<li><a href="?page=%s">尾页</a></li>' % (self.all_pager,)
        page_html_list.append(last_page)
        # 尾部添加标签
        page_html_list.append('''
        </nav>
        </ul>
        ''')
        return ''.join(page_html_list)