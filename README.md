# Сборка изображений в формат TIFF

Этот проект предлагает два способа его использования:

## 1. Запуск в качестве Python-скрипта

Чтобы запустить скрипт в качестве Python-скрипта, выполните следующие шаги:

1. Создайте виртуальное окружение:
    ```
    python -m venv venv
    ```
2. Установите необходимые зависимости:
    ```
    pip install -r requirements.txt
    ```
3. Запустите скрипт:
    ```
    python tiff_convert.py
    ```

## 2. Запуск в качестве FastAPI приложения

Чтобы запустить приложение в качестве FastAPI приложения, вам нужно установить Docker и Docker Compose. Выполните следующие шаги:

1. Соберите и запустите Docker-контейнер:
    ```
    sudo docker-compose up
    ```
2. Приложение будет доступно по адресу `http://0.0.0.0:8000/`.
3. Документация API находится по адресу `http://0.0.0.0:8000/docs`.

### Пример HTTP POST-запроса

Чтобы сделать HTTP POST-запрос по адресу `http://0.0.0.0:8000/` с JSON-данными, вы можете использовать следующий пример для bash:

```curl -X POST -H "Content-Type: application/json" -d '{"dir_names": ["<dir name>"], "root_dir": "<root_dir(directory where needed directory placed)>"}' http://0.0.0.0:8000/ --output path/to/file/name.zip```

# Collect images to TIFF

This project provides two ways to use it:

## 1. Running as a Python script

To run the script as a Python script, follow these steps:

1. Create a virtual environment:
    ```
    python -m venv venv
    ```
2. Install the required dependencies:
    ```
    pip install -r requirements.txt
    ```
3. Run the script:
    ```
    python tiff_convert.py
    ```

## 2. Running as a FastAPI app

To run the app as a FastAPI app, you need Docker and Docker Compose installed. Follow these steps:

1. Build and run the Docker container:
    ```
    sudo docker-compose up
    ```
2. The app will be available at `http://0.0.0.0:8000/`.
3. The API documentation can be found at `http://0.0.0.0:8000/docs`.

### Example of HTTP POST request

To make an HTTP POST request to `http://0.0.0.0:8000/` with JSON data, you can use the following example with bash:

```curl -X POST -H "Content-Type: application/json" -d '{"dir_names": ["<dir name>"], "root_dir": "<root_dir(directory where needed directory placed)>"}' http://0.0.0.0:8000/ --output path/to/file/name.zip```