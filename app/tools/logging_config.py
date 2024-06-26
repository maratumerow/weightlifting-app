from logging.config import dictConfig

# Словарь с конфигурацией логирования
logging_config = {
    "version": 1,  # Версия конфигурации
    "disable_existing_loggers": False,  # Не отключать существующие логеры
    "formatters": {  # Определение форматеров
        "default": {  # Форматер по умолчанию
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            # Формат сообщения лога:
            # %(asctime)s - Время записи сообщения
            # %(name)s - Имя логера
            # %(levelname)s - Уровень важности сообщения
            # %(message)s - Само сообщение
        },
    },
    "handlers": {  # Определение обработчиков
        "console": {  # Обработчик для вывода в консоль
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {  # Корневой логер
        "level": "INFO",  # Уровень логирования
        "handlers": ["console"],  # Обработчики, которые будут использоваться
    },
    "loggers": {  # Дополнительные логеры для uvicorn
        "uvicorn": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,  # Не передавать сообщения корневому логеру
        },
        "uvicorn.error": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
        "uvicorn.access": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}


def setup_logging():
    dictConfig(logging_config)  # Применение конфигурации логирования
