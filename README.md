## courses

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Описание

Проект был разработан для действий с курсами (CRUD/выбор/прохождение)

## Зависимости:

    - Python - основной язык программирования
    - Django - фреймворк для написания backend части
    - Celery - библиотека для управления очередями

## Окружение

1. Развёртывание производится на операционной системе Manjaro
1. Требуется предустановленный интерпретатор Python версии 3.10.5, docker, docker-compose

## Использование

Для запуска нужно установить библиотеки invoke и rich для удобного
взаимодействия

```bash
pip install invoke rich
```

После установки библиотек:

```bash
inv docker.run
```
