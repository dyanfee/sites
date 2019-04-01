from django.contrib import admin
from .models import Post, Category, Tag


# admin.site.register(Post, PostAdmin)

# 用控制器注册
@admin.register(Post)
class PostAdmin (admin.ModelAdmin):
    def title_desc(self):
        return self.title
    title_desc.short_description = "题目"
    # 显示字段
    list_display = [title_desc, "create_time",

                    "modified_time", "category", "author"]
    # 过滤器 显示过滤字段
    list_filter = ["title"]
    # 分页
    list_per_page = 10
    # 查找栏 搜索字段
    # search_fields = []

    # 修改循序
    # fields = []
    # 分组修改 与fields不能同时使用
    # fieldsets = []

    actions_on_top = False
    actions_on_bottom = True


# TabularInline
class PostCre(admin.StackedInline):
    model = Post
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
  # 关联创建
    inlines = [PostCre]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag)
