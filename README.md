## Rubik 运维平台

[![Python3](https://img.shields.io/badge/python-3.6-green.svg?style=plastic)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-2.2-brightgreen.svg?style=plastic)](https://www.djangoproject.com/)
[![Celery](https://img.shields.io/badge/celery-4.1.0-blue.svg?style=plastic)](http://www.celeryproject.org/)
[![Paramiko](https://img.shields.io/badge/paramiko-2.4.1-green.svg?style=plastic)](http://www.paramiko.org/)


----

被打乱的魔方也能拼接成手中情趣

远离黑白屏，拥抱多彩生活

改变世界，从一点点开始

----

#### 安装部署说明：

*系统环境：pyenv
```angular2
推荐使用python3 -m venv python3，避免影响系统自带python环境

或使用pyenv
yum install openssl openssl-devel openssl-static mysql-devel -y
#安装pyenv环境
su - saas
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
vim .bashrc
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"


```

* 安装依赖包与配置更新

```
拷贝并修改config.py文件中的配置内容
cp config_example.py config.py

安装依赖
yum -y install `cat rpm_requirements.txt`
pip install -r requirements.txt

```


* 数据库创建及初始化
```
CREATE DATABASE IF NOT EXISTS rubik default charset utf8 COLLATE utf8_general_ci;
grant all privileges on rubik.* to rubik@"127.0.0.1" identified by "rubik";
flush privileges;

python3 manage.py makemigrations 

python3 manage.py migrate

# 初始化数据库
python install.py

# 配合Nginx
python manage.py collectstatic
django会把所有的static文件都复制到STATIC_ROOT文件夹下

# 启动任务
celery -A rubik worker -l info

```

* 初始化账户密码
> 账号：admin
> 密码：123456

####作者
* Godan
----