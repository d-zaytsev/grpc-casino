import service_profile.user_profile_pb2_grpc as pb2_grpc
import service_profile.user_profile_pb2 as pb2
from pathlib import Path
import threading
import grpc
from concurrent import futures
import json
import uuid
from service_balance.client import UserBalanceClient


BALANCE_DB = Path("user_profile_db.json")
LOCK = threading.Lock()  # для потокобезопасного доступа
SERVICE_CONNECT_DATA = "localhost:5004"

_NOT_FOUND = pb2.StatusResponse.StatusCode.USER_NOT_FOUND
_ERR = pb2.StatusResponse.StatusCode.ERROR
_OK = pb2.StatusResponse.StatusCode.OK


class UserProfileServer(pb2_grpc.UserProfileServicer):
    def __init__(self):
        if not BALANCE_DB.exists():
            BALANCE_DB.write_text("{}")

    def register_user(self, request, context):
        data = self._read_db()

        usr_name = request.name
        usr_pass_hash: str = request.password_hash

        if usr_name in data:
            return pb2.StatusResponse(
                code=_ERR,
                message=f"User {usr_name} already exists!",
            )

        usr_uuid: str = str(uuid.uuid4())

        data[usr_name] = usr_uuid
        self._write_db(data)

        balance_service = UserBalanceClient()
        balance_service.register_user_balance(usr_uuid)
        usr_balance = balance_service.get_balance(usr_uuid)
        balance_service.close()

        profile_info = pb2.UserProfileInfo(
            name=usr_name,
            password_hash=usr_pass_hash,
            balance=usr_balance,
            user_uuid=usr_uuid,
        )

        print(
            f"USER PROFILE SERVER: new user registered. Name: {usr_name} uuid: {usr_uuid}"
        )
        return pb2.StatusResponse(
            code=_OK, message="User registered.", user_profile=profile_info
        )

    def get_user_profile(self, request, context):
        data = self._read_db()

        usr_name = request.name
        usr_pass_hash: str = request.password_hash

        if usr_name not in data:
            return pb2.StatusResponse(
                code=_NOT_FOUND,
                message=f"User {usr_name} doesn't exist!",
            )

        usr_uuid = data[usr_name]

        balance_service = UserBalanceClient()
        balance_service.get_balance(usr_uuid)
        usr_balance = balance_service.get_balance(usr_uuid)
        balance_service.close()

        print(
            f"USER PROFILE SERVER: fetch user data. Name: {usr_name} uuid: {usr_uuid} balance: {usr_balance}"
        )
        profile_info = pb2.UserProfileInfo(
            name=usr_name,
            password_hash=usr_pass_hash,
            balance=usr_balance,
            user_uuid=usr_uuid,
        )

        return pb2.StatusResponse(
            code=_OK, message="Here is your user's info!", user_profile=profile_info
        )

    def _read_db(self) -> dict[tuple[str, str], str]:
        try:
            with LOCK:
                with BALANCE_DB.open("r") as f:
                    return json.load(f)
        except:  # noqa: E722
            return {}

    def _write_db(self, data):
        with LOCK:
            with BALANCE_DB.open("w") as f:
                json.dump(data, f)


def main():
    service = UserProfileServer()
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_UserProfileServicer_to_server(service, grpc_server)
    grpc_server.add_insecure_port(SERVICE_CONNECT_DATA)

    grpc_server.start()
    grpc_server.wait_for_termination()


if __name__ == "__main__":
    main()
