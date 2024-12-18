from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DatiUtente(_message.Message):
    __slots__ = ("email", "ticker")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    TICKER_FIELD_NUMBER: _ClassVar[int]
    email: str
    ticker: str
    def __init__(self, email: _Optional[str] = ..., ticker: _Optional[str] = ...) -> None: ...

class Email(_message.Message):
    __slots__ = ("email",)
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    def __init__(self, email: _Optional[str] = ...) -> None: ...

class Conferma(_message.Message):
    __slots__ = ("conferma", "messaggio")
    CONFERMA_FIELD_NUMBER: _ClassVar[int]
    MESSAGGIO_FIELD_NUMBER: _ClassVar[int]
    conferma: bool
    messaggio: str
    def __init__(self, conferma: bool = ..., messaggio: _Optional[str] = ...) -> None: ...

class Valore(_message.Message):
    __slots__ = ("valore",)
    VALORE_FIELD_NUMBER: _ClassVar[int]
    valore: float
    def __init__(self, valore: _Optional[float] = ...) -> None: ...

class DatiMediaValori(_message.Message):
    __slots__ = ("email", "numeroDati")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NUMERODATI_FIELD_NUMBER: _ClassVar[int]
    email: str
    numeroDati: int
    def __init__(self, email: _Optional[str] = ..., numeroDati: _Optional[int] = ...) -> None: ...

class RegistraUtenteRequest(_message.Message):
    __slots__ = ("email", "ticker")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    TICKER_FIELD_NUMBER: _ClassVar[int]
    email: str
    ticker: str
    def __init__(self, email: _Optional[str] = ..., ticker: _Optional[str] = ...) -> None: ...
