# Amazon Ananlytics

amazon 类目和关键词搜索的rest API

## 需求配置
-  Python 3.5
- django 1.11
-  django-rest-framwork 3

**pip install -r requirement.txt**

## Start
```shell
python manage.py migration
python manage.py migrate
python manage.py runserver
```

## 主要配置
|主要配置|特性|
|:---:|:---:|
|utils--->exception_handler.py|处理各种exception，返回error_code|
|utils--->extra_exceptions.py|自定义exception|
|utils--->parsers.py|自定义content-type处理器|

     
# 项目结构

	.
	├── amazon
	│   ├── admin.py
	│   ├── apps.py
	│   ├──__init__.py
	│   ├── migrations
	│   │   └── __init__.py
	│   ├── models.py
	│   ├── serializer.py
	│   ├── tests.py
	│   ├── urls.py
	│   └── views.py
	├── amazon_analytics
	│   ├──__init__.py
	│   ├── settings.py
	│   ├── urls.py
	│   └── wsgi.py
	├── db.sqlite3
	├── file
	│   └── top
	│       └── origin
	├── manage.py
	├── README.md
	├── templates
	├── user
	│   ├── admin.py
	│   ├── apps.py
	│   ├── __init__.py
	│   ├── migrations
	│   │   └── __init__.py
	│   ├── models.py
	│   ├── serializer.py
	│   ├── tests.py
	│   ├── urls.py
	│   └── views.py
	└── utils
	    ├── exception_handler.py
	    ├── extra_exceptions.py
	    ├── __init__.py
	    └── parsers.py
	    

    
    
  
    