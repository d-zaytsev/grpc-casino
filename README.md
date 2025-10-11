# grpc-casino
Fake online web casino for gRPC talk

## Структура проекта

### `/protos`

Все сервисы взаимодействуют по `gRPC`. В этом каталоге находятся все `.proto` файлы для них.

### `front`

Фронт написал на `Node.js/React/Tailwind`. Для общения с сервисами по `gRPC` используется [gRPC web](https://github.com/grpc/grpc-web) и прокси [envoy](https://www.envoyproxy.io/). Прокси выступает в качестве переводчика с `gRPC-web` на `gRPC`, так как обычный `gRPC` слишком низкоуровневый для браузеров.

```
[Browser JS] --(gRPC-Web)--> [Envoy proxy] --(gRPC)--> [Backend server]
```

### `service_balance`

Python-сервис для работы с балансом пользователей. Каждый пользователь определяется через уникальный `user_id`, который можно получить у сервиса `service_profile`.

### `service_profile`

Python-сервис для регистрации новых пользователей и авторизации старых.