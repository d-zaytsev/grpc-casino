from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UserDepositRequest(_message.Message):
    __slots__ = ("name", "password_hash", "amount")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_HASH_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    name: str
    password_hash: str
    amount: float
    def __init__(self, name: _Optional[str] = ..., password_hash: _Optional[str] = ..., amount: _Optional[float] = ...) -> None: ...

class TransactionResponse(_message.Message):
    __slots__ = ("code", "message")
    class StatusCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        OK: _ClassVar[TransactionResponse.StatusCode]
        USER_NOT_FOUND: _ClassVar[TransactionResponse.StatusCode]
        ERROR: _ClassVar[TransactionResponse.StatusCode]
    OK: TransactionResponse.StatusCode
    USER_NOT_FOUND: TransactionResponse.StatusCode
    ERROR: TransactionResponse.StatusCode
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    code: TransactionResponse.StatusCode
    message: str
    def __init__(self, code: _Optional[_Union[TransactionResponse.StatusCode, str]] = ..., message: _Optional[str] = ...) -> None: ...
