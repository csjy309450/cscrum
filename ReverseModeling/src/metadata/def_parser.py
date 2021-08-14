# 已弃用

from metadata.index_parser import *

class ComDefNode(XmlNode):
    def __init__(self, _name, _parent, _refid, _kind, _prot):
        super(ComDefNode, self).__init__(_name, _parent)
        self.refid = _refid
        self.kind = _kind
        self.prot = _prot
        self.compoundname = ''
        self.includes = ''


class SectionDefNode(XmlNode):
    list_SD_Type = [
        "public-attrib",
        "protected-attrib",
        "private-attrib",
        "public-func",
        "protected-func",
        "private-func",
    ]

    def __init__(self, _name, _parent, _kind):
        super(SectionDefNode, self).__init__(_name, _parent)
        if type(_kind) is not str \
                and _kind not in self.list_SD_Type:
            raise "<sectiondef>->kind must in {0,1,2}"
        self.kind = _kind


class MemDefNode(XmlNode):
    list_MD_Type = [
        "variable",
        "function",
    ]

    def __init__(self, _name, _parent, _kind, _refid, _prot, _static):
        super(MemDefNode, self).__init__(_name, _parent)
        self.kind = _kind
        self.refid = _refid
        self.prot = _prot
        self.static = _static
        self.stru_type = None


class TypeNode(XmlNode):
    """
    存放<type>节点的对象
    :var type_fraction 存放类型碎片，比如'const PARAM_IN int *'必须从中识别出'const int *'才是真正的类型
    """
    def __init__(self, _name, _parent):
        super(TypeNode, self).__init__(_name, _parent)
        self.type_fraction = []

class InitializerNode(XmlNode):
    def __init__(self, _name, _parent):
        super(InitializerNode, self).__init__(_name, _parent)
        self.init_fraction = []

class ParamNode(XmlNode):
    def __init__(self, _name, _parent):
        super(ParamNode, self).__init__(_name, _parent)
        self.param_type_fraction = []
        self.param_name = None
        self.param_array = None


class RefNode(XmlNode):
    def __init__(self, _name, _parent, _refid, _kindref):
        super(RefNode, self).__init__(_name, _parent)
        self.refid = _refid
        self.kindref = _kindref
        self.type_name = ''


