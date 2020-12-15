开发框架2.0使用说明：https://docs.bk.tencent.com/blueapps/USAGE.html


```
$ npm i bk-magic-vue --save
```

数据库设置

CREATE DATABASE `{APP_CODE}` default charset utf8 COLLATE utf8_general_ci;

如果{APP_CODE}中包含连接符(-)，需要使用反引号( ` )转译，否则会报错


Host设置

127.0.0.1 appdev.paas.exam.bktencent.com

python manage.py runserver appdev.paas.exam.bktencent.com:8000


开发者中心 -》应用创建 -》
git 配置 https://github.com:zhanghe06/bk_test.git，使用https协议，用户名和密码随便填


代码配置

config/__init__.py
APP_CODE
SECRET_KEY
BK_URL

config/dev.py
数据库配置

