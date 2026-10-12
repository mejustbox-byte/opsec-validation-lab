# Манифест lab-1.0

Манифест содержит ровно schema_version, suite_id и cases. Сценарий содержит id, kind, report, sha256, producer, expected и provenance. Kind — synthetic или live. Имя отчёта и хеш либо заполнены вместе, либо оба пусты; это позволяет честно представить невыполненный live-сценарий.

Producer содержит name, version и ruleset. Expected — непустой список check_id, asset_id и status с уникальными парами. Сравниваются полные карты фактических и ожидаемых результатов: отсутствие и лишний результат дают fail LAB-001. Ожидаемый not_tested может совпасть: утверждение проходит, но исходный отчёт по-прежнему заявляет непроверенный контроль. Успех лаборатории не равен успеху аудитора.

Provenance содержит platform, platform_version, execution_id и sanitization_reviewed. Это предоставленные заявления, а не независимо собранные факты. Пустая платформа даёт fail LAB-002 при наличии свидетельств. Live без ID выполнения оставляет LAB-003 not_tested. False-флаг проверки приватности оставляет LAB-004 not_tested. Подписи, время и журнал исполнения манифест не проверяет.

[Index](index.md) · [Other language](../en/manifest.md)
