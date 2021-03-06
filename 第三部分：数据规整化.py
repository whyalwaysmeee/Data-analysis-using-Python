import pandas as pd
from pandas import Series, DataFrame
import numpy as np
import re
import json

#合并数据集
df1 = DataFrame({'key':['b','b','a','c','a','a','b'], 'data1':range(7)})
df2 = DataFrame({'key':['a','b','d'], 'data2':range(3)})
df3 = DataFrame({'lkey':['b','b','a','c','a','a','b'], 'data1':range(7)})
df4 = DataFrame({'rkey':['a','b','d'], 'data2':range(3)})
df5 = DataFrame({'key':['a','b','a','b','d'],'data2':range(5)})
df6 = DataFrame({'key':['b','b','a','c','a','b'], 'data1':range(6)})
#数据库风格的DataFrame合并
#多对一的合并。df1中有多个被标记为a和b的行，df2中每个key仅对应一行
#直接合并，没有指定哪个列连接的情况下，将会用重叠的列名当做键（默认交集）
pd.merge(df1,df2)
#制定列名
pd.merge(df1,df2, on = 'key')
#若两对象的列名不同，可分别指定
pd.merge(df3,df4, left_on = 'lkey',right_on = 'rkey')
#若要将列名的并集合并
pd.merge(df1,df2,how = 'outer')


#多对多的合并
left = DataFrame({'key1':['foo','foo','bar'],
                  'key2':['one','two','one'],
                  'lval':[1,2,3]})
right = DataFrame({'key1':['foo','foo','bar','bar'],
                  'key2':['one','one','one','two'],
                  'rval':[4,5,6,7]})
#outer表示将搜有的列名key都要包含进来，在这里最后生成的结果应该是一个12行的DataFrame
#理由：df5中2个b，df6中3个b，产生6行数据，df5、df6中各2个a，产生4行数据，df5中d、df6中c各产生1行数据
pd.merge(df5,df6, on = 'key', how = 'outer')
#根据多个键进行合并，传入一个由列名组成的列表
pd.merge(left, right, on = ['key1','key2'], how = 'outer')
#根据单个键合并，会生成key2_x和key2_y两个新列名，分别代表两个对象中的key2，因为两个对象中都有key2
pd.merge(left,right, on = 'key1')
#对新生成的列名进行命名
pd.merge(left,right, on = 'key1', suffixes = ('_left','_right'))


#索引的合并
left1 = DataFrame({'key':['a','b','a','a','b','c'],
                   'value' : range(6)})
right1 = DataFrame({'group_val':[3.5,7]},index = ['a','b'])
#right_index表示右侧（第二个）对象的索引被用作连接键，默认取交集
pd.merge(left1, right1, left_on = 'key',right_index = True)
#若要取并集
pd.merge(left1, right1, left_on = 'key',right_index = True, how = 'outer')
#join方法
left1.join(right1, how = 'outer')


#连接
#该种操作对DataFrame对象同样适用
s1 = Series([0,1],index = ['a','b'])
s2 = Series([2,3,4],index = ['c','d','e'])
s3 = Series([5,6],index = ['f','g'])
#使用concat，结果仍是一个Series（默认并集）
pd.concat([s1,s2])
#两个以上对象时，传入参数axis = 1会生成DataFrame（若不传入sort参数会出现警告）,结果为每个Series的数据占据一列，其余为空值
pd.concat([s1,s2,s3],axis = 1,sort = True)
#若要得到交集
pd.concat([s1,s3],axis = 1,join = 'inner')
#指定索引
pd.concat([s1,s3],axis = 1,join_axes = [['a','f']])
#层次化索引
pd.concat([s1,s2,s3],keys = ['one','two','three'])
#让keys成为列头
pd.concat([s1,s2,s3],keys = ['one','two','three'],axis = 1)

#合并重叠数据
a = Series([np.nan,2.5,np.nan,3.5,4.5,np.nan],index = ['f','e','d','c','b','a'])
b = Series(np.arange(len(a)),dtype=np.float64,index = ['f','e','d','c','b','a'])
#b会将a中的空值填充成自己的值，对DataFrame也同样适用
b.combine_first(a)

