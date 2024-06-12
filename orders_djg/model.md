1.2 create

通过模型类.objects.create()保存。

>>> HeroInfo.objects.create(
    hname='沙悟净',
    hgender=0,
    hbook=book
)
<HeroInfo: 沙悟净>
1
2
3
4
5
6
2. 查询

2.1 基本查询
get :查询单一结果，如果不存在会抛出模型类.DoesNotExist异常。
all :查询多个结果。
count :查询结果数量。

>>> BookInfo.objects.all()
<QuerySet [<BookInfo: 射雕英雄传>, <BookInfo: 天龙八部>, <BookInfo: 笑傲江湖>, <BookInfo: 雪山飞狐>, <BookInfo: 西游记>]>
>>> book = BookInfo.objects.get(btitle='西游记')
>>> book.id
5

>>> BookInfo.objects.get(id=3)
<BookInfo: 笑傲江湖>
>>> BookInfo.objects.get(pk=3)
<BookInfo: 雪山飞狐>
>>> BookInfo.objects.get(id=100)
Traceback (most recent call last):
  File "<console>", line 1, in <module>
  File "/Users/delron/.virtualenv/dj/lib/python3.6/site-packages/django/db/models/manager.py", line 85, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "/Users/delron/.virtualenv/dj/lib/python3.6/site-packages/django/db/models/query.py", line 380, in get
    self.model._meta.object_name
db.models.DoesNotExist: BookInfo matching query does not exist.

>>> BookInfo.objects.count()
6

2.2 过滤查询

实现SQL中的where功能，包括

filter 过滤出多个结果
exclude 排除掉符合条件剩下的结果
get 过滤单一结果
对于过滤条件的使用，上述三个方法相同，故仅以filter进行讲解。

过滤条件的表达语法如下：

属性名称__比较运算符=值
# 属性名称和比较运算符间使用两个下划线，所以属性名不能包括多个下划线
1
2
1）相等

exact：表示判等。

例：查询编号为3的图书。

BookInfo.objects.filter(id__exact=3)
可简写为：
BookInfo.objects.filter(id=3)
1
2
3
2）模糊查询

contains：是否包含。

说明：如果要包含%无需转义，直接写即可。

例：查询书名包含’游’的图书。

BookInfo.objects.filter(btitle__contains='游')
1
startswith、endswith：以指定值开头或结尾。
例：查询书名以’记’结尾的图书

BookInfo.objects.filter(btitle__endswith='记')
1
以上运算符都区分大小写，在这些运算符前加上i表示不区分大小写，如iexact、icontains、istartswith、iendswith.

3） 空查询

isnull：是否为null。

例：查询书名不为空的图书。

BookInfo.objects.filter(btitle__isnull=False)
1
4） 范围查询

in：是否包含在范围内。

例：查询编号为1或3或5的图书

BookInfo.objects.filter(id__in=[1, 3, 5])
1
5）比较查询

gt ：大于 (greater then)
gte ：大于等于 (greater then equal)
lt ：小于 (less then)
lte ：小于等于 (less then equal)
例：查询编号大于3的图书

BookInfo.objects.filter(id__gt=3)
1
不等于的运算符，使用exclude()过滤器。

例：查询编号不等于3的图书

BookInfo.objects.exclude(id=3)
1
6）日期查询

year、month、day、week_day、hour、minute、second：对日期时间类型的属性进行运算。

例：查询1980年发表的图书。

BookInfo.objects.filter(bpub_date__year=1980)
1
例：查询1980年1月1日后发表的图书。

BookInfo.objects.filter(bpub_date__gt=date(1990, 1, 1))
1
F对象

之前的查询都是对象的属性与常量值比较，两个属性怎么比较呢？ 答：使用F对象，被定义在django.db.models中。

语法如下：

F(属性名)
1
例：查询阅读量大于等于评论量的图书。

from django.db.models import F
BookInfo.objects.filter(bread__gte=F('bcomment'))
1
2
可以在F对象上使用算数运算。

例：查询阅读量大于2倍评论量的图书。

BookInfo.objects.filter(bread__gt=F('bcomment') * 2)
1
Q对象

多个过滤器逐个调用表示逻辑与关系，同sql语句中where部分的and关键字。

例：查询阅读量大于20，并且编号小于3的图书。

BookInfo.objects.filter(bread__gt=20,id__lt=3)
或
BookInfo.objects.filter(bread__gt=20).filter(id__lt=3)
1
2
3
如果需要实现逻辑或or的查询，需要使用Q()对象结合|运算符，Q对象被义在django.db.models中。

语法如下：

Q(属性名__运算符=值)
1
例：查询阅读量大于20的图书，改写为Q对象如下。

from django.db.models import Q

BookInfo.objects.filter(Q(bread__gt=20))
1
2
3
Q对象可以使用&、|连接，&表示逻辑与，|表示逻辑或。

例：查询阅读量大于20，或编号小于3的图书，只能使用Q对象实现

BookInfo.objects.filter(Q(bread__gt=20) | Q(pk__lt=3))
1
Q对象前可以使用~操作符，表示非not。

例：查询编号不等于3的图书。

BookInfo.objects.filter(~Q(pk=3))
1
聚合函数

