# -*-encoding=utf-8-*-

import xml.sax as sax
from metadata.tools import *


class IndexXml:
    tuple_type = {
        'all',
        'compound', 'define',
        'enum', 'typedef',
        'var', 'func',
    }

    def __init__(self):
        self.arr_compound = []
        self.arr_define = []
        self.arr_enum = []
        self.arr_typedef = []
        self.arr_variable = []
        self.arr_function = []

    def find_by_name(self, _name, _type='all'):
        if _type not in self.tuple_type:
            raise "searching _type must in {'all' 'compound' 'define' 'enum' 'typedef' 'var' 'func'}"
        if _type == 'all':
            stru_elem = self.find_by_name(_name, 'compound')
            if stru_elem is not None:
                return stru_elem
            stru_elem = self.find_by_name(_name, 'define')
            if stru_elem is not None:
                return stru_elem
            stru_elem = self.find_by_name(_name, 'enum')
            if stru_elem is not None:
                return stru_elem
            stru_elem = self.find_by_name(_name, 'typedef')
            if stru_elem is not None:
                return stru_elem
            stru_elem = self.find_by_name(_name, 'var')
            if stru_elem is not None:
                return stru_elem
            stru_elem = self.find_by_name(_name, 'func')
            if stru_elem is not None:
                return stru_elem
        elif _type == 'compound':
            for it in self.arr_compound:
                if it.sz_ELM_Name == _name:
                    return it
        elif _type == 'define':
            for it in self.arr_define:
                if it.sz_ELM_Name == _name:
                    return it
        elif _type == 'enum':
            for it in self.arr_enum:
                if it.sz_ELM_Name == _name:
                    return it
        elif _type == 'typedef':
            for it in self.arr_typedef:
                if it.sz_ELM_Name == _name:
                    return it
        elif _type == 'var':
            for it in self.arr_variable:
                if it.sz_ELM_Name == _name:
                    return it
        elif _type == 'func':
            for it in self.arr_function:
                if it.sz_ELM_Name == _name:
                    return it
        else:
            return None
        pass

    def find(self, _refid, _type='all'):
        if _type not in self.tuple_type:
            raise "searching _type must in {'all' 'compound' 'define' 'enum' 'typedef' 'var' 'func'}"
        if _type == 'all':
            stru_elem = self.find(_refid, 'compound')
            if stru_elem is not None:
                return stru_elem
            stru_elem = self.find(_refid, 'define')
            if stru_elem is not None:
                return stru_elem
            stru_elem = self.find(_refid, 'enum')
            if stru_elem is not None:
                return stru_elem
            stru_elem = self.find(_refid, 'typedef')
            if stru_elem is not None:
                return stru_elem
            stru_elem = self.find(_refid, 'var')
            if stru_elem is not None:
                return stru_elem
            stru_elem = self.find(_refid, 'func')
            if stru_elem is not None:
                return stru_elem
        elif _type == 'compound':
            for it in self.arr_compound:
                if it.sz_XFile_refid == _refid:
                    return it
        elif _type == 'define':
            for it in self.arr_define:
                if it.sz_Def_refid == _refid:
                    return it
        elif _type == 'enum':
            for it in self.arr_enum:
                if it.sz_Enum_refid == _refid:
                    return it
        elif _type == 'typedef':
            for it in self.arr_typedef:
                if it.sz_AN_refid == _refid:
                    return it
        elif _type == 'var':
            for it in self.arr_variable:
                if it.sz_Var_refid == _refid:
                    return it
        elif _type == 'func':
            for it in self.arr_function:
                if it.sz_Fn_refid == _refid:
                    return it
        else:
            return None

    def assert_DDef(self, _refid):
        """
        确定宏是否是数据类型宏
        :param _refid: 检索id
        :return:
        """
        stru_Def = self.find(_refid, "define")
        if type(stru_Def) is clt.Define:
            if stru_Def.i_Def_Type == 0:
                # TODO: 说明当前宏类型未知，需要递归确定宏类型（方法是查找file.xml文件）
                return stru_Def
            else:
                return None
        elif type(stru_Def) is clt.DDefine:
            return stru_Def
        else:
            return None

    def assert_AN(self, _refid):
        stru_AN = self.find(_refid, "typedef")
        if stru_AN.stru_AN_DT is None:
            # FIXME: 确定别名类型，到底是类型的别名还是，函数指针
            return stru_AN
        else:
            return stru_AN


class XmlNode:
    def __init__(self, _name, _parent=None):
        self.name = _name
        self.parent = _parent


class ComNode(XmlNode):
    def __init__(self, _name, _parent, _refid, _kind):
        super(ComNode, self).__init__(_name)
        self.szDType = ''
        self.refid = _refid
        self.kind = _kind


class MemberNode(XmlNode):
    def __init__(self, _name, _parent, _refid, _kind):
        super(MemberNode, self).__init__(_name)
        self.refid = _refid
        self.kind = _kind


