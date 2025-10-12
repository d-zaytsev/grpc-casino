# grpc-casino
Fake online web casino for gRPC talk

## Как запускать

**Для фронта:**
1. `envoy -c envoy.yaml` (прокси)
2. `npm run dev`

**Для python-сервисов:**
1. `cd src/`
2. `PYTHONPATH=. python3 service_X/server.py`

## Структура проекта

<img width="2419" height="2203" alt="grpc casino" src="https://github.com/user-attachments/assets/22695c05-7d25-45e3-b116-a366c310dfdf" />

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

### `service_transaction`

Python-сервер для проверки денежных транзакций пользователя (фронта). Когда проверка выполнена, обращается к `service_balance`.
