# -*-encoding=utf-8-*-

from metadata import clang_type as clt


class CodeWriter:
    """
    向文件写入代码的对象
    """
    tuple_mode = ('w', 'wp')

    def __init__(self, _name, _mode='wp'):
        if type(_name) is not str:
            raise "type(_name) is not str"
        self.f = open(_name, 'w')
        self.mode = _mode
        if self.f is None:
            raise "file open failed"

    def wirte_to_file(self, _msg):
        """
        文件写入操作
        :param _msg: 写入内容
        :return:
        """
        if self.f is None:
            raise "file open failed"
        self.f.write(_msg)
        if self.mode == 'wp':
            '''
            模式为wp时，需要同时向terminal输出内容
            '''
            print(_msg)


class MappingEvn:
    """
    代码映射环境对象，主要是在递归映射代码时记录映射的语法元素对象，避免产生重复代码
    """
    tuple_kind = ("func", "com", "var")

    def __init__(self, _lang):
        self.sz_language = _lang
        self.arr_obj_fn = []
        self.arr_obj_com = []
        self.arr_obj_var = []

    def find(self, _item, _kind):
        """
        在映射环境中查询元素是否已经映射
        :param _item: 语法元素对象
        :param _kind: 类型，目前只关注"func" 函数对象, "com" 复合数据类型对象, "var" 全局变量对象
        :return:
        """
        if _kind not in self.tuple_kind:
            raise "_kind must in self.tuple_kind"
        if _kind == "func":
            if type(_item) is not clt.Function:
                raise "type(_fn) must clt.Function"
            for it in self.arr_obj_fn:
                if _item.sz_ELM_Name == it.sz_ELM_Name:
                    return True
            return False
        elif _kind == "com":
            if type(_item) is not clt.Compound:
                raise "type(_fn) must clt.Compound"
            for it in self.arr_obj_com:
                if _item.sz_ELM_Name == it.sz_ELM_Name:
                    return True
            return False
        elif _kind == "var":
            if type(_item) is not clt.Variable:
                raise "type(_fn) must clt.Variable"
            for it in self.arr_obj_var:
                if _item.sz_ELM_Name == it.sz_ELM_Name:
                    return True
            return False


class MappingList:
    """
    待映射列表，目前只关心函数对象
    """
    def __init__(self):
        self.arr_function = []


class MappingEngine:
    """
    映射引擎对象，驱动用户的代码映射过程
    """
    def __init__(self, _lang):
        self.sz_language = _lang
        pass

    def run(self, _l_mapping):
        pass


class MappingCore:
    """
    代码映射规则核心对象，负责具体的代码映射操作
    """
    def __init__(self, _lang):
        self.sz_language = _lang

    def mapping_core(self, _elm, _data=None):
        return ""


class BaseMappingRule:
    """
    代码映射用户接口基类
    """
    def __init__(self, _elm):
        self.obj_elm = _elm
        self.sz_language = ''

    def mapping(self, _core, _data=None):
        return ""


class VariableMappingRule(BaseMappingRule):
    """
    变量语法元素映射接口对象
    """
    def __init__(self, _elm):
        super(VariableMappingRule, self).__init__(_elm)
        pass

    def mapping(self, _core, _data=None):
        if type(self.obj_elm) is clt.Variable \
                and issubclass(type(_core), MappingCore):
            return _core.mapping_core(self.obj_elm, _data)
        else:
            raise "self.obj_elm must in { Variable }"


class AnotherNameMappingRule(BaseMappingRule):
    """
    重命名语法元素映射接口对象
    """
    def __init__(self, _elm):
        super(AnotherNameMappingRule, self).__init__(_elm)
        pass

    def mapping(self, _core, _data=None):
        if type(self.obj_elm) is clt.AnotherName \
                and issubclass(type(_core), MappingCore):
            return _core.mapping_core(self.obj_elm, _data)
        else:
            raise "self.obj_elm must in { AnotherName }"