class ComDefHandler(sax.handler.ContentHandler):
    def __init__(self, _indx_handler):
        super(ComDefHandler, self).__init__()
        self.stru_xml = IndexXml()
        self.stack_node = Stack()
        if type(_indx_handler) is not IndexHandler:
            raise "param \"_indx_handler\" must a instance of class IndexHandler"
        self.indx_handler = _indx_handler
        self.curr_member_node = None
        self.curr_com_type = None
        self.curr_member_type = None

    # 元素开始事件处理
    def startElement(self, tag, attributes):
        if tag == "doxygen":
            if not self.stack_node.is_empty():
                raise '<doxygen> must root node'
            self.stack_node.push([tag, XmlNode(tag, None)])
        elif tag == "compounddef":
            if not self.stack_node.top()[0] == "doxygen":
                raise '<compounddef> father must <doxygen>'
            node = ComDefNode(tag, self.stack_node.top(),attributes["id"], attributes["kind"], attributes["prot"])
            self.stack_node.push([tag, node])
            if attributes["kind"] in {'struct', 'class', 'union'}:
                '''
                搜索复合数据结构的对象
                '''
                self.curr_com_type = self.indx_handler.stru_xml.find(attributes["id"], 'compound')
                if self.curr_com_type is None:
                    raise 'curr_com_type mustn\'t None'
            elif attributes["kind"] == 'file':
                raise '<compounddef>.kind must in {\'struct\', \'class\', \'union\'}'
        elif tag == "compoundname":
            self.stack_node.push([tag, XmlNode(tag, self.stack_node.top())])
        elif tag == 'includes':
            self.stack_node.push([tag, XmlNode(tag, self.stack_node.top())])
        elif tag == "sectiondef":
            node = SectionDefNode(tag, self.stack_node.top(), attributes["kind"])
            self.stack_node.push([tag, node])
        elif tag == "memberdef": # 解析的重点
            node = MemDefNode(tag, self.stack_node.top(),
                              attributes["kind"],
                              attributes["id"],
                              attributes["prot"],
                              attributes["static"])
            self.stack_node.push([tag, node])
            self.curr_member_node = self.stack_node.top()
            self.curr_member_type = self.curr_com_type.find(attributes["id"])
            if self.curr_member_type is None:
                raise 'curr_com_type mustn\'t None'
        elif tag == "type":  # 解析的重点
            self.stack_node.push([tag, TypeNode(tag, self.stack_node.top())])
        elif tag == "ref":  # 解析的重点
            root = self.stack_node.top()
            node = None
            if root[0] == "type":
                node = RefNode(tag, self.stack_node.top(), attributes["refid"], attributes["kindref"])
                root[1].type_fraction.append(node)
            self.stack_node.push([tag, node])
        elif tag == "argsstring":
            self.stack_node.push([tag, XmlNode(tag, None)])


    # 元素结束事件处理
    def endElement(self, tag):
        if tag == "doxygen":
            if self.stack_node.is_empty():
                raise '</doxygen> must last node'
            pass
        elif tag == "compounddef":
            pass
        elif tag == "compoundname":
            pass
        elif tag == 'includes':
            pass
        elif tag == "sectiondef":
            pass
        elif tag == "memberdef":
            # fixme 完成一个成员的初始化
            # self.curr_member_type = clt.BuildIn(node[1].name, szBuildinType)
            pass
        elif tag == "type":
            if type(self.curr_member_type) is clt.Function:
                pass
            elif type(self.curr_member_type) is clt.Variable:
                node = self.stack_node.top()
                str_DT = None
                # 检测类型是否属于已建立索引的类型
                for it in node[1].type_fraction:
                    if type(it) is str:
                        szBuildinType = isBuildinType(it)
                        if szBuildinType is not None:
                            # FIXME c++ 内建数据类型应该有专门的数据库
                            str_DT = clt.BuildIn(it, szBuildinType)
                            break
                    elif type(it) is RefNode:
                        if it.kindref == 'compound':
                            str_DT = self.indx_handler.stru_xml.find(it.refid, 'compound')
                            if str_DT is not None:
                                break
                        elif it.kindref == 'member':
                            str_DT = self.indx_handler.stru_xml.assert_DDef(it.refid)
                            if str_DT is not None:
                                break
                            str_DT = self.indx_handler.stru_xml.assert_AN(it.refid)
                            if str_DT is not None:
                                break
                        else:
                            raise "it.kindref must \"compound\" or \"member\""
                    else:
                        raise "<type> content error!"
                if str_DT is not None:
                    if type(str_DT) is clt.BuildIn:
                        self.curr_member_type.stru_Var_TData = str_DT
                    else:
                        b_pointer = False
                        for it in node[1].type_fraction:
                            if type(it) is str:
                                if re.match('(( )*)\*(( )*)', it) is not None:
                                    b_pointer = True
                                    break
                        if b_pointer:
                            # FIXME 此处不应该新建类型，而是应该在全局的数据类型数据库拿
                            self.curr_member_type.stru_Var_TData = clt.DPointer(str_DT.sz_ELM_Name+' *', str_DT)
                        else:
                            self.curr_member_type.stru_Var_TData = str_DT
                else:
                    # FIXME 未知类型也应该建立索引
                    self.curr_member_type.stru_Var_TData = clt.TData(str(node[1].type_fraction), 0)
        elif tag == "ref":
            pass
        elif tag == "argsstring":
            pass
        else:
            return
        self.stack_node.pop()

    # 内容事件处理
    def characters(self, content):
        node = self.stack_node.top()
        if node == None:
            return
        if node[0] == "compoundname":
            node[1].compoundname = content
        elif node[0] == "includes":
            if node[1].parent[0] != "compounddef":
                raise "root of <includes> must <compounddef>"
            node[1].parent[1].includes = content
        elif node[0] == "type":
            node[1].type_fraction.append(content)
        elif node[0] == "ref":
            node[1].type_name = content
        elif node[0] == "argsstring":
            if type(self.curr_member_type) is clt.Variable:
                if re.match('\[.*\]', content):
                    sz_arrSize = content[1:len(content)-1]
                    # FIXME 此处应该增加确定 sz_arrSize 是否可检索
                    if issubclass(type(self.curr_member_type.stru_Var_TData), clt.TData):
                        self.curr_member_type.stru_Var_TData.sz_TD_ArrSize = sz_arrSize
                    elif type(self.curr_member_type.stru_Var_TData) is clt.AnotherName:
                        self.curr_member_type.stru_Var_TData.sz_TD_ArrSize = sz_arrSize
                    else:
                        raise "self.curr_member_type must a class of clt.TData or clt.AnotherName"
                else:
                    raise "<argsstring> content error!"


