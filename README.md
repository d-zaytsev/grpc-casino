# grpc-casino
Fake online web casino for gRPC talk

## Структура проекта

### `protos`

Все сервисы взаимодействуют по `gRPC`. В этом каталоге находятся все `.proto` файлы для них.

### `front`

Поднять сервис:
```bash
cd front \
npm run dev
```

Фронт на `Node.js/React/Tailwind` 

### `service_balance`

Python сервис для работы с балансом пользователей.