import grpc
from concurrent import futures
import user_balance_pb2_grpc as pb2_grpc
import user_balance_pb2 as pb2
from pathlib import Path
import threading
import json

BALANCE_DB = Path("user_balance_db.json")
LOCK = threading.Lock()  # для потокобезопасного доступа

_NOT_FOUND = pb2.StatusResponse.StatusCode.USER_NOT_FOUND
_ERR = pb2.StatusResponse.StatusCode.ERROR
_OK = pb2.StatusResponse.StatusCode.OK


class UserBalanceService(pb2_grpc.UserBalanceServicer):
    def __init__(self):
        if not BALANCE_DB.exists():
            BALANCE_DB.write_text("{}")

    def register_user_balance(self, request, context):
        data = self._read_db()

        if request.user_id in data:
            return pb2.StatusResponse(
                code=_NOT_FOUND,
                message=f"User {request.user_id} already exists!",
            )

        data[request.user_id] = 0.0
        self._write_db(data)
        return pb2.StatusResponse(code=_OK, message="User registered.")

    def get_balance(self, request, context):
        data = self._read_db()

        if request.user_id in data:
            return pb2.StatusResponse(
                code=_OK,
                user_balance=data[request.user_id],
            )
        else:
            return pb2.StatusResponse(
                code=_NOT_FOUND,
                message=f"Can't find user with id '{request.user_id}'.",
            )

    def deposit(self, request, context):
        data = self._read_db()

        if request.user_id not in data:
            return pb2.StatusResponse(
                code=_NOT_FOUND,
                message=f"Can't find user with id '{request.user_id}'.",
            )

        data[request.user_id] += request.amount_delta
        self._write_db(data)
        return pb2.StatusResponse(code=_OK, user_balance=data[request.user_id])

    def withdraw(self, request, context):
        data = self._read_db()

        if request.user_id not in data:
            return pb2.StatusResponse(
                code=_NOT_FOUND,
                message=f"Can't find user with id '{request.user_id}'.",
            )

        if data[request.user_id] < request.amount_delta:
            return pb2.StatusResponse(
                code=_ERR,
                message=f"Not enough balance for user '{request.user_id}'!",
            )

        data[request.user_id] -= request.amount_delta
        self._write_db(data)
        return pb2.StatusResponse(code=_OK, user_balance=data[request.user_id])

    def _read_db(self):
        with LOCK:
            with BALANCE_DB.open("r") as f:
                return json.load(f)

    def _write_db(self, data):
        with LOCK:
            with BALANCE_DB.open("w") as f:
                json.dump(data, f)


def main():
    service = UserBalanceService()
    grpc_server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )  # 10 потоков на обработку запросов
    pb2_grpc.add_UserBalanceServicer_to_server(service, grpc_server)
    grpc_server.add_insecure_port("localhost:5005")

    grpc_server.start()
    grpc_server.wait_for_termination()


if __name__ == "__main__":
    main()
