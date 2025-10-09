import grpc
import service_profile.user_profile_pb2_grpc as pb2_grpc
import service_profile.user_profile_pb2 as pb2


class UserProfileClient:
    def __init__(self, host: str = "localhost", port: int = 5004):
        self._host = host
        self._port = port

        self._channel = grpc.insecure_channel(f"{self._host}:{self._port}")
        self._grpc_stub = pb2_grpc.UserProfileStub(self._channel)

    def register_user(self, name: str, pass_hash: str) -> tuple[float, str] | None:
        response = self._grpc_stub.register_user(
            pb2.UserLogInfo(name=name, password_hash=pass_hash)
        )

        if response.code == pb2.StatusResponse.StatusCode.OK:
            user_uuid = response.user_profile.user_uuid
            print(f"User '{name}' registered successfully as '{user_uuid}'.")
            return response.user_profile.balance, user_uuid
        else:
            print(f"Failed to register user '{name}': {response.message}")
            return None

    def get_user_profile(self, name: str, pass_hash: str) -> tuple[float, str] | None:
        response = self._grpc_stub.get_user_profile(
            pb2.UserLogInfo(name=name, password_hash=pass_hash)
        )

        if response.code == pb2.StatusResponse.StatusCode.OK:
            print(f"Get user '{name}' profile!")
            return response.user_profile.balance, response.user_profile.user_uuid
        else:
            print(f"Failed to get user '{name}': {response.message}")
            return None

    def close(self):
        self._channel.close()
