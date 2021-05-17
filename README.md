#### 创建第一个项目
```django-admin.py startproject HelloWorld ``` 

#### 创建一个APP
```django-admin.py startapp TestModel```

```
python3 manage.py migrate   # 创建表结构

python3 manage.py makemigrations tools  # 让 Django 知道我们在我们的模型有一些变更
python3 manage.py migrate tools   # 创建表结构
```

#### 启动项目
```python3 manage.py runserver 0.0.0.0:8000```

#### 路由数据
```path(route, view, kwargs=None, name=None)```
1. route: 字符串，表示 URL 规则，与之匹配的 URL 会执行对应的第二个参数 view。
2. view: 用于执行与正则表达式匹配的 URL 请求。
3. kwargs: 视图使用的字典类型的参数。
4. name: 用来反向获取 URL。

#### 数据库配置
创建数据库
```
create database qa_open default charset=utf8; # 防止编码问题，指定为 utf8
```

```
DATABASES = { 
    'default': 
    { 
        'ENGINE': 'django.db.backends.mysql',    # 数据库引擎
        'NAME': 'runoob', # 数据库名称
        'HOST': '127.0.0.1', # 数据库地址，本机 ip 地址 127.0.0.1 
        'PORT': 3306, # 端口 
        'USER': 'root',  # 数据库用户名
        'PASSWORD': '123456', # 数据库密码
    }  
}
```

#### 时区
```
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'
```

#### models对应SQL语句
https://segmentfault.com/a/1190000016053857