#重塑和轴向旋转
data = DataFrame(np.arange(6).reshape((2,3)),
                 index = pd.Index(['Ohio','Colorado'],name = 'state'),
                 columns = pd.Index(['one','two','three'],name = 'number'))
#重塑层次化索引
#将列旋转为行，结果是一个Series
data.stack()
#将行旋转为列，结果是一个DataFrame。默认情况是旋转最内层，传入分层级别的编号或名称可对其他级别进行操作
result = data.stack()
result.unstack()
result.unstack(0)
result.unstack('state')
#若不是有些值在索引中无法找到，那么会引入缺失值
data2 = pd.concat([s1,s2],keys = ['one','two'])
data2.unstack()
#stack会默认滤除缺失值
data2.unstack().stack()


#将长格式旋转为宽格式
data0 = pd.read_excel("D:/cs/P4/time.xlsx")
#不同item值分别形成一列，并用作列名，时间值作为索引
pivoted = data0.pivot('data','item','value1')
pivoted.head()
#新增一个需要重塑的列value2
data0['value2'] = np.random.randn(len(data0))
#重塑时忽略最后一个参数
pivoted1 = data0.pivot('data','item')
#pivot其实是一个快捷方式。原方法如下
unstacked = data0.set_index(['date','item']).unstack('item')

#数据转换
#移除重复数据
data1 = DataFrame({'k1':['one']*3 + ['two']*4,'k2':[1,1,2,3,3,4,4]})
#检查数据是否重复
data1.duplicated()
#移除重复数据，默认保留出现的第一个值。如果传入参数则保留最后一个
data1.drop_duplicates()
data1.drop_duplicates(['k1','k2'],take_last = True)
#只根据某列进行重复移除
data1.drop_duplicates(['k1'])

#数据转换
data2 = DataFrame({'food':['bacon','pulled pork','bacon','Pastrami','CORNED BEEF','Bacon','pastrami','honey ham','nove lox'],'ounces':[4,3,11,6,7.5,8,3,5,6]})
meat_to_animal = {'bacon':'pig','pulled pork':'pig','pastrami':'pig','corned beef':'cow','honey ham':'pig','nova lox':'salmon'}
#利用函数将大写字母转为小写
data2 = data2['food'].map(str.lower)
#利用映射进行转换
data2['animal'] = data2['food'].map(str.lower).map(meat_to_animal)


#重命名轴索引
#upper：转大写；lower：转小写；title：
data = DataFrame(np.arange(12).reshape((3,4)),index = ['Ohio','Colorado','New York'],columns=['one','two','three','four'])
#用map转换
data.index = data.index.map(str.upper)
#用rename转换
data.rename(index=str.title,columns = str.upper)
#改变索引名
data.rename(index={'Ohio':'Indiana'},columns = {'THREE':'peekaboo'})

#离散化和面元划分
ages = [20,22,25,27,31,23,37,31,61,45,41,32]
bins = [18,25,35,60,100]
data = np.random.randn(20)
data0 = np.random.randn(1000)
#划分数据（默认左开右闭），传入参数为面元边界
cats = pd.cut(ages,bins)
#设置为左闭右开
cats = pd.cut(ages,bins,right = False)
#对每个阶层计数
pd.value_counts(cats)
#给每个组设置一个标签
cats = pd.cut(ages,bins,labels=['a','b','c','d'])
#划分数据，传入参数为面元数量，会自动根据最大值和最小值计算等长面元
cats = pd.cut(data,4,precision = 2)
#qcut会默认根据四分位数来进行切割
cats = pd.qcut(data0,4)
#也可以设置自定义的分位数
pd.qcut(data,[0,0.1,0.5,0.9,1.])

#检测和过滤异常值
data = DataFrame(np.random.randn(1000,4))
#分析数据，包括平均值、最大值、四分位数等
data.describe()
#找出每列中绝对值超过3的值
col = data[3]
col[np.abs(col)>3]
#找出所有含有“绝对值超过3”的行
data[(np.abs(data)>3).any(1)]
#将值限制在-3到3之间
data[np.abs(data)>3] = np.sign(data) * 3

#排列和随机采样
df = DataFrame(np.arange(5*4).reshape(5,4))
sampler = np.random.permutation(5)
#将df的行顺序按sampler的顺序重排
df.take(sampler)
#取前3行
df.take(sampler)[:3]
#得到一组随机整数,范围0——4，长度10
sampler0 = np.random.randint(0,5,size=10)

