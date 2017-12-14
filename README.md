flask-skeleton
--------------

每开始一个Flask项目总是要重复做一些代码结构上的规划和写一些相同的代码，
flask-skeleton的目的是想把这些重复的事情都先统一做成脚手架，
在以后的API服务开发过程中只需clone下来就可以直接开始写业务代码。


#### flask-skeleton代码结构

    flask-skeleton
    ├── app                                                 服务代码根目录
    │   ├── blueprints                                      业务逻辑统一存放位置（以蓝图方式按业务创建目录来组织代码）
    │   │   ├── demo                                        一个demo示例（增删改查）
    │   │   │   ├── handlers.py                             视图业务处理逻辑
    │   │   │   ├── __init__.py
    │   │   │   ├── routes.py                               视图url路由逻辑
    │   │   │   └── validator_schemas.py                    参数验证schema
    │   │   └── __init__.py
    │   ├── extensions.py                                   app拓展统一存放位置
    │   ├── __init__.py
    │   ├── models                                          ORM模型
    │   │   ├── demo.py                                     一个demo示例（增删改查）
    │   │   └── __init__.py
    │   ├── periodic_tasks                                  定时任务统一存放位置
    │   │   ├── app.py                                      Celery主程序
    │   │   ├── config.py                                   Celery beat配置
    │   │   ├── readme.md
    │   │   └── tasks                                       Celery 任务统一存放位置
    │   │       ├── __init__.py
    │   │       └── print_tasks.py                          一个定时执行print的示例
    │   ├── server.py                                       flask app server（在这里统一注册蓝图）
    │   ├── settings.py                                     配置变量统一存放位置（通过.env文件可以改变默认配置）
    │   └── utils                                           工具类函数统一存放位置
    │       ├── cache.py                                    缓存工具（redis）
    │       ├── __init__.py                                 基础或不好分类的工具
    │       ├── log.py                                      日志工具
    │       ├── response.py                                 返回处理工具
    │       └── stringcase.py                               字符串风格转换（被response.py使用，不要修改或添加代码）
    ├── deploy                                              部署配置文件示例
    │   ├── gunicorn_cfg.py                                 gunicorn配置
    │   ├── logrotate                                       日志rorate配置
    │   ├── nginx.conf                                      nginx配置
    │   ├── sqls                                            数据库变更增量sql统一存放位置
    │   │   └── v0.0.0_demo.sql                             demo示例的sql（命名风格按flyway规范）
    │   └── supervisor.conf                                 supervisor配置
    ├── README.md                                           :)
    └── requirements.txt                                    依赖库列表
