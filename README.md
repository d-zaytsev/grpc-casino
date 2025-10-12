# grpc-casino
**НЕНАСТОЯЩЕЕ (фейк)** онлайн-казино, сделанное в качестве практической части доклада по gRPC.

# Как запускать

**Для фронта:**
1. `envoy -c envoy.yaml` (прокси)
2. `npm run dev`

**Для python-сервисов:**
1. `cd src/`
2. `PYTHONPATH=. python3 service_X/server.py`

# Структура проекта

<img width="2419" height="2278" alt="grpc casino (1)" src="https://github.com/user-attachments/assets/c63e6e13-d136-404d-9f18-ba5705a46849" />

### `/protos`

Все сервисы взаимодействуют по `gRPC`. В этом каталоге находятся все `.proto` файлы для них.

### `front`

Фронт написал на `Node.js + React + Tailwind`. Для общения с сервисами по `gRPC` используется [gRPC web](https://github.com/grpc/grpc-web) и прокси [envoy](https://www.envoyproxy.io/). Прокси выступает в качестве переводчика с `gRPC-web` на `gRPC`.

```
[Browser JS] --(gRPC-Web)--> [Envoy proxy] --(gRPC)--> [Backend server]
```

### `service_balance`

Python-сервис для работы с балансом пользователей. Каждый пользователь определяется через `user_uuid`, который можно получить у сервиса `service_profile`.

### `service_profile`

Python-сервис для регистрации новых пользователей и авторизации старых.

### `service_transaction`

Python-сервис для проверки денежных транзакций пользователя (фронта). Когда проверка выполнена, обращается к `service_balance`. При проверке данных пользователя так же обращается к `service_profile`.

## Скрины работы приложения 

<img width="1000" height="600" alt="image" src="https://github.com/user-attachments/assets/2c31bfc9-5086-47bb-a131-942fb47d52eb" />
