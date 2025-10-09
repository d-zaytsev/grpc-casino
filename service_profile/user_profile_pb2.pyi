from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UserLogInfo(_message.Message):
    __slots__ = ("name", "password_hash")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_HASH_FIELD_NUMBER: _ClassVar[int]
    name: str
    password_hash: str
    def __init__(self, name: _Optional[str] = ..., password_hash: _Optional[str] = ...) -> None: ...

class UserProfileInfo(_message.Message):
    __slots__ = ("name", "password_hash", "balance", "user_uuid")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_HASH_FIELD_NUMBER: _ClassVar[int]
    BALANCE_FIELD_NUMBER: _ClassVar[int]
    USER_UUID_FIELD_NUMBER: _ClassVar[int]
    name: str
    password_hash: str
    balance: float
    user_uuid: str
    def __init__(self, name: _Optional[str] = ..., password_hash: _Optional[str] = ..., balance: _Optional[float] = ..., user_uuid: _Optional[str] = ...) -> None: ...

class StatusResponse(_message.Message):
    __slots__ = ("code", "message", "user_profile")
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
    USER_PROFILE_FIELD_NUMBER: _ClassVar[int]
    code: StatusResponse.StatusCode
    message: str
    user_profile: UserProfileInfo
    def __init__(self, code: _Optional[_Union[StatusResponse.StatusCode, str]] = ..., message: _Optional[str] = ..., user_profile: _Optional[_Union[UserProfileInfo, _Mapping]] = ...) -> None: ...
