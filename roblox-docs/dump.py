# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = dump_from_dict(json.loads(json_string))

from enum import Enum
from typing import Any, Callable, List, Optional, Type, TypeVar, Union, cast

T = TypeVar("T")
EnumT = TypeVar("EnumT", bound=Enum)


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def to_enum(c: Type[EnumT], x: Any) -> EnumT:
    assert isinstance(x, c)
    return x.value


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


class MemberType(Enum):
    CALLBACK = "Callback"
    EVENT = "Event"
    FUNCTION = "Function"
    PROPERTY = "Property"


class Category(Enum):
    CLASS = "Class"
    DATA_TYPE = "DataType"
    ENUM = "Enum"
    GROUP = "Group"
    PRIMITIVE = "Primitive"


class ReturnTypeClass:
    category: Category
    name: str

    def __init__(self, category: Category, name: str) -> None:
        self.category = category
        self.name = name

    @staticmethod
    def from_dict(obj: Any) -> "ReturnTypeClass":
        assert isinstance(obj, dict)
        category = Category(obj.get("Category"))
        name = from_str(obj.get("Name"))
        return ReturnTypeClass(category, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Category"] = to_enum(Category, self.category)
        result["Name"] = from_str(self.name)
        return result


class Parameter:
    name: str
    type: ReturnTypeClass
    default: Optional[str]

    def __init__(
        self, name: str, type: ReturnTypeClass, default: Optional[str]
    ) -> None:
        self.name = name
        self.type = type
        self.default = default

    @staticmethod
    def from_dict(obj: Any) -> "Parameter":
        assert isinstance(obj, dict)
        name = from_str(obj.get("Name"))
        type = ReturnTypeClass.from_dict(obj.get("Type"))
        default = from_union([from_str, from_none], obj.get("Default"))
        return Parameter(name, type, default)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Name"] = from_str(self.name)
        result["Type"] = to_class(ReturnTypeClass, self.type)
        result["Default"] = from_union([from_str, from_none], self.default)
        return result


class Security(Enum):
    LOCAL_USER_SECURITY = "LocalUserSecurity"
    NONE = "None"
    NOT_ACCESSIBLE_SECURITY = "NotAccessibleSecurity"
    PLUGIN_SECURITY = "PluginSecurity"
    ROBLOX_SCRIPT_SECURITY = "RobloxScriptSecurity"
    ROBLOX_SECURITY = "RobloxSecurity"


class SecurityClass:
    read: Security
    write: Security

    def __init__(self, read: Security, write: Security) -> None:
        self.read = read
        self.write = write

    @staticmethod
    def from_dict(obj: Any) -> "SecurityClass":
        assert isinstance(obj, dict)
        read = Security(obj.get("Read"))
        write = Security(obj.get("Write"))
        return SecurityClass(read, write)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Read"] = to_enum(Security, self.read)
        result["Write"] = to_enum(Security, self.write)
        return result


class Serialization:
    can_load: bool
    can_save: bool

    def __init__(self, can_load: bool, can_save: bool) -> None:
        self.can_load = can_load
        self.can_save = can_save

    @staticmethod
    def from_dict(obj: Any) -> "Serialization":
        assert isinstance(obj, dict)
        can_load = from_bool(obj.get("CanLoad"))
        can_save = from_bool(obj.get("CanSave"))
        return Serialization(can_load, can_save)

    def to_dict(self) -> dict:
        result: dict = {}
        result["CanLoad"] = from_bool(self.can_load)
        result["CanSave"] = from_bool(self.can_save)
        return result


class MemberTag(Enum):
    CAN_YIELD = "CanYield"
    CUSTOM_LUA_STATE = "CustomLuaState"
    DEPRECATED = "Deprecated"
    HIDDEN = "Hidden"
    NOT_BROWSABLE = "NotBrowsable"
    NOT_REPLICATED = "NotReplicated"
    NOT_SCRIPTABLE = "NotScriptable"
    NO_YIELD = "NoYield"
    READ_ONLY = "ReadOnly"
    YIELDS = "Yields"


class ThreadSafety(Enum):
    READ_SAFE = "ReadSafe"
    SAFE = "Safe"
    UNSAFE = "Unsafe"


class Member:
    category: Optional[str]
    member_type: MemberType
    name: str
    security: Union[SecurityClass, Security]
    serialization: Optional[Serialization]
    thread_safety: ThreadSafety
    value_type: Optional[ReturnTypeClass]
    tags: Optional[List[MemberTag]]
    parameters: Optional[List[Parameter]]
    return_type: Optional[ReturnTypeClass]

    def __init__(
        self,
        category: Optional[str],
        member_type: MemberType,
        name: str,
        security: Union[SecurityClass, Security],
        serialization: Optional[Serialization],
        thread_safety: ThreadSafety,
        value_type: Optional[ReturnTypeClass],
        tags: Optional[List[MemberTag]],
        parameters: Optional[List[Parameter]],
        return_type: Optional[ReturnTypeClass],
    ) -> None:
        self.category = category
        self.member_type = member_type
        self.name = name
        self.security = security
        self.serialization = serialization
        self.thread_safety = thread_safety
        self.value_type = value_type
        self.tags = tags
        self.parameters = parameters
        self.return_type = return_type

    @staticmethod
    def from_dict(obj: Any) -> "Member":
        assert isinstance(obj, dict)
        category = from_union([from_str, from_none], obj.get("Category"))
        member_type = MemberType(obj.get("MemberType"))
        name = from_str(obj.get("Name"))
        security = from_union([SecurityClass.from_dict, Security], obj.get("Security"))
        serialization = from_union(
            [Serialization.from_dict, from_none], obj.get("Serialization")
        )
        thread_safety = ThreadSafety(obj.get("ThreadSafety"))
        value_type = from_union(
            [ReturnTypeClass.from_dict, from_none], obj.get("ValueType")
        )
        tags = from_union(
            [lambda x: from_list(MemberTag, x), from_none], obj.get("Tags")
        )
        parameters = from_union(
            [lambda x: from_list(Parameter.from_dict, x), from_none],
            obj.get("Parameters"),
        )
        return_type = from_union(
            [ReturnTypeClass.from_dict, from_none], obj.get("ReturnType")
        )
        return Member(
            category,
            member_type,
            name,
            security,
            serialization,
            thread_safety,
            value_type,
            tags,
            parameters,
            return_type,
        )

    def to_dict(self) -> dict:
        result: dict = {}
        result["Category"] = from_union([from_str, from_none], self.category)
        result["MemberType"] = to_enum(MemberType, self.member_type)
        result["Name"] = from_str(self.name)
        result["Security"] = from_union(
            [lambda x: to_class(SecurityClass, x), lambda x: to_enum(Security, x)],
            self.security,
        )
        result["Serialization"] = from_union(
            [lambda x: to_class(Serialization, x), from_none], self.serialization
        )
        result["ThreadSafety"] = to_enum(ThreadSafety, self.thread_safety)
        result["ValueType"] = from_union(
            [lambda x: to_class(ReturnTypeClass, x), from_none], self.value_type
        )
        result["Tags"] = from_union(
            [lambda x: from_list(lambda x: to_enum(MemberTag, x), x), from_none],
            self.tags,
        )
        result["Parameters"] = from_union(
            [lambda x: from_list(lambda x: to_class(Parameter, x), x), from_none],
            self.parameters,
        )
        result["ReturnType"] = from_union(
            [lambda x: to_class(ReturnTypeClass, x), from_none], self.return_type
        )
        return result


class MemoryCategory(Enum):
    ANIMATION = "Animation"
    GRAPHICS_TEXTURE = "GraphicsTexture"
    GUI = "Gui"
    INSTANCES = "Instances"
    INTERNAL = "Internal"
    PHYSICS_PARTS = "PhysicsParts"
    SCRIPT = "Script"


class ClassTag(Enum):
    DEPRECATED = "Deprecated"
    NOT_BROWSABLE = "NotBrowsable"
    NOT_CREATABLE = "NotCreatable"
    NOT_REPLICATED = "NotReplicated"
    PLAYER_REPLICATED = "PlayerReplicated"
    SERVICE = "Service"
    SETTINGS = "Settings"
    USER_SETTINGS = "UserSettings"


class Class:
    members: List[Member]
    memory_category: MemoryCategory
    name: str
    superclass: str
    tags: Optional[List[ClassTag]]

    def __init__(
        self,
        members: List[Member],
        memory_category: MemoryCategory,
        name: str,
        superclass: str,
        tags: Optional[List[ClassTag]],
    ) -> None:
        self.members = members
        self.memory_category = memory_category
        self.name = name
        self.superclass = superclass
        self.tags = tags

    @staticmethod
    def from_dict(obj: Any) -> "Class":
        assert isinstance(obj, dict)
        members = from_list(Member.from_dict, obj.get("Members"))
        memory_category = MemoryCategory(obj.get("MemoryCategory"))
        name = from_str(obj.get("Name"))
        superclass = from_str(obj.get("Superclass"))
        tags = from_union(
            [lambda x: from_list(ClassTag, x), from_none], obj.get("Tags")
        )
        return Class(members, memory_category, name, superclass, tags)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Members"] = from_list(lambda x: to_class(Member, x), self.members)
        result["MemoryCategory"] = to_enum(MemoryCategory, self.memory_category)
        result["Name"] = from_str(self.name)
        result["Superclass"] = from_str(self.superclass)
        result["Tags"] = from_union(
            [lambda x: from_list(lambda x: to_enum(ClassTag, x), x), from_none],
            self.tags,
        )
        return result


class Item:
    name: str
    value: int
    legacy_names: Optional[List[str]]
    tags: Optional[List[MemberTag]]

    def __init__(
        self,
        name: str,
        value: int,
        legacy_names: Optional[List[str]],
        tags: Optional[List[MemberTag]],
    ) -> None:
        self.name = name
        self.value = value
        self.legacy_names = legacy_names
        self.tags = tags

    @staticmethod
    def from_dict(obj: Any) -> "Item":
        assert isinstance(obj, dict)
        name = from_str(obj.get("Name"))
        value = from_int(obj.get("Value"))
        legacy_names = from_union(
            [lambda x: from_list(from_str, x), from_none], obj.get("LegacyNames")
        )
        tags = from_union(
            [lambda x: from_list(MemberTag, x), from_none], obj.get("Tags")
        )
        return Item(name, value, legacy_names, tags)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Name"] = from_str(self.name)
        result["Value"] = from_int(self.value)
        result["LegacyNames"] = from_union(
            [lambda x: from_list(from_str, x), from_none], self.legacy_names
        )
        result["Tags"] = from_union(
            [lambda x: from_list(lambda x: to_enum(MemberTag, x), x), from_none],
            self.tags,
        )
        return result


class EnumElement:
    items: List[Item]
    name: str
    tags: Optional[List[MemberTag]]

    def __init__(
        self, items: List[Item], name: str, tags: Optional[List[MemberTag]]
    ) -> None:
        self.items = items
        self.name = name
        self.tags = tags

    @staticmethod
    def from_dict(obj: Any) -> "EnumElement":
        assert isinstance(obj, dict)
        items = from_list(Item.from_dict, obj.get("Items"))
        name = from_str(obj.get("Name"))
        tags = from_union(
            [lambda x: from_list(MemberTag, x), from_none], obj.get("Tags")
        )
        return EnumElement(items, name, tags)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Items"] = from_list(lambda x: to_class(Item, x), self.items)
        result["Name"] = from_str(self.name)
        result["Tags"] = from_union(
            [lambda x: from_list(lambda x: to_enum(MemberTag, x), x), from_none],
            self.tags,
        )
        return result


class Dump:
    classes: List[Class]
    enums: List[EnumElement]
    version: int

    def __init__(
        self, classes: List[Class], enums: List[EnumElement], version: int
    ) -> None:
        self.classes = classes
        self.enums = enums
        self.version = version

    @staticmethod
    def from_dict(obj: Any) -> "Dump":
        assert isinstance(obj, dict)
        classes = from_list(Class.from_dict, obj.get("Classes"))
        enums = from_list(EnumElement.from_dict, obj.get("Enums"))
        version = from_int(obj.get("Version"))
        return Dump(classes, enums, version)

    def to_dict(self) -> dict:
        result: dict = {}
        result["Classes"] = from_list(lambda x: to_class(Class, x), self.classes)
        result["Enums"] = from_list(lambda x: to_class(EnumElement, x), self.enums)
        result["Version"] = from_int(self.version)
        return result


def dump_from_dict(s: Any) -> Dump:
    return Dump.from_dict(s)


def dump_to_dict(x: Dump) -> Any:
    return to_class(Dump, x)