class FileDefHandler(sax.handler.ContentHandler):
    def __init__(self, _indx_handler):
        super(FileDefHandler, self).__init__()
        self.stack_node = Stack()
        if type(_indx_handler) is not IndexHandler:
            raise "param \"_indx_handler\" must a instance of class IndexHandler"
        self.indx_handler = _indx_handler
        self.curr_section_node = None
        self.curr_member_node = None
        self.curr_member_type = None

    # 元素开始事件处理
    def startElement(self, tag, attributes):
        if tag == "doxygen":
            if not self.stack_node.is_empty():
                raise '<doxygen> must root node'
            self.stack_node.push([tag, XmlNode(tag, None)])
        elif tag == "compounddef":
            if not self.stack_node.top()[0] == "doxygen":
                raise '<compounddef> father must <doxygen>'
            node = ComDefNode(tag, self.stack_node.top(),attributes["id"], attributes["kind"],None)
            self.stack_node.push([tag, node])
            if attributes["kind"] in {'struct', 'class', 'union'}:
                raise '<compounddef>.kind must file'
            elif attributes["kind"] == 'file':
                pass
        elif tag == "compoundname":
            self.stack_node.push([tag, XmlNode(tag, self.stack_node.top())])
        elif tag == 'innerclass':
            # 忽略<innerclass>
            pass
        elif tag == "sectiondef":
            node = SectionDefNode(tag, self.stack_node.top(), attributes["kind"])
            self.stack_node.push([tag, node])
            self.curr_section_node = node
        elif tag == "memberdef": # 解析的重点
            node = MemDefNode(tag, self.stack_node.top(),
                              attributes["kind"],
                              attributes["id"],
                              attributes["prot"],
                              attributes["static"])
            self.stack_node.push([tag, node])
            self.curr_member_node = self.stack_node.top()
            self.curr_member_type = self.indx_handler.stru_xml.find(attributes["id"], self.curr_section_node.kind)
            if self.curr_member_type is None:
                raise 'curr_member_type mustn\'t None'
        elif tag == "name":
            self.stack_node.push([tag, XmlNode(tag, self.stack_node.top())])
        elif tag == "initializer":
            self.stack_node.push([tag, InitializerNode(tag, self.stack_node.top())])
        elif tag == "type":  # 解析的重点
            self.stack_node.push([tag, TypeNode(tag, self.stack_node.top())])
        elif tag == "ref":  # 解析的重点
            root = self.stack_node.top()
            node = None
            if root[0] == "type":
                node = RefNode(tag, self.stack_node.top(), attributes["refid"], attributes["kindref"])
                root[1].type_fraction.append(node)
            elif root[0] == "initializer":
                node = RefNode(tag, self.stack_node.top(), attributes["refid"], attributes["kindref"])
                root[1].init_fraction.append(node)
            self.stack_node.push([tag, node])
        elif tag == "argsstring":
            self.stack_node.push([tag, XmlNode(tag, self.stack_node.top())])
        elif tag == "param":
            self.stack_node.push([tag, ParamNode(tag, self.stack_node.top())])


    # 元素结束事件处理
    def endElement(self, tag):
        if tag == "doxygen":
            if self.stack_node.is_empty():
                raise '</doxygen> must last node'
            pass
        elif tag == "compounddef":
            pass
        elif tag == "compoundname":
            pass
        elif tag == 'includes':
            pass
        elif tag == "sectiondef":
            pass
        elif tag == "memberdef":
            # fixme 完成一个成员的初始化
            # self.curr_member_type = clt.BuildIn(node[1].name, szBuildinType)
            pass
        elif tag == "name":
            pass
        elif tag == "initializer":
            if type(self.curr_member_type) is clt.Function:
                pass
            elif type(self.curr_member_type) is clt.Define:
                node = self.stack_node.top()
                str_DT = None
                # 检测类型是否属于已建立索引的类型
                for it in node[1].init_fraction:
                    if type(it) is str:
                        szBuildinType = isBuildinType(it)
                        if szBuildinType is not None:
                            # FIXME c++ 内建数据类型应该有专门的数据库
                            str_DT = clt.BuildIn(it, szBuildinType)
                            break
                    elif type(it) is RefNode:
                        if it.kindref == 'compound':
                            str_DT = self.indx_handler.stru_xml.find(it.refid, 'compound')
                            if str_DT is not None:
                                break
                        elif it.kindref == 'member':
                            str_DT = self.indx_handler.stru_xml.assert_DDef(it.refid)
                            if str_DT is not None:
                                break
                            str_DT = self.indx_handler.stru_xml.assert_AN(it.refid)
                            if str_DT is not None:
                                break
                        else:
                            raise "it.kindref must \"compound\" or \"member\""
                    else:
                        raise "<type> content error!"
                if str_DT is not None:
                    if type(str_DT) is clt.BuildIn:
                        # FIXME 此处应该构造clt.DDefine替代之前那的Define，但是暂时没找到怎么跟新所有关联引用的办法
                        # if type(self.curr_member_type) is clt.Define:
                        #     type_node = clt.DDefine(self.curr_member_type.sz_ELM_Name, str_DT, self.curr_member_type)
                        self.curr_member_type.stru_Def_TData = str_DT
                        self.curr_member_type.i_Def_Type = 3
                    else:
                        b_pointer = False
                        for it in node[1].init_fraction:
                            if type(it) is str:
                                if re.match('(( )*)\*(( )*)', it) is not None:
                                    b_pointer = True
                                    break
                        if b_pointer:
                            # FIXME 此处不应该新建类型，而是应该在全局的数据类型数据库拿
                            self.curr_member_type.stru_Def_TData = clt.DPointer(str_DT.sz_ELM_Name+' *', str_DT)
                        else:
                            self.curr_member_type.stru_Def_TData = str_DT
                else:
                    # FIXME 未知类型也应该建立索引
                    self.curr_member_type.stru_Def_TData = clt.TData(str(node[1].init_fraction), 0)
            pass
        elif tag == "type":
            if type(self.curr_member_type) is clt.Function:
                pass
            elif type(self.curr_member_type) is clt.Variable:
                node = self.stack_node.top()
                str_DT = None
                # 检测类型是否属于已建立索引的类型
                for it in node[1].type_fraction:
                    if type(it) is str:
                        szBuildinType = isBuildinType(it)
                        if szBuildinType is not None:
                            # FIXME c++ 内建数据类型应该有专门的数据库
                            str_DT = clt.BuildIn(it, szBuildinType)
                            break
                    elif type(it) is RefNode:
                        if it.kindref == 'compound':
                            str_DT = self.indx_handler.stru_xml.find(it.refid, 'compound')
                            if str_DT is not None:
                                break
                        elif it.kindref == 'member':
                            str_DT = self.indx_handler.stru_xml.assert_DDef(it.refid)
                            if str_DT is not None:
                                break
                            str_DT = self.indx_handler.stru_xml.assert_AN(it.refid)
                            if str_DT is not None:
                                break
                        else:
                            raise "it.kindref must \"compound\" or \"member\""
                    else:
                        raise "<type> content error!"
                if str_DT is not None:
                    if type(str_DT) is clt.BuildIn:
                        self.curr_member_type.stru_Var_TData = str_DT
                    else:
                        b_pointer = False
                        for it in node[1].type_fraction:
                            if type(it) is str:
                                if re.match('(( )*)\*(( )*)', it) is not None:
                                    b_pointer = True
                                    break
                        if b_pointer:
                            # FIXME 此处不应该新建类型，而是应该在全局的数据类型数据库拿
                            self.curr_member_type.stru_Var_TData = clt.DPointer(str_DT.sz_ELM_Name+' *', str_DT)
                        else:
                            self.curr_member_type.stru_Var_TData = str_DT
                else:
                    # FIXME 未知类型也应该建立索引
                    self.curr_member_type.stru_Var_TData = clt.TData(str(node[1].type_fraction), 0)
        elif tag == "ref":
            pass
        elif tag == "argsstring":
            pass
        elif tag == "param":
            # 把参数保存到ctl.Function中
            pass
        else:
            return
        self.stack_node.pop()

    # 内容事件处理
    def characters(self, content):
        node = self.stack_node.top()
        if node == None:
            return
        if node[0] == "compoundname":
            node[1].compoundname = content
        elif node[0] == "includes":
            if node[1].parent[0] != "compounddef":
                raise "root of <includes> must <compounddef>"
            node[1].parent[1].includes = content
        elif node[0] == "name":
            if self.curr_member_type.sz_ELM_Name != content:
                raise "self.curr_member_type.sz_ELM_Name must "+content
        elif node[0] == "initializer":
            node[1].init_fraction.append(content)
            pass
        elif node[0] == "type":
            node[1].type_fraction.append(content)
        elif node[0] == "ref":
            node[1].type_name = content
        elif node[0] == "argsstring":
            if type(self.curr_member_type) is clt.Variable:
                if re.match('\[.*\]', content):
                    sz_arrSize = content[1:len(content)-1]
                    # FIXME 此处应该增加确定 sz_arrSize 是否可检索
                    if issubclass(type(self.curr_member_type.stru_Var_TData), clt.TData):
                        self.curr_member_type.stru_Var_TData.sz_TD_ArrSize = sz_arrSize
                    elif type(self.curr_member_type.stru_Var_TData) is clt.AnotherName:
                        self.curr_member_type.stru_Var_TData.sz_TD_ArrSize = sz_arrSize
                    else:
                        raise "self.curr_member_type must a class of clt.TData or clt.AnotherName"
                else:
                    raise "<argsstring> content error!"
            elif type(self.curr_member_type) is clt.Function:
                if re.match('\(.*\)', content):
                    sz_Args = content[1:len(content)-1]
        elif node[0] == "declname":
            node[1]._name = content


