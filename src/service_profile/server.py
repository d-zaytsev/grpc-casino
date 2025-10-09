import service_profile.user_profile_pb2_grpc as pb2_grpc
import service_profile.user_profile_pb2 as pb2
from pathlib import Path
import threading
import grpc
from concurrent import futures
import json
import uuid
from service_balance.client import UserBalanceClient
from json import JSONDecodeError

BALANCE_DB = Path("user_profile_db.json")
LOCK = threading.Lock()
SERVICE_CONNECT_DATA = "localhost:5004"

_NOT_FOUND = pb2.StatusResponse.StatusCode.USER_NOT_FOUND
_ERR = pb2.StatusResponse.StatusCode.ERROR
_OK = pb2.StatusResponse.StatusCode.OK


class UserProfileServer(pb2_grpc.UserProfileServicer):
    def __init__(self):
        if not BALANCE_DB.exists():
            BALANCE_DB.write_text("{}")

    def register_user(self, request, context):
        try:
            data = self._read_db()
        except Exception as e:
            return pb2.StatusResponse(code=_ERR, message=f"Failed to read DB: {e}")

        usr_name = request.name
        usr_pass_hash = request.password_hash

        if usr_name in data:
            return pb2.StatusResponse(
                code=_ERR,
                message=f"User {usr_name} already exists!",
            )

        usr_uuid = str(uuid.uuid4())
        data[usr_name] = {"uuid": usr_uuid, "hash": usr_pass_hash}

        try:
            self._write_db(data)
        except Exception as e:
            return pb2.StatusResponse(code=_ERR, message=f"Failed to write DB: {e}")

        try:
            balance_service = UserBalanceClient()
            balance_service.register_user_balance(usr_uuid)
            usr_balance = balance_service.get_balance(usr_uuid)
        except grpc.RpcError as rpc_err:
            return pb2.StatusResponse(
                code=_ERR, message=f"Balance service RPC error: {rpc_err.details()}"
            )
        except Exception as e:
            return pb2.StatusResponse(
                code=_ERR, message=f"Unexpected balance service error: {e}"
            )
        finally:
            if "balance_service" in locals():
                balance_service.close()

        profile_info = pb2.UserProfileInfo(
            name=usr_name,
            password_hash=usr_pass_hash,
            balance=usr_balance,
            user_uuid=usr_uuid,
        )

        return pb2.StatusResponse(
            code=_OK, message="User registered.", user_profile=profile_info
        )

    def get_user_profile(self, request, context):
        try:
            data = self._read_db()
        except Exception as e:
            return pb2.StatusResponse(code=_ERR, message=f"Failed to read DB: {e}")

        usr_name = request.name
        usr_pass_hash = request.password_hash

        if usr_name not in data:
            return pb2.StatusResponse(
                code=_NOT_FOUND,
                message=f"User {usr_name} doesn't exist!",
            )

        usr_data = data[usr_name]
        usr_uuid = usr_data["uuid"]

        if usr_pass_hash != usr_data["hash"]:
            return pb2.StatusResponse(
                code=_ERR,
                message=f"Incorrect password for user {usr_name}!",
            )

        try:
            balance_service = UserBalanceClient()
            usr_balance = balance_service.get_balance(usr_uuid)
        except grpc.RpcError as rpc_err:
            return pb2.StatusResponse(
                code=_ERR, message=f"Balance service RPC error: {rpc_err.details()}"
            )
        except Exception as e:
            return pb2.StatusResponse(
                code=_ERR, message=f"Unexpected balance service error: {e}"
            )
        finally:
            if "balance_service" in locals():
                balance_service.close()

        profile_info = pb2.UserProfileInfo(
            name=usr_name,
            password_hash=usr_pass_hash,
            balance=usr_balance,
            user_uuid=usr_uuid,
        )

        return pb2.StatusResponse(
            code=_OK, message="Here is your user's info!", user_profile=profile_info
        )

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

    def _write_db(self, data):
        with LOCK:
            try:
                with BALANCE_DB.open("w") as f:
                    json.dump(data, f)
            except Exception as e:
                raise RuntimeError(f"DB write error: {e}")


def main():
    service = UserProfileServer()
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_UserProfileServicer_to_server(service, grpc_server)
    grpc_server.add_insecure_port(SERVICE_CONNECT_DATA)
    grpc_server.start()
    grpc_server.wait_for_termination()


if __name__ == "__main__":
    main()