#哑变量
df = DataFrame({'key':['b','b','a','c','a','b'],'data1':range(6)})
#得到哑矩阵
pd.get_dummies(df['key'])
#给每个列名加前缀
dummies = pd.get_dummies(df['key'],prefix='key')
#将data1列合并
df[['data1']].join(dummies)

#字符串操作
#字符串对象方法
val = 'a,b, guido'
#以逗号为分隔拆分，结果为一个列表
val.split(',')
#若需要去除空格
pieces = [x.strip() for x in val.split(',')]
#用"::"进行连接
'::'.join(pieces)
#检测字符串
'guido' in val
#定位字符串(首个出现)，rfind返回最后一个
val.index(',')
#如果找不到，index返回异常，find返回-1
val.find(':')
#返回出现次数
val.count(',')
#替换
val.replace(',','::')

#正则表达式
text = "foo bar\t baz \tqux"
text0 = """Dave dave@google.com
Steve steve@gmail.com
Rob rob@gmail.com
Ryan ryan@yahoo.com
"""
#拆分字符串，分隔符为数量不一的空白符(\s+)
re.split('\s+',text)
#获取一个可重用的regex对象然后再拆分
regex = re.compile('\s+')
regex.split(text)
#返回所有匹配项，即空白符
regex.findall(text)
#获取text0中电子邮件地址，IGNORECASE使正则表达式对大小写不敏感
pattern = r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}'
regex = re.compile(pattern,flags=re.IGNORECASE)
regex.findall(text0)
#替换
regex.sub('REDACTED',text0)
#添加名称
regex.sub(r'Usename: \1,Domain: \2,Suffi: \3',text0)
#将地址分为3个部分：用户名、域名及后缀
pattern0 = r'([A-Z0-9._%+-]+)@([A-Z0-9.-]+)\.([A-Z]{2,4})'
regex = re.compile(pattern,flags=re.IGNORECASE)
regex.findall(text0)
#由这种正则表达式产生的匹配项对象，可通过groups方法返回一个由模式各段组成的元组
m = regex.match('12345@ctgod.net')
m.groups()


#示例项目：USDA食品数据库
#该json文件在引入后是一个由字典组成的列表，每一行都是一个字典，其中'portion'和'nutrients'两个key又分别代表一个字典
db = json.load(open('foods-2011-10-03.json'))
#查看记录条数
len(db)
#查看所有key，该json文件本身没有key，因为它本质是一个列表，是它的每一条记录（即一个字典）含有key
db[0].keys()
#查看第一条记录的第一种'nutrients'
db[0]['nutrients'][0]
#抽取第一条记录的'nutrients’
nutrients = DataFrame(db[0]['nutrients'])
#抽取部分字段
info_keys = ['description','group','id','manufacturer']
info = DataFrame(db,columns=info_keys)
#查看食物类别分布情况（计数）
pd.value_counts(info.group)
#对营养数据进行分析
nutrients0 = []
for i in db:
    fnuts = DataFrame(i['nutrients'])
    fnuts['id'] = i['id']
    nutrients0.append(fnuts)
nutrients0 = pd.concat(nutrients0,ignore_index=True)
#查看重复项数量
nutrients0.duplicated().sum()
#去掉重复项
nutrients0.drop_duplicates()
#现在要对info和nutrients0进行整合，因为两者都含有'description'和'group'，所以要区分开来
col_mapping = {'descrption':'food','group':'fgroup'}
col_mapping0 = {'description':'nutrients','group':'nutgroup'}
info = info.rename(columns = col_mapping,copy = False)
nutrients0 = nutrients0.rename(columns = col_mapping0,copy = False)
ndata = pd.merge(nutrients0,info,on='id',how='outer')
#查看nadata的第2000项
ndata.ix[2000]
#求各营养成分最为丰富的食物是什么，这里只列出含'Amino Acids'类营养最丰富的食物
by_nutrients = ndata.groupby(['nutgroup','nutrient'])
get_maximum = lambda x:x.xs(x.value.idxmax())
get_minimum = lambda x:x.xs(x.value.idxmin())
max_foods = by_nutrients.apply(get_maximum)[['value','food']]
max_foods.ix['Amino Acids']['food']







