class FDefFunHandler(sax.handler.ContentHandler):
    def __init__(self, _indx_handler):
        super(FDefFunHandler, self).__init__()
        self.stack_node = Stack()
        if type(_indx_handler) is not IndexHandler:
            raise "param \"_indx_handler\" must a instance of class IndexHandler"
        self.indx_handler = _indx_handler
        self.curr_section_node = None
        self.curr_member_node = None
        self.curr_member_type = None

    # 元素开始事件处理
    def startElement(self, tag, attributes):
        if tag == "doxygen":
            if not self.stack_node.is_empty():
                raise '<doxygen> must root node'
            self.stack_node.push([tag, XmlNode(tag, None)])
        elif tag == "compounddef":
            if not self.stack_node.top()[0] == "doxygen":
                raise '<compounddef> father must <doxygen>'
            node = ComDefNode(tag, self.stack_node.top(),attributes["id"], attributes["kind"],None)
            if attributes["kind"] in {'struct', 'class', 'union'}:
                raise '<compounddef>.kind must file'
            elif attributes["kind"] == 'file':
                pass
            self.stack_node.push([tag, node])
        elif tag == "compoundname":
            self.stack_node.push([tag, XmlNode(tag, self.stack_node.top())])
        elif tag == "sectiondef":
            node = SectionDefNode(tag, self.stack_node.top(), attributes["kind"])
            self.stack_node.push([tag, node])
            self.curr_section_node = node
        elif tag == "memberdef":
            if self.curr_section_node is None or self.curr_section_node.kind != "func":
                '''
                过滤非 func 模块
                '''
                return
            if attributes["kind"] != "function":
                raise '<compounddef>.kind must function'
            node = MemDefNode(tag, self.stack_node.top(),
                              attributes["kind"],
                              attributes["id"],
                              attributes["prot"],
                              attributes["static"])
            self.stack_node.push([tag, node])
            self.curr_member_node = self.stack_node.top()
            self.curr_member_type = self.indx_handler.stru_xml.find(attributes["id"], self.curr_section_node.kind)
            if self.curr_member_type is None:
                raise 'curr_member_type mustn\'t None'
        elif tag == "type":  # 解析的重点
            if self.curr_section_node is None or self.curr_section_node.kind != "func":
                '''
                过滤非 func 模块
                '''
                return
            self.stack_node.push([tag, TypeNode(tag, self.stack_node.top())])
        elif tag == "ref":  # 解析的重点
            if self.curr_section_node is None or self.curr_section_node.kind != "func":
                '''
                过滤非 func 模块
                '''
                return
            root = self.stack_node.top()
            node = None
            if root[1].parent[0] == "param" and root[0] == "type":
                node = RefNode(tag, self.stack_node.top(), attributes["refid"], attributes["kindref"])
                root[1].parent[1].param_type_fraction.append(node)
            elif root[0] == "type":
                node = RefNode(tag, self.stack_node.top(), attributes["refid"], attributes["kindref"])
                root[1].type_fraction.append(node)
            else:
                raise '<ref> parant must be <type> in section func'
            self.stack_node.push([tag, node])
        elif tag == "definition":
            if self.curr_section_node is None or self.curr_section_node.kind != "func":
                '''
                过滤非 func 模块
                '''
                return
            self.stack_node.push([tag, XmlNode(tag, self.stack_node.top())])
        elif tag == "argsstring":
            if self.curr_section_node is None or self.curr_section_node.kind != "func":
                '''
                过滤非 func 模块
                '''
                return
            self.stack_node.push([tag, XmlNode(tag, self.stack_node.top())])
        elif tag == "name":
            if self.curr_section_node is None or self.curr_section_node.kind != "func":
                '''
                过滤非 func 模块
                '''
                return
            self.stack_node.push([tag, XmlNode(tag, self.stack_node.top())])
        elif tag == "param":
            if self.curr_section_node is None or self.curr_section_node.kind != "func":
                '''
                过滤非 func 模块
                '''
                return
            self.stack_node.push([tag, ParamNode(tag, self.stack_node.top())])
        elif tag == "declname":
            if self.curr_section_node is None or self.curr_section_node.kind != "func":
                '''
                过滤非 func 模块
                '''
                return
            self.stack_node.push([tag, XmlNode(tag, self.stack_node.top())])
        elif tag == "array":
            if self.curr_section_node is None or self.curr_section_node.kind != "func":
                '''
                过滤非 func 模块
                '''
                return
            self.stack_node.push([tag, XmlNode(tag, self.stack_node.top())])
        else:
            return

    # 元素结束事件处理
    def endElement(self, tag):
        if tag == "doxygen":
            if self.stack_node.is_empty():
                #FIXME 节点元素入栈出栈顺序有问题！！！！！！！！！！！！！
                raise '</doxygen> must last node'
            pass
        elif tag == "compounddef":
            pass
        elif tag == "sectiondef":
            self.curr_section_node = None
            pass
        elif tag == "compoundname":
            pass
        elif tag == "memberdef":
            if self.curr_section_node is None or self.curr_section_node.kind != "func":
                '''
                过滤非 func 模块
                '''
                return
            # fixme 完成一个成员的初始化
            # self.curr_member_type = clt.BuildIn(node[1].name, szBuildinType)
            pass
        elif tag == "type":
            if self.curr_section_node is None or self.curr_section_node.kind != "func":
                '''
                过滤非 func 模块
                '''
                return
            if type(self.curr_member_type) is clt.Function:
                node = self.stack_node.top()
                str_DT = None
                # 检测类型是否属于已建立索引的类型
                for it in node[1].type_fraction:
                    if type(it) is str:
                        szBuildinType = isBuildinType(it)
                        if szBuildinType is not None:
                            # FIXME c++ 内建数据类型应该有专门的数据库
                            str_DT = clt.BuildIn(it, szBuildinType)
                            break
                    elif type(it) is RefNode:
                        if it.kindref == 'compound':
                            str_DT = self.indx_handler.stru_xml.find(it.refid, 'compound')
                            if str_DT is not None:
                                break
                        elif it.kindref == 'member':
                            str_DT = self.indx_handler.stru_xml.assert_DDef(it.refid)
                            if str_DT is not None:
                                break
                            str_DT = self.indx_handler.stru_xml.assert_AN(it.refid)
                            if str_DT is not None:
                                break
                        else:
                            raise "it.kindref must \"compound\" or \"member\""
                    else:
                        raise "<type> content error!"
                if str_DT is not None:
                    if type(str_DT) is clt.BuildIn:
                        node = self.stack_node.top()
                        if node[1].parent[0] == "param":
                            node[1].type_fraction.append(str_DT)
                        elif node[1].parent[0] == "memberdef":
                            self.curr_member_type.stru_Var_TData = str_DT
                        else:
                            raise '<ref> parant must be <type> in section func'
                    else:
                        b_pointer = False
                        for it in node[1].type_fraction:
                            if type(it) is str:
                                if re.match('(( )*)\*(( )*)', it) is not None:
                                    b_pointer = True
                                    break
                        if b_pointer:
                            # FIXME 此处不应该新建类型，而是应该在全局的数据类型数据库拿
                            node = self.stack_node.top()
                            if node[1].parent[0] == "param":
                                node[1].type_fraction.append(clt.DPointer(str_DT.sz_ELM_Name+' *', str_DT))
                            elif node[1].parent[0] == "memberdef":
                                self.curr_member_type.stru_Var_TData = clt.DPointer(str_DT.sz_ELM_Name+' *', str_DT)
                            else:
                                raise '<ref> parant must be <type> in section func'
                        else:
                            node = self.stack_node.top()
                            if node[1].parent[0] == "param":
                                node[1].type_fraction.append(str_DT)
                            elif node[1].parent[0] == "memberdef":
                                self.curr_member_type.stru_Var_TData = str_DT
                            else:
                                raise '<ref> parant must be <type> in section func'
                else:
                    # FIXME 未知类型也应该建立索引
                    self.curr_member_type.arr_Fn_args.append(clt.TData(str(node[1].type_fraction), 0))
        elif tag == "ref":
            if self.curr_section_node is None or self.curr_section_node.kind != "func":
                '''
                过滤非 func 模块
                '''
                return
            node = self.stack_node.top()
            if node[1].parent[1].parent[0] == "param" and node[1].parent[0] == "type":
                node[1].parent[1].type_fraction.append(node[1])
            elif node[1].parent[0] == "type":
                node[1].parent[1].type_fraction.append(node[1])
            else:
                raise '<ref> parant must be <type> in section func'

        elif tag == "definition":
            if self.curr_section_node is None or self.curr_section_node.kind != "func":
                '''
                过滤非 func 模块
                '''
                return
            pass
        elif tag == "argsstring":
            if self.curr_section_node is None or self.curr_section_node.kind != "func":
                '''
                过滤非 func 模块
                '''
                return
            pass
        elif tag == "name":
            if self.curr_section_node is None or self.curr_section_node.kind != "func":
                '''
                过滤非 func 模块
                '''
                return
            pass
        elif tag == "param":
            if self.curr_section_node is None or self.curr_section_node.kind != "func":
                '''
                过滤非 func 模块
                '''
                return
            pass
        elif tag == "declname":
            if self.curr_section_node is None or self.curr_section_node.kind != "func":
                '''
                过滤非 func 模块
                '''
                return
            pass
        elif tag == "array":
            if self.curr_section_node is None or self.curr_section_node.kind != "func":
                '''
                过滤非 func 模块
                '''
                return
            pass
        else:
            return
        self.stack_node.pop()

    # 内容事件处理
    def characters(self, content):
        node = self.stack_node.top()
        if node == None:
            return
        if node[0] == "name":
            if self.curr_section_node is None or self.curr_section_node.kind != "func":
                '''
                过滤非 func 模块
                '''
                return
            if self.curr_member_type.sz_ELM_Name != content:
                raise "self.curr_member_type.sz_ELM_Name must "+content
        elif node[0] == "type":
            if self.curr_section_node is None or self.curr_section_node.kind != "func":
                '''
                过滤非 func 模块
                '''
                return
            node[1].type_fraction.append(content)
        elif node[0] == "ref":
            if self.curr_section_node is None or self.curr_section_node.kind != "func":
                '''
                过滤非 func 模块
                '''
                return
            node[1].type_name = content
        elif node[0] == "argsstring":
            if self.curr_section_node is None or self.curr_section_node.kind != "func":
                '''
                过滤非 func 模块
                '''
                return
            if type(self.curr_member_type) is clt.Function:
                if re.match('\(.*\)', content):
                    self.curr_member_type.sz_ELM_Define = content[1:len(content)-1]
        elif node[0] == "declname":
            if self.curr_section_node is None or self.curr_section_node.kind != "func":
                '''
                过滤非 func 模块
                '''
                return
            node[1]._name = content
        elif node[0] == "array":
            if self.curr_section_node is None or self.curr_section_node.kind != "func":
                '''
                过滤非 func 模块
                '''
                return


