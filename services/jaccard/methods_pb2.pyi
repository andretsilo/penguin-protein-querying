from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Ack(_message.Message):
    __slots__ = ("success", "message")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class ProteinBatch(_message.Message):
    __slots__ = ("proteins",)
    PROTEINS_FIELD_NUMBER: _ClassVar[int]
    proteins: _containers.RepeatedCompositeFieldContainer[Protein]
    def __init__(self, proteins: _Optional[_Iterable[_Union[Protein, _Mapping]]] = ...) -> None: ...

class JaccardTuple(_message.Message):
    __slots__ = ("entry", "jaccard")
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    JACCARD_FIELD_NUMBER: _ClassVar[int]
    entry: str
    jaccard: float
    def __init__(self, entry: _Optional[str] = ..., jaccard: _Optional[float] = ...) -> None: ...

class MatchResult(_message.Message):
    __slots__ = ("query_protein", "correlations")
    QUERY_PROTEIN_FIELD_NUMBER: _ClassVar[int]
    CORRELATIONS_FIELD_NUMBER: _ClassVar[int]
    query_protein: Protein
    correlations: _containers.RepeatedCompositeFieldContainer[JaccardTuple]
    def __init__(self, query_protein: _Optional[_Union[Protein, _Mapping]] = ..., correlations: _Optional[_Iterable[_Union[JaccardTuple, _Mapping]]] = ...) -> None: ...

class EntryList(_message.Message):
    __slots__ = ("entries",)
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    entries: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, entries: _Optional[_Iterable[str]] = ...) -> None: ...

class SaveStateRequest(_message.Message):
    __slots__ = ("state_name", "overwrite")
    STATE_NAME_FIELD_NUMBER: _ClassVar[int]
    OVERWRITE_FIELD_NUMBER: _ClassVar[int]
    state_name: str
    overwrite: bool
    def __init__(self, state_name: _Optional[str] = ..., overwrite: bool = ...) -> None: ...

class RollbackRequest(_message.Message):
    __slots__ = ("state_name", "confirm")
    STATE_NAME_FIELD_NUMBER: _ClassVar[int]
    CONFIRM_FIELD_NUMBER: _ClassVar[int]
    state_name: str
    confirm: bool
    def __init__(self, state_name: _Optional[str] = ..., confirm: bool = ...) -> None: ...

class StateList(_message.Message):
    __slots__ = ("names",)
    NAMES_FIELD_NUMBER: _ClassVar[int]
    names: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, names: _Optional[_Iterable[str]] = ...) -> None: ...

class StateName(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class Protein(_message.Message):
    __slots__ = ("id", "entry", "reviewed", "entry_name", "protein_names", "gene_names", "organism", "interpro", "ec_number", "sequence")
    ID_FIELD_NUMBER: _ClassVar[int]
    ENTRY_FIELD_NUMBER: _ClassVar[int]
    REVIEWED_FIELD_NUMBER: _ClassVar[int]
    ENTRY_NAME_FIELD_NUMBER: _ClassVar[int]
    PROTEIN_NAMES_FIELD_NUMBER: _ClassVar[int]
    GENE_NAMES_FIELD_NUMBER: _ClassVar[int]
    ORGANISM_FIELD_NUMBER: _ClassVar[int]
    INTERPRO_FIELD_NUMBER: _ClassVar[int]
    EC_NUMBER_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    id: str
    entry: str
    reviewed: str
    entry_name: str
    protein_names: str
    gene_names: str
    organism: str
    interpro: str
    ec_number: str
    sequence: str
    def __init__(self, id: _Optional[str] = ..., entry: _Optional[str] = ..., reviewed: _Optional[str] = ..., entry_name: _Optional[str] = ..., protein_names: _Optional[str] = ..., gene_names: _Optional[str] = ..., organism: _Optional[str] = ..., interpro: _Optional[str] = ..., ec_number: _Optional[str] = ..., sequence: _Optional[str] = ...) -> None: ...
