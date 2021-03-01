# WebStack

WebStack build by Django.

## Intro

这是一个开源的网址导航网站项目，具备完整的前后台，你可以拿来制作自己的网址导航，也可以做与导航无关的网站。如果你有任何疑问，可以通过个人网站 www.hujiangtao.cn 中的联系方式找到我，欢迎与我交流分享。

## Usage

1. clone this project

```bash
git clone https://github.com/hustjiangtao/webstack-django.git webstack
cd webstack
```

2. install virtual env & requirements

```bash
cd webstack
pyenv local 3.6.5
python -m venv .venv
.venv/bin/pip install -r requirements.txt
```

3. sql migrate

```bash
make migrate
```

4. test & run

```bash
make test
make dev (for development env)
make run (for production ready)
```

项目启动成功后，在浏览器中访问：
- 展示地址: http://127.0.0.1:8000/
- 后台地址: http://127.0.0.1:8000/admin/

5. deploy

- docker

```bash
cd webstack
docker-compose up -d
```

- supervisor

```bash
supervisorctl start webstack
```

## THX

- 前端设计: [WebStackPage](https://github.com/WebStackPage/WebStackPage.github.io)
- 后台框架: [django](https://www.djangoproject.com/)
- 项目架构：[木先生](https://www.hujiangtao.cn/)

## License

AGPL-3.0

> 注：本站开源的目的是大家能够在本站的基础之上有所启发，做出更多新的东西。并不是让大家照搬所有代码。 如果你使用这个开源项目，请注明本项目开源地址。
