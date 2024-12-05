# Upload Files
FastAPI дозволяє легко обробляти завантажені файли через HTTP-форми. Завдяки інтеграції з Python-бібліотекою python-multipart, FastAPI може приймати файли, відправлені як частина мультипарт-форми. Завдяки асинхронній природі FastAPI, можливо оптимізувати процес завантаження та обробки файлів, використовуючи асинхронні оператори та методи.
 FastAPI використовує спеціальний клас UploadFile, який надає зручний інтерфейс для роботи з завантаженими файлами. UploadFile має атрибути та методи для доступу до метаданих файлу (наприклад, ім'я файлу) та його змісту. Після завантаження файл може бути збережений на сервері. FastAPI дозволяє легко читати вміст файлу та зберігати його у файловій системі сервера або передавати до інших сервісів для обробки.

## Documentation

- [Fastapi request files](https://fastapi.tiangolo.com/tutorial/request-files/#file-parameters-with-uploadfile)

 - [Pillow](https://pillow.readthedocs.io/en/stable/handbook/tutorial.html)