ComDef_path = "D:\\3_test_program\\HCStructModel\\XmlModel3\\mode\\xml\\struct_n_e_t___d_v_r___e_t_h_e_r_n_e_t.xml"
def ComDef_execute(_path, index_handler):
    if type(index_handler) is not IndexHandler:
        raise "param index_handler must a class IndexHandler"
    # 创建一个 XMLReader
    parser = sax.make_parser()
    # turn off namepsaces
    parser.setFeature(sax.handler.feature_namespaces, 0)

    # 重写 ContextHandler
    Handler = ComDefHandler(index_handler)
    parser.setContentHandler(Handler)

    parser.parse(_path)
    return Handler

FileDef_path = "D:\\3_test_program\\HCStructModel\\XmlModel3\\mode\\xml\\test_8h.xml"
def FileDef_execute(_path, index_handler):
    if type(index_handler) is not IndexHandler:
        raise "param index_handler must a class IndexHandler"
    # 创建一个 XMLReader
    parser = sax.make_parser()
    # turn off namepsaces
    parser.setFeature(sax.handler.feature_namespaces, 0)

    # 重写 ContextHandler
    Handler = FileDefHandler(index_handler)
    parser.setContentHandler(Handler)

    parser.parse(_path)
    return Handler

def FileFnDef_execute(_path, index_handler):
    if type(index_handler) is not IndexHandler:
        raise "param index_handler must a class IndexHandler"
    # 创建一个 XMLReader
    parser = sax.make_parser()
    # turn off namepsaces
    parser.setFeature(sax.handler.feature_namespaces, 0)

    # 重写 ContextHandler
    Handler = FDefFunHandler(index_handler)
    parser.setContentHandler(Handler)

    parser.parse(_path)
    return Handler

if __name__ == "__main__":
    indx_handler = index_execute(index_path)
    # def_handler = ComDef_execute(ComDef_path, indx_handler)
    # def_handler = FileDef_execute(FileDef_path, indx_handler)
    def_handler = FileFnDef_execute(FileDef_path, indx_handler)
    pass



