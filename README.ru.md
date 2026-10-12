# OPSEC Validation Lab

Установите Python 3.12+ и точный выпущенный wheel контракта через bootstrap. Первоначальная установка требует сеть; проверка выполняется локально. Выходные имена не должны существовать. Первый пример возвращает 0; невыполненный live-пример записывает результат и возвращает 2. Код 1 означает несовпадение утверждения, 3 — повреждённый вход или недоступный выход. Коды относятся к утверждениям лаборатории, а не безопасности инфраструктуры.

```bash
python -m pip install -r requirements-bootstrap.txt
python -m pip install .
opsec-lab check-manifest examples/suite.synthetic.json
opsec-lab verify examples/suite.synthetic.json --observed-at 2026-10-12T00:00:00Z --output result.json
opsec-lab verify examples/live-unexecuted.json --observed-at 2026-10-12T00:00:00Z --output live-result.json
```

[Documentation](docs/ru/index.md)

Alpha 0.1.0a1. На Linux/macOS прошли 19 тестовых методов; на Windows — 18 с пропуском FIFO-теста. На трёх ОС с Python 3.13 проверены 11 пар RU/EN документов и чистая установка wheel. Живая среда не проверялась.