class EnumeratorMappingRule(BaseMappingRule):
    """
    枚举元素语法元素映射接口对象
    """
    def __init__(self, _elm):
        super(EnumeratorMappingRule, self).__init__(_elm)
        pass

    def mapping(self, _core, _data=None):
        if type(self.obj_elm) is clt.Enumerator \
                and issubclass(type(_core), MappingCore):
            return _core.mapping_core(self.obj_elm, _data)
        else:
            raise "self.obj_elm must in { Enumerator }"


class FunctionMappingRule(BaseMappingRule):
    def __init__(self, _elm):
        super(FunctionMappingRule, self).__init__(_elm)
        pass

    def mapping(self, _core, _data=None):
        if type(self.obj_elm) is clt.Function \
                and issubclass(type(_core), MappingCore):
            return _core.mapping_core(self.obj_elm, _data)
        else:
            raise "self.obj_elm must in { Function }"


class DefineMappingRule(BaseMappingRule):
    def __init__(self, _elm):
        super(DefineMappingRule, self).__init__(_elm)
        pass

    def mapping(self, _core, _data=None):
        if type(self.obj_elm) is clt.Define \
                and issubclass(type(_core), MappingCore):
            return _core.mapping_core(self.obj_elm, _data)
        else:
            raise "self.obj_elm must in { Define }"


class BuildinMappingRule(BaseMappingRule):
    def __init__(self, _elm):
        super(BuildinMappingRule, self).__init__(_elm)
        pass

    def mapping(self, _core, _data=None):
        if type(self.obj_elm) is clt.BuildIn \
                and issubclass(type(_core), MappingCore):
            return _core.mapping_core(self.obj_elm, _data)
        else:
            raise "self.obj_elm must in { BuildIn }"


class DPointerMappingRule(BaseMappingRule):
    def __init__(self, _elm):
        super(DPointerMappingRule, self).__init__(_elm)
        pass

    def mapping(self, _core, _data=None):
        if type(self.obj_elm) is clt.DPointer \
                and issubclass(type(_core), MappingCore):
            return _core.mapping_core(self.obj_elm, _data)
        else:
            raise "self.obj_elm must in { DPointer }"


class FPointerMappingRule(BaseMappingRule):
    def __init__(self, _elm):
        super(FPointerMappingRule, self).__init__(_elm)
        pass

    def mapping(self, _core, _data=None):
        if type(self.obj_elm) is clt.FPointer \
                and issubclass(type(_core), MappingCore):
            return _core.mapping_core(self.obj_elm, _data)
        else:
            raise "self.obj_elm must in { FPointer }"


class ReferenceMappingRule(BaseMappingRule):
    def __init__(self, _elm):
        super(ReferenceMappingRule, self).__init__(_elm)
        pass

    def mapping(self, _core, _data=None):
        if type(self.obj_elm) is clt.Reference \
                and issubclass(type(_core), MappingCore):
            return _core.mapping_core(self.obj_elm, _data)
        else:
            raise "self.obj_elm must in { Reference }"


class CompoundMappingRule(BaseMappingRule):
    def __init__(self, _elm):
        super(CompoundMappingRule, self).__init__(_elm)
        pass

    def mapping(self, _core, _data=None):
        if type(self.obj_elm) is clt.Compound \
                and issubclass(type(_core), MappingCore):
            return _core.mapping_core(self.obj_elm, _data)
        else:
            raise "self.obj_elm must in { Compound }"


class EnumMappingRule(BaseMappingRule):
    def __init__(self, _elm):
        super(EnumMappingRule, self).__init__(_elm)
        pass

    def mapping(self, _core, _data=None):
        if type(self.obj_elm) is clt.Enum \
                and issubclass(type(_core), MappingCore):
            return _core.mapping_core(self.obj_elm, _data)
        else:
            raise "self.obj_elm must in { Enum }"
