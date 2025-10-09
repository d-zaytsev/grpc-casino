from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class User(_message.Message):
    __slots__ = ("user_uuid",)
    USER_UUID_FIELD_NUMBER: _ClassVar[int]
    user_uuid: str
    def __init__(self, user_uuid: _Optional[str] = ...) -> None: ...

class Balance(_message.Message):
    __slots__ = ("amount",)
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    amount: float
    def __init__(self, amount: _Optional[float] = ...) -> None: ...

class UpdateRequest(_message.Message):
    __slots__ = ("user_uuid", "amount_delta")
    USER_UUID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_DELTA_FIELD_NUMBER: _ClassVar[int]
    user_uuid: str
    amount_delta: float
    def __init__(self, user_uuid: _Optional[str] = ..., amount_delta: _Optional[float] = ...) -> None: ...

class StatusResponse(_message.Message):
    __slots__ = ("code", "message", "user_balance")
    class StatusCode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        OK: _ClassVar[StatusResponse.StatusCode]
        USER_NOT_FOUND: _ClassVar[StatusResponse.StatusCode]
        ERROR: _ClassVar[StatusResponse.StatusCode]
    OK: StatusResponse.StatusCode
    USER_NOT_FOUND: StatusResponse.StatusCode
    ERROR: StatusResponse.StatusCode
    CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    USER_BALANCE_FIELD_NUMBER: _ClassVar[int]
    code: StatusResponse.StatusCode
    message: str
    user_balance: float
    def __init__(self, code: _Optional[_Union[StatusResponse.StatusCode, str]] = ..., message: _Optional[str] = ..., user_balance: _Optional[float] = ...) -> None: ...
