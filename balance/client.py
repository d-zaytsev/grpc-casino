import grpc
import user_balance_pb2_grpc as pb2_grpc
import user_balance_pb2 as pb2


class UserBalanceClient:
    def __init__(self, host: str = "localhost", port: int = 5005):
        self._host = host
        self._port = port

        self._channel = grpc.insecure_channel(f"{self._host}:{self._port}")
        self._grpc_stub = pb2_grpc.UserBalanceStub(self._channel)

    def register_user_balance(self, user_id: str) -> bool:
        response = self._grpc_stub.register_user_balance(pb2.User(user_id=user_id))

        if response.code == pb2.StatusResponse.StatusCode.OK:
            print(f"User '{user_id}' registered successfully.")
            return True
        else:
            print(f"Failed to register user '{user_id}': {response.message}")
            return False

    def get_balance(self, user_id: str) -> float | None:
        request = pb2.User(user_id=user_id)
        response = self._grpc_stub.get_balance(request)

        if response.code == pb2.StatusResponse.StatusCode.OK:
            print(f"Balance for user '{user_id}': {response.user_balance}")
            return response.user_balance
        else:
            print(f"Error fetching balance for '{user_id}': {response.message}")
            return None

    def deposit(self, user_id: str, amount: float) -> float | None:
        request = pb2.UpdateRequest(user_id=user_id, amount_delta=amount)
        response = self._grpc_stub.deposit(request)

        if response.code == pb2.StatusResponse.StatusCode.OK:
            print(
                f"Deposited {amount} to '{user_id}'. New balance: {response.user_balance}"
            )
            return response.user_balance
        else:
            print(f"Deposit failed for '{user_id}': {response.message}")
            return None

    def withdraw(self, user_id: str, amount: float) -> float | None:
        request = pb2.UpdateRequest(user_id=user_id, amount_delta=amount)
        response = self._grpc_stub.withdraw(request)

        if response.code == pb2.StatusResponse.StatusCode.OK:
            print(
                f"Withdrew {amount} from '{user_id}'. New balance: {response.user_balance}"
            )
            return response.user_balance
        else:
            print(f"Withdrawal failed for '{user_id}': {response.message}")
            return None

    def close(self):
        self._channel.close()


if __name__ == "__main__":
    client = UserBalanceClient()
    result = client.register_user_balance(3)
    result = client.get_balance(3)