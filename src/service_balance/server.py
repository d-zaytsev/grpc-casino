import grpc
from concurrent import futures
import service_balance.user_balance_pb2_grpc as pb2_grpc
import service_balance.user_balance_pb2 as pb2
from pathlib import Path
import threading
import json
from json import JSONDecodeError

BALANCE_DB = Path("user_balance_db.json")
LOCK = threading.Lock()
SERVICE_CONNECT_DATA = "localhost:5005"

_NOT_FOUND = pb2.StatusResponse.StatusCode.USER_NOT_FOUND
_ERR = pb2.StatusResponse.StatusCode.ERROR
_OK = pb2.StatusResponse.StatusCode.OK


class UserBalanceService(pb2_grpc.UserBalanceServicer):
    def __init__(self):
        if not BALANCE_DB.exists():
            BALANCE_DB.write_text("{}")

    def register_user_balance(self, request, context):
        try:
            data = self._read_db()
        except Exception as e:
            return pb2.StatusResponse(code=_ERR, message=f"Failed to read DB: {e}")

        if request.user_uuid in data:
            return pb2.StatusResponse(
                code=_ERR,
                message=f"User {request.user_uuid} already exists!",
            )

        data[request.user_uuid] = 0.0

        try:
            self._write_db(data)
        except Exception as e:
            return pb2.StatusResponse(code=_ERR, message=f"Failed to write DB: {e}")

        return pb2.StatusResponse(code=_OK, message="User registered.")

    def get_balance(self, request, context):
        try:
            data = self._read_db()
        except Exception as e:
            return pb2.StatusResponse(code=_ERR, message=f"Failed to read DB: {e}")

        if request.user_uuid not in data:
            return pb2.StatusResponse(
                code=_NOT_FOUND,
                message=f"Can't find user with id '{request.user_uuid}'.",
            )

        balance = data[request.user_uuid]
        return pb2.StatusResponse(code=_OK, user_balance=balance)

    def deposit(self, request, context):
        try:
            data = self._read_db()
        except Exception as e:
            return pb2.StatusResponse(code=_ERR, message=f"Failed to read DB: {e}")

        if request.user_uuid not in data:
            return pb2.StatusResponse(
                code=_NOT_FOUND,
                message=f"Can't find user with id '{request.user_uuid}'.",
            )

        try:
            amount = float(request.amount_delta)
            data[request.user_uuid] += amount
            self._write_db(data)
        except Exception as e:
            return pb2.StatusResponse(code=_ERR, message=f"Write failed: {e}")

        return pb2.StatusResponse(code=_OK, user_balance=data[request.user_uuid])

    def withdraw(self, request, context):
        try:
            data = self._read_db()
        except Exception as e:
            return pb2.StatusResponse(code=_ERR, message=f"Failed to read DB: {e}")

        if request.user_uuid not in data:
            return pb2.StatusResponse(
                code=_NOT_FOUND,
                message=f"Can't find user with id '{request.user_uuid}'.",
            )

        current_balance = data[request.user_uuid]
        amount = float(request.amount_delta)

        if current_balance < amount:
            return pb2.StatusResponse(
                code=_ERR,
                message=f"Not enough balance for user '{request.user_uuid}'! "
                f"Current: {current_balance}, requested: {amount}",
            )

        data[request.user_uuid] -= amount

        try:
            self._write_db(data)
        except Exception as e:
            return pb2.StatusResponse(code=_ERR, message=f"Write failed: {e}")

        return pb2.StatusResponse(code=_OK, user_balance=data[request.user_uuid])

    def _read_db(self) -> dict:
        with LOCK:
            try:
                with BALANCE_DB.open("r") as f:
                    return json.load(f)
            except (FileNotFoundError, JSONDecodeError):
                BALANCE_DB.write_text("{}")
                return {}
            except Exception as e:
                raise RuntimeError(f"DB read error: {e}")

    def _write_db(self, data: dict):
        with LOCK:
            try:
                with BALANCE_DB.open("w") as f:
                    json.dump(data, f)
            except Exception as e:
                raise RuntimeError(f"DB write error: {e}")


def main():
    service = UserBalanceService()
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_UserBalanceServicer_to_server(service, grpc_server)
    grpc_server.add_insecure_port(SERVICE_CONNECT_DATA)
    grpc_server.start()
    grpc_server.wait_for_termination()


if __name__ == "__main__":
    main()