使用aggregate()过滤器调用聚合函数。聚合函数包括：Avg(平均)，Count(数量)，Max(最大)，Min(最小)，Sum(求和)，被定义在django.db.models中。

例：查询图书的总阅读量。

from django.db.models import Sum
BookInfo.objects.aggregate(Sum('bread'))
1
2
注意aggregate的返回值是一个字典类型，格式如下：

  {'属性名__聚合类小写':值}
  如:{'bread__sum':3}
1
2
使用count时一般不使用aggregate()过滤器。

例：查询图书总数。

BookInfo.objects.count()
1
注意count函数的返回值是一个数字。

2.3 排序

使用order_by对结果进行排序

BookInfo.objects.all().order_by('bread')  # 升序
BookInfo.objects.all().order_by('-bread')  # 降序
1
2
2.4 关联查询

由一到多的访问语法：

一对应的模型类对象.多对应的模型类名小写_set 例：

b = BookInfo.objects.get(id=1)
b.heroinfo_set.all()
1
2
由多到一的访问语法:

多对应的模型类对象.多对应的模型类中的关系类属性名 例：

h = HeroInfo.objects.get(id=1)
h.hbook
1
2
访问一对应的模型类关联对象的id语法:

多对应的模型类对象.关联类属性_id

例：

h = HeroInfo.objects.get(id=1)
h.book_id
1
2
关联过滤查询

由多模型类条件查询一模型类数据:

语法如下：

关联模型类名小写__属性名__条件运算符=值
注意：如果没有"__运算符"部分，表示等于。

例：查询图书，要求图书英雄为"孙悟空"

BookInfo.objects.filter(heroinfo__hname='孙悟空')
1
查询图书，要求图书中英雄的描述包含"八"

BookInfo.objects.filter(heroinfo__hcomment__contains='八')
1
由一模型类条件查询多模型类数据:
语法如下：

一模型类关联属性名__一模型类属性名__条件运算符=值
1
注意：如果没有"__运算符"部分，表示等于。

例：查询书名为“天龙八部”的所有英雄。

HeroInfo.objects.filter(hbook__btitle='天龙八部')
1
查询图书阅读量大于30的所有英雄

HeroInfo.objects.filter(hbook__bread__gt=30)
1
3. 修改

修改更新有两种方法

3.1 save

修改模型类对象的属性，然后执行save()方法

hero = HeroInfo.objects.get(hname='猪八戒')
hero.hname = '猪悟能'
hero.save()
1
2
3
3.2 update
使用模型类.objects.filter().update()，会返回受影响的行数

HeroInfo.objects.filter(hname='沙悟净').update(hname='沙僧')
1
4. 删除
删除有两种方法

4.1 模型类对象delete

hero = HeroInfo.objects.get(id=13)
hero.delete()
1
2
4.2 模型类.objects.filter().delete()

HeroInfo.objects.filter(id=14).delete()
1



五、查询集 QuerySet
1. 概念

Django的ORM中存在查询集的概念。

查询集，也称查询结果集、QuerySet，表示从数据库中获取的对象集合。

当调用如下过滤器方法时，Django会返回查询集（而不是简单的列表）：

all()：返回所有数据。
filter()：返回满足条件的数据。
exclude()：返回满足条件之外的数据。
order_by()：对结果进行排序。
对查询集可以再次调用过滤器进行过滤，如

BookInfo.objects.filter(bread__gt=30).order_by('bpub_date')
1
也就意味着查询集可以含有零个、一个或多个过滤器。过滤器基于所给的参数限制查询的结果。

从SQL的角度讲，查询集与select语句等价，过滤器像where、limit、order by子句。

判断某一个查询集中是否有数据：

exists()：判断查询集中是否有数据，如果有则返回True，没有则返回False。
2. 两大特性

2.1 惰性执行
创建查询集不会访问数据库，直到调用数据时，才会访问数据库，调用数据的情况包括迭代、序列化、与if合用

例如，当执行如下语句时，并未进行数据库查询，只是创建了一个查询集qs

qs = BookInfo.objects.all()
1
继续执行遍历迭代操作后，才真正的进行了数据库的查询

for book in qs:
    print(book.btitle)
1
2
2.2 缓存
使用同一个查询集，第一次使用时会发生数据库的查询，然后Django会把结果缓存下来，再次使用这个查询集时会使用缓存的数据，减少了数据库的查询次数。

实例1：如下是两个查询集，无法重用缓存，每次查询都会与数据库进行一次交互，增加了数据库的负载。

from booktest.models import BookInfo
[book.id for book in BookInfo.objects.all()]
[book.id for book in BookInfo.objects.all()]
1
2
3
实例二：经过存储后，可以重用查询集，第二次使用缓存中的数据。

qs=BookInfo.objects.all()
[book.id for book in qs]
[book.id for book in qs]
1
2
3
3. 限制查询集
可以对查询集进行取下标或切片操作，等同于sql中的limit和offset子句。
        注意：不支持负数索引。

对查询集进行切片后返回一个新的查询集，不会立即执行查询。

如果获取一个对象，直接使用[0]，等同于[0:1].get()，但是如果没有数据，[0]引发IndexError异常，[0:1].get()如果没有数据引发DoesNotExist异常。

示例：获取第1、2项，运行查看。

qs = BookInfo.objects.all()[0:2]
1

