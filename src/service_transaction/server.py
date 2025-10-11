import service_transaction.money_transcation_pb2_grpc as pb2_grpc
import service_transaction.money_transcation_pb2 as pb2
import grpc
from concurrent import futures
from service_balance.client import UserBalanceClient
from service_profile.client import UserProfileClient

SERVICE_CONNECT_DATA = "localhost:5005"

_NOT_FOUND = pb2.StatusResponse.StatusCode.USER_NOT_FOUND
_ERR = pb2.StatusResponse.StatusCode.ERROR
_OK = pb2.StatusResponse.StatusCode.OK


class MoneyTransactionsServer(pb2_grpc.MoneyTransactonServicer):
    def deposit(self, request, context):
        name = request.name
        password_hash = request.password_hash
        amount = request.amount
        user_uuid = request.user_uuid

        try:
            profile_service = UserProfileClient()
            res = profile_service.get_user_profile(name=name, pass_hash=password_hash)

            if not res:
                return pb2.StatusResponse(code=_NOT_FOUND, message="User not found.")
        except grpc.RpcError as rpc_err:
            return pb2.StatusResponse(
                code=_ERR, message=f"Balance service RPC error: {rpc_err.details()}"
            )
        except Exception as e:
            return pb2.StatusResponse(
                code=_ERR, message=f"Unexpected balance service error: {e}"
            )
        finally:
            if "profile_service" in locals():
                profile_service.close()

        try:
            balance_service = UserBalanceClient()
            balance_service.deposit(user_uuid=user_uuid, amount=amount)
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

        return pb2.StatusResponse(code=_OK, message="Successfully deposit money.")
    
    def withdraw(self, request, context):
        raise NotImplementedError()

def main():
    service = MoneyTransactionsServer()
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_MoneyTransactonServicer_to_server(service, grpc_server)
    grpc_server.add_insecure_port(SERVICE_CONNECT_DATA)
    grpc_server.start()
    grpc_server.wait_for_termination()


if __name__ == "__main__":
    main()
