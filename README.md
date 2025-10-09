# grpc-casino
Fake online web casino for gRPC talk

## Структура проекта

### `protos`

Все сервисы взаимодействуют по `gRPC`. В этом каталоге находятся все `.proto` файлы для них.

### `front`

Фронт на `Node.js/React/Tailwind`.

### `service_balance`

Python-сервис для работы с балансом пользователей. Каждый пользователь определяется через уникальный `user_id`, который можно получить у сервиса `service_profile`.

### `service_profile`

Python-сервис для регистрации новых пользователей и авторизации старых.