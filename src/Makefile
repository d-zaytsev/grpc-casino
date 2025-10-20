PID_DIR := .pids
ENVOY_PID := $(PID_DIR)/envoy.pid
TRANSACTIONS_PID := $(PID_DIR)/transactions.pid
PROFILE_PID := $(PID_DIR)/profile.pid
BALANCE_PID := $(PID_DIR)/balance.pid
GAME_PID := $(PID_DIR)/game.pid
FRONT_PID := $(PID_DIR)/front.pid

VENV := .venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip

ENVOY_CMD := envoy -c service_front/envoy.yaml
TRANSACTIONS_CMD := PYTHONPATH=. $(PYTHON) service_transaction/server.py
PROFILE_CMD := PYTHONPATH=. $(PYTHON) service_profile/server.py
BALANCE_CMD := PYTHONPATH=. $(PYTHON) service_balance/server.py
GAME_CMD := cd service_game/ && go run server/server.go
FRONT_CMD := cd service_front/ && npm run dev

.PHONY: all start stop restart clean status logs help setup install install-go install-node

all: help

setup: $(VENV) install npm

$(VENV):
	@echo "Создание виртуального окружения Python..."
	python3 -m venv $(VENV)
	@echo "Виртуальное окружение создано"

npm:
	@echo "Установка Node.js зависимостей..."
	npm install service_front/
	@echo "Node.js зависимости установлены"

install: $(VENV)
	@echo "Установка Python зависимостей..."
	$(PIP) install grpcio grpcio-tools protobuf
	@echo "Python зависимости установлены"

$(PID_DIR):
	@mkdir -p $(PID_DIR)

start: $(PID_DIR)
	@echo "Запуск всех сервисов..."
	@$(MAKE) start-envoy
	@$(MAKE) start-transactions
	@$(MAKE) start-profile
	@$(MAKE) start-balance
	@$(MAKE) start-game
	@$(MAKE) start-front
	@echo "Все сервисы запущены!"
	@$(MAKE) status

stop:
	@echo "Остановка всех сервисов..."
	@-$(MAKE) stop-envoy
	@-$(MAKE) stop-transactions
	@-$(MAKE) stop-profile
	@-$(MAKE) stop-balance
	@-$(MAKE) stop-game
	@-$(MAKE) stop-front
	@echo "Все сервисы остановлены"

restart: stop start

start-envoy: $(PID_DIR)
	@if [ -f $(ENVOY_PID) ] && kill -0 `cat $(ENVOY_PID)` 2>/dev/null; then \
		echo "Envoy уже запущен (PID: `cat $(ENVOY_PID)`)"; \
	else \
		echo "Запуск Envoy..."; \
		$(ENVOY_CMD) & \
		echo $$! > $(ENVOY_PID); \
		echo "Envoy запущен (PID: $$!)"; \
	fi

start-transactions: $(PID_DIR)
	@if [ -f $(TRANSACTIONS_PID) ] && kill -0 `cat $(TRANSACTIONS_PID)` 2>/dev/null; then \
		echo "Service Transactions уже запущен (PID: `cat $(TRANSACTIONS_PID)`)"; \
	else \
		echo "Запуск Service Transactions..."; \
		$(TRANSACTIONS_CMD) & \
		echo $$! > $(TRANSACTIONS_PID); \
		echo "Service Transactions запущен (PID: $$!)"; \
	fi

start-profile: $(PID_DIR)
	@if [ -f $(PROFILE_PID) ] && kill -0 `cat $(PROFILE_PID)` 2>/dev/null; then \
		echo "Service Profile уже запущен (PID: `cat $(PROFILE_PID)`)"; \
	else \
		echo "Запуск Service Profile..."; \
		$(PROFILE_CMD) & \
		echo $$! > $(PROFILE_PID); \
		echo "Service Profile запущен (PID: $$!)"; \
	fi

start-balance: $(PID_DIR)
	@if [ -f $(BALANCE_PID) ] && kill -0 `cat $(BALANCE_PID)` 2>/dev/null; then \
		echo "Service Balance уже запущен (PID: `cat $(BALANCE_PID)`)"; \
	else \
		echo "Запуск Service Balance..."; \
		$(BALANCE_CMD) & \
		echo $$! > $(BALANCE_PID); \
		echo "Service Balance запущен (PID: $$!)"; \
	fi

start-game: $(PID_DIR)
	@if [ -f $(GAME_PID) ] && kill -0 `cat $(GAME_PID)` 2>/dev/null; then \
		echo "Service Game уже запущен (PID: `cat $(GAME_PID)`)"; \
	else \
		echo "Запуск Service Game..."; \
		$(GAME_CMD) & \
		echo $$! > $(GAME_PID); \
		echo "Service Game запущен (PID: $$!)"; \
	fi

start-front: $(PID_DIR)
	@if [ -f $(FRONT_PID) ] && kill -0 `cat $(FRONT_PID)` 2>/dev/null; then \
		echo "Frontend уже запущен (PID: `cat $(FRONT_PID)`)"; \
	else \
		echo "Запуск Frontend..."; \
		$(FRONT_CMD) & \
		echo $$! > $(FRONT_PID); \
		echo "Frontend запущен (PID: $$!)"; \
	fi

stop-envoy:
	@if [ -f $(ENVOY_PID) ]; then \
		pid=$$(cat $(ENVOY_PID)); \
		if kill -0 $$pid 2>/dev/null; then \
			echo "Остановка Envoy (PID: $$pid)..."; \
			kill $$pid && rm $(ENVOY_PID) && echo "Envoy остановлен"; \
		else \
			echo "Envoy не запущен, удаляю PID файл"; \
			rm $(ENVOY_PID); \
		fi; \
	else \
		echo "Envoy не запущен"; \
	fi

stop-transactions:
	@if [ -f $(TRANSACTIONS_PID) ]; then \
		pid=$$(cat $(TRANSACTIONS_PID)); \
		if kill -0 $$pid 2>/dev/null; then \
			echo "Остановка Service Transactions (PID: $$pid)..."; \
			kill $$pid && rm $(TRANSACTIONS_PID) && echo "Service Transactions остановлен"; \
		else \
			echo "Service Transactions не запущен, удаляю PID файл"; \
			rm $(TRANSACTIONS_PID); \
		fi; \
	else \
		echo "Service Transactions не запущен"; \
	fi

stop-profile:
	@if [ -f $(PROFILE_PID) ]; then \
		pid=$$(cat $(PROFILE_PID)); \
		if kill -0 $$pid 2>/dev/null; then \
			echo "Остановка Service Profile (PID: $$pid)..."; \
			kill $$pid && rm $(PROFILE_PID) && echo "Service Profile остановлен"; \
		else \
			echo "Service Profile не запущен, удаляю PID файл"; \
			rm $(PROFILE_PID); \
		fi; \
	else \
		echo "Service Profile не запущен"; \
	fi

stop-balance:
	@if [ -f $(BALANCE_PID) ]; then \
		pid=$$(cat $(BALANCE_PID)); \
		if kill -0 $$pid 2>/dev/null; then \
			echo "Остановка Service Balance (PID: $$pid)..."; \
			kill $$pid && rm $(BALANCE_PID) && echo "Service Balance остановлен"; \
		else \
			echo "Service Balance не запущен, удаляю PID файл"; \
			rm $(BALANCE_PID); \
		fi; \
	else \
		echo "Service Balance не запущен"; \
	fi

stop-game:
	@if [ -f $(GAME_PID) ]; then \
		pid=$$(cat $(GAME_PID)); \
		if kill -0 $$pid 2>/dev/null; then \
			echo "Остановка Service Game (PID: $$pid)..."; \
			kill $$pid && rm $(GAME_PID) && echo "Service Game остановлен"; \
		else \
			echo "Service Game не запущен, удаляю PID файл"; \
			rm $(GAME_PID); \
		fi; \
	else \
		echo "Service Game не запущен"; \
	fi

stop-front:
	@if [ -f $(FRONT_PID) ]; then \
		pid=$$(cat $(FRONT_PID)); \
		if kill -0 $$pid 2>/dev/null; then \
			echo "Остановка Frontend (PID: $$pid)..."; \
			kill $$pid && rm $(FRONT_PID) && echo "Frontend остановлен"; \
		else \
			echo "Frontend не запущен, удаляю PID файл"; \
			rm $(FRONT_PID); \
		fi; \
	else \
		echo "Frontend не запущен"; \
	fi

status:
	@echo "=== Статус сервисов ==="
	@for service in envoy transactions profile balance game front; do \
		pid_file="$(PID_DIR)/$$service.pid"; \
		if [ -f "$$pid_file" ]; then \
			pid=$$(cat $$pid_file); \
			if kill -0 $$pid 2>/dev/null; then \
				echo "$$service: запущен (PID: $$pid)"; \
			else \
				echo "$$service: PID файл есть, но процесс не запущен"; \
			fi; \
		else \
			echo "$$service: не запущен"; \
		fi; \
	done

clean:
	@echo "Очистка PID файлов..."
	@-rm -rf $(PID_DIR)
	@echo "PID файлы удалены"

clean-all: clean
	@echo "Очистка виртуального окружения..."
	@-rm -rf $(VENV)
	@echo "Виртуальное окружение удалено"

help:
	@echo "Доступные команды:"
	@echo ""
	@echo "  Настройка окружения:"
	@echo "    make setup        - Создать виртуальное окружение и установить зависимости"
	@echo "    make install      - Установить Python зависимости"
	@echo ""
	@echo "  Управление сервисами:"
	@echo "    make start        - Запустить все сервисы"
	@echo "    make stop         - Остановить все сервисы"
	@echo "    make restart      - Перезапустить все сервисы"
	@echo "    make status       - Показать статус всех сервисов"
	@echo ""
	@echo "  Очистка:"
	@echo "    make clean        - Удалить все PID файлы"
	@echo "    make clean-all    - Удалить PID файлы и виртуальное окружение"
	@echo ""
	@echo "  Запуск отдельных сервисов:"
	@echo "    make start-envoy, make stop-envoy"
	@echo "    make start-transactions, make stop-transactions"
	@echo "    make start-profile, make stop-profile"
	@echo "    make start-balance, make stop-balance"
	@echo "    make start-game, make stop-game"
	@echo "    make start-front, make stop-front"
	@echo ""
	@echo "  make help           - Показать эту справку"