class IndexHandler(sax.handler.ContentHandler):
    def __init__(self):
        super(IndexHandler, self).__init__()
        self.__b_ok = False
        self.stru_xml = IndexXml()
        self.stack_node = Stack()
        self.loc_com_node = None  # 当前<compound>
        self.__sz_node_text = ""  # 缓存当前节点正文

    def isOK(self):
        return self.__b_ok

    def setOK(self, _b_ok=True):
        self.__b_ok = _b_ok

    def startElement(self, tag, attributes):
        """
        元素开始事件处理
        :param tag: 节点名
        :param attributes: 属性字典
        :return: None
        """
        if tag == "doxygenindex":
            # index.xml 起始节点 <doxygenindex> 处理
            if not self.stack_node.is_empty():
                raise '<doxygenindex> must root node'
            self.stack_node.push([tag, XmlNode('', None)])
        elif tag == "compound":
            # 复合xml节点<compound>...</compound>
            if not self.stack_node.top()[0] == "doxygenindex":
                raise '<compound> father must <doxygenindex>'
            self.__proc_start_compound(tag, attributes)
            self.loc_com_node = self.stack_node.top()
        elif tag == "name":
            # <name> 节点起始事件处理
            self.__proc_start_name(tag, attributes)
            self.__sz_node_text = ''
        elif tag == 'member':
            # <member> 节点起始事件处理（重要）
            self.__proc_start_member(tag, attributes)

    def endElement(self, tag):
        """
        元素结束事件处理
        :param tag:
        :return:
        """
        if tag == "doxygenindex":
            if self.stack_node.is_empty():
                raise '<doxygenindex> must last node'
            self.stack_node.pop()
        elif tag == "compound":
            self.__proc_end_compound(tag)
        elif tag == "name":
            node = self.stack_node.top()
            self.__proc_char_name(node, self.__sz_node_text)  # [code_mark-1]
            self.__proc_end_name(tag)
        elif tag == 'member':
            self.__proc_end_member(tag)

    def characters(self, content):
        """
        节点内容事件处理
        :param content:
        :return:
        """
        node = self.stack_node.top()
        if node[0] == "name":
            '''
            FIXED: 直接在characters()方法中处理节点中的文本内容，可能引起节点内容获取不全的问题
            原因: xml.sax方法解析xml文件时，是顺序读入文件，当遇到节点开头则调用startElement(), 遇到节点正文则调用characters(),
                 而遇到节点结束则调用endElement()方法。当xml文件特别大时，一次读入的文件长度有限，很可能没有将当前节点的正文读全，此时
                 当前节点的正文会分多次由characters()回调给用户，因此处理节点文本的工作最好在当前节点结束时再做处理，以保证对正文处理的完整性
            解决: __proc_char_name() 放到endElement中[code_mark-1]处调用
            '''
            # __proc_char_name(node, content)
            self.__sz_node_text = self.__sz_node_text + content
        pass

    def __proc_start_compound(self, tag, attributes):
        """
        复合xml节点<compound>...</compound>开始事件处理
        :param tag:
        :param attributes:
        :return:
        """
        if attributes['kind'] == 'struct' \
                or attributes['kind'] == 'class' \
                or attributes['kind'] == 'union':
            # 特殊处理，目前不需要
            pass
        # 构造一个xml复合节点对象。索引文件中每一类语义元素都包含在同一个复合节点下
        node = ComNode(tag, self.stack_node.top(), attributes['refid'], attributes['kind'])
        self.stack_node.push([tag, node])
        pass

    def __proc_start_name(self, tag, attributes):
        parent = self.stack_node.top()
        if parent[0] == 'compound':
            if parent[1].kind == 'struct' \
                    or parent[1].kind == 'class' \
                    or parent[1].kind == 'union':
                pass  # 特殊处理
            elif parent[1].kind == 'file':
                pass  # 特殊处理
            elif parent[1].kind == 'dir':
                pass  # 特殊处理
            else:
                raise '<name> kind must in {struct class union file dir}'
        elif parent[0] == 'member' \
                and self.loc_com_node[1].kind == 'file':
            pass  # 特殊处理

        node = XmlNode(tag, self.stack_node.top())
        self.stack_node.push([tag, node])
        pass

    def __proc_start_member(self, tag, attributes):
        parent = self.stack_node.top()
        if parent[1].kind == 'struct' \
                or parent[1].kind == 'class' \
                or parent[1].kind == 'union':
            pass  # 特殊处理
        elif parent[1].kind == 'file':
            pass  # 特殊处理

        node = MemberNode(tag, parent, attributes['refid'], attributes['kind'])
        self.stack_node.push([tag, node])

    def __proc_end_compound(self, tag):
        if self.stack_node.top()[0] != "compound" \
                and self.loc_com_node == self.stack_node.top()[1] \
                and self.loc_com_node.parent[0] == "doxygenindex":
            raise '<compound> father must <doxygenindex>'

        # print('</compound> ' + self.loc_com_node[1].kind)
        self.stack_node.pop()
        self.loc_com_node = None
        pass

    def __proc_end_name(self, tag):
        if self.stack_node.top()[1].parent[0] == "compound":
            pass  # 特殊处理
        elif self.stack_node.top()[1].parent[0] == "member":
            pass  # 特殊处理
        else:
            raise '<name> father must <compound> or <member>'

        self.stack_node.pop()

    def __proc_end_member(self, tag):
        self.stack_node.pop()

    def __proc_char_name(self, node, content):
        if node[1] is not None \
                and node[1].parent is not None \
                and (self.loc_com_node[1].kind == 'struct' \
                     or self.loc_com_node[1].kind == 'class' \
                     or self.loc_com_node[1].kind == 'union'):
            if node[1].parent[0] == 'compound':
                node[1].parent[1].szDType = content
                if self.loc_com_node[1].kind == 'struct':
                    stru_com = clt.Compound(content, 1)
                elif self.loc_com_node[1].kind == 'class':
                    stru_com = clt.Compound(content, 2)
                elif self.loc_com_node[1].kind == 'union':
                    stru_com = clt.Compound(content, 3)
                else:
                    raise '<name> father <compound> kind must in {struct class union}'
                stru_com.sz_XFile_refid = self.loc_com_node[1].refid
                self.stru_xml.arr_compound.append(stru_com)
            elif node[1].parent[0] == 'member':
                # if content == "wAlarmTyp":
                #     pass
                stru_com = self.stru_xml.arr_compound[len(self.stru_xml.arr_compound) - 1]
                if self.loc_com_node[1].szDType == stru_com.sz_ELM_Name:
                    if node[1].parent[1].kind == 'variable':
                        stru_var = clt.Variable(content)
                        stru_var.sz_XFile_refid = self.loc_com_node[1].refid
                        stru_var.sz_Var_refid = node[1].parent[1].refid
                        stru_com.arr_Com_members.append(stru_var)
                    elif node[1].parent[1].kind == 'function':
                        stru_fun = clt.Function(content)
                        stru_fun.sz_XFile_refid = self.loc_com_node[1].refid
                        stru_fun.sz_Fn_refid = node[1].parent[1].refid
                        stru_com.arr_Com_members.append(stru_fun)
                    pass
                pass
            else:
                raise '<name> father must <compound> or <member>'
        elif node[1] is not None \
                and node[1].parent is not None \
                and self.loc_com_node[1].kind == 'file':
            if node[1].parent[0] == 'compound':
                pass
            elif node[1].parent[0] == 'member':
                if node[1].parent[1].kind == 'define':
                    stru_def = clt.Define(content)
                    stru_def.sz_XFile_refid = self.loc_com_node[1].refid
                    stru_def.sz_Def_refid = node[1].parent[1].refid
                    self.stru_xml.arr_define.append(stru_def)
                elif node[1].parent[1].kind == 'enum':
                    stru_enum = clt.Enum(content)
                    stru_enum.sz_XFile_refid = self.loc_com_node[1].refid
                    stru_enum.sz_Enum_refid = node[1].parent[1].refid
                    self.stru_xml.arr_enum.append(stru_enum)
                elif node[1].parent[1].kind == 'enumvalue':
                    stru_enumor = clt.Enumerator(content)
                    stru_enumor.sz_XFile_refid = self.loc_com_node[1].refid
                    stru_enumor.sz_Enumor_refid = node[1].parent[1].refid
                    self.stru_xml.arr_enum[len(self.stru_xml.arr_enum) - 1].arr_Enum_members.append(stru_enumor)
                elif node[1].parent[1].kind == 'typedef':
                    # FIXME 需要区分重命名类型和函数指针
                    stru_typedef = clt.AnotherName(content)
                    stru_typedef.sz_XFile_refid = self.loc_com_node[1].refid
                    stru_typedef.sz_AN_refid = node[1].parent[1].refid
                    self.stru_xml.arr_typedef.append(stru_typedef)
                elif node[1].parent[1].kind == 'variable':
                    stru_var = clt.Variable(content)
                    stru_var.sz_XFile_refid = self.loc_com_node[1].refid
                    stru_var.sz_Var_refid = node[1].parent[1].refid
                    self.stru_xml.arr_variable.append(stru_var)
                elif node[1].parent[1].kind == 'function':
                    stru_fun = clt.Function(content)
                    stru_fun.sz_XFile_refid = self.loc_com_node[1].refid
                    stru_fun.sz_Fn_refid = node[1].parent[1].refid
                    self.stru_xml.arr_function.append(stru_fun)
                else:
                    raise '<name> father <member> kind must in {define enum enumvalue typedef variable function}'
            else:
                raise '<name> father must <member> in <compound> \'file\''


# index_path = "D:\\3_test_program\\HCStructModel\\XmlModel\\xml\\index.xml"
def index_execute(_path):
    print("**** start indexing ***")
    # 创建一个 XMLReader
    parser = sax.make_parser()
    # turn off namepsaces
    parser.setFeature(sax.handler.feature_namespaces, 0)

    # 重写 ContextHandler
    Handler = IndexHandler()
    parser.setContentHandler(Handler)

    parser.parse(_path)
    Handler.setOK()
    print("*** indexing finished ***\n")
    return Handler


if (__name__ == "__main__"):
    handler = index_execute(index_path)
    pass
