# Результат тестового задания
## Как запустить локально
1. склонируйте этот репозиторий
2. установите переменные среды или запишите их в `.env` файл по файлу-примеру `.env-example.docker-compose.dev`
3. установите структуру базы данных
4. запустите внутри `Docker` при помощи `Docker-compose`

Клонирование:
```bash
git clone https://github.com/emptybutton/Test-cryptobot.git
```

Остальные комманды после установки переменных окружения внутри, `Test-cryptobot` директории:
```bash
docker compose -f docker-compose.dev.yml run cryptobot alembic upgrade head
docker compose -f docker-compose.dev.yml up
```

## Пример использования
<img src="https://github.com/emptybutton/Test-cryptobot/blob/main/assets/dialog.png?raw=true"/>

> [!NOTE]
> - Можно отслеживать множество криптовалют по разным диапазонам
> - Диапазон указывается в долларах
> - Каждые 30 секунд в Telegram приходят оповещения об изменении криптовалюты относительно указанного диапазона

## От себя
Некоторые модули задокументированы. Там описываются либо будущие решения, либо неочевидности. Оставлял как комментарии, потому что это тестовое, но по идее такие вещи в вики следует переносить.</br>

Если что wip — "work in process", но обычно так не пишу, а использую [это](https://gist.github.com/ericavonb/3c79e5035567c8ef3267).
