flask-skeleton
--------------

flask-skeleton是一个flask代码骨架，为了方便起新项目时，直接在此骨架上进行修改便可以进行开发。

需要修改的是最外层的一些脚本和配置，可能你并不需要用到，service中默认有一个ping-demo，可以将其删除。

flask-skeleton中orm使用的是peewee，环境变量配置读取使用python-decouple。

如何运行它？

0. 安装requirements.txt中的所有依赖
1. 环境变量都写在.env文件中，需要你在service目录中或者根目录新建一个名叫.env文件并将dotenv中通用的环境变量按照你的环境写入其中。

