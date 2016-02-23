
import ply.yacc as yacc
from pyfranca import franca_lexer
from pyfranca import ast


class Parser(object):
    """
    Franca IDL PLY parser.
    """

    # noinspection PyUnusedLocal,PyIncorrectDocstring
    @staticmethod
    def p_fidl_1(p):
        """
        fidl : fidl def
        """
        p[0] = p[1]
        p[0].append(p[2])

    # noinspection PyUnusedLocal,PyIncorrectDocstring
    @staticmethod
    def p_fidl_2(p):
        """
        fidl : def
        """
        p[0] = [p[1]]

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_package_def(p):
        """
        def : PACKAGE namespace
        """
        p[0] = p[2]

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_namespace_1(p):
        """
        namespace : ID '.' namespace
        """
        p[0] = "{}.{}".format(p[1], p[3])

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_namespace_2(p):
        """
        namespace : ID
        """
        p[0] = p[1]

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_namespace_3(p):
        """
        namespace : '*'
        """
        p[0] = p[1]

    # noinspection PyIncorrectDocstring
    # TODO: Support for "import model"
    @staticmethod
    def p_import_def(p):
        """
        def : IMPORT namespace FROM FILE_NAME
        """
        p[0] = ast.Import(p[4], p[2])

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_type_collection_1(p):
        """
        def : TYPECOLLECTION ID '{' version_def type_collection_members '}'
        """
        p[0] = ast.TypeCollection(p[2], p[4], p[5])

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_type_collection_2(p):
        """
        def : TYPECOLLECTION ID '{' type_collection_members '}'
        """
        p[0] = ast.TypeCollection(p[2], None, p[4])

    # noinspection PyUnusedLocal, PyIncorrectDocstring
    @staticmethod
    def p_type_collection_members_1(p):
        """
        type_collection_members : type_collection_members type_collection_member
        """
        p[0] = p[1]
        p[0].append(p[2])

    # noinspection PyUnusedLocal, PyIncorrectDocstring
    @staticmethod
    def p_type_collection_members_2(p):
        """
        type_collection_members : type_collection_member
        """
        p[0] = [p[1]]

    # noinspection PyUnusedLocal, PyIncorrectDocstring
    @staticmethod
    def p_type_collection_members_3(p):
        """
        type_collection_members : empty
        """
        pass

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_type_collection_member_2(p):
        """
        type_collection_member : type_def
                               | enumeration_def
                               | struct_def
        """
        p[0] = p[1]

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_version_def(p):
        """
        version_def : VERSION '{' MAJOR INTEGER MINOR INTEGER '}'
        """
        p[0] = ast.Version(p[4], p[6])

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_type_def_1(p):
        """
        type_def : TYPEDEF ID IS ID
        """
        base_type = ast.CustomType(p[4])
        p[0] = ast.Typedef(p[2], base_type)

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_type_def_2(p):
        """
        type_def : TYPEDEF ID IS type
        """
        p[0] = ast.Typedef(p[2], p[4])

    # noinspection PyIncorrectDocstring
    # TODO: support for "extends"
    # TODO: "interface elements can be arranged freely"
    @staticmethod
    def p_interface(p):
        """
        def : INTERFACE ID '{' \
                version_def \
                attribute_defs \
                method_defs \
                broadcast_defs \
                enumeration_defs \
              '}'
        """
        p[0] = ast.Interface(p[2], p[4], p[5], p[6], p[7])

    # noinspection PyUnusedLocal, PyIncorrectDocstring
    @staticmethod
    def p_attribute_defs_1(p):
        """
        attribute_defs : attribute_defs attribute_def
        """
        p[0] = p[1]
        p[0].append(p[2])

    # noinspection PyUnusedLocal, PyIncorrectDocstring
    @staticmethod
    def p_attribute_defs_2(p):
        """
        attribute_defs : attribute_def
        """
        p[0] = [p[1]]

    # noinspection PyUnusedLocal, PyIncorrectDocstring
    @staticmethod
    def p_attribute_defs_3(p):
        """
        attribute_defs : empty
        """
        pass

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_attribute_def_1(p):
        """
        attribute_def : ATTRIBUTE type ID
        """
        p[0] = ast.Attribute(p[3], p[2])

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_attribute_def_2(p):
        """
        attribute_def : ATTRIBUTE ID ID
        """
        attr_type = ast.CustomType(p[3])
        p[0] = ast.Attribute(p[3], attr_type)

    # noinspection PyUnusedLocal, PyIncorrectDocstring
    @staticmethod
    def p_method_defs_1(p):
        """
        method_defs : method_defs method_def
        """
        p[0] = p[1]
        p[0].append(p[2])

    # noinspection PyUnusedLocal, PyIncorrectDocstring
    @staticmethod
    def p_method_defs_2(p):
        """
        method_defs : method_def
        """
        p[0] = [p[1]]

    # noinspection PyUnusedLocal, PyIncorrectDocstring
    @staticmethod
    def p_method_defs_3(p):
        """
        method_defs : empty
        """
        pass

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_method_def_1(p):
        """
        method_def : METHOD ID '{' '}'
        """
        p[0] = ast.Method(p[2])

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_method_def_2(p):
        """
        method_def : METHOD ID '{' \
                        IN '{' arg_defs '}' \
                     '}'
        """
        p[0] = ast.Method(p[2], p[6])

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_method_def_3(p):
        """
        method_def : METHOD ID '{' \
                        OUT '{' arg_defs '}' \
                     '}'
        """
        p[0] = ast.Method(p[2], [], p[6])

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_method_def_4(p):
        """
        method_def : METHOD ID '{' \
                        IN '{' arg_defs '}' \
                        OUT '{' arg_defs '}' \
                     '}'
        """
        p[0] = ast.Method(p[2], p[6], p[10])

    # noinspection PyUnusedLocal, PyIncorrectDocstring
    @staticmethod
    def p_broadcast_defs_1(p):
        """
        broadcast_defs : broadcast_defs broadcast_def
        """
        p[0] = p[1]
        p[0].append(p[2])

    # noinspection PyUnusedLocal, PyIncorrectDocstring
    @staticmethod
    def p_broadcast_defs_2(p):
        """
        broadcast_defs : broadcast_def
        """
        p[0] = [p[1]]

    # noinspection PyUnusedLocal, PyIncorrectDocstring
    @staticmethod
    def p_broadcast_defs_3(p):
        """
        broadcast_defs : empty
        """
        pass

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_broadcast_def(p):
        """
        broadcast_def : BROADCAST ID '{' \
                            OUT '{' arg_defs '}' \
                        '}'
        """
        p[0] = ast.Broadcast(p[2], p[6])

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_arg_defs_1(p):
        """
        arg_defs : arg_defs arg_def
        """
        p[0] = p[1]
        p[0].append(p[2])

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_arg_defs_2(p):
        """
        arg_defs : arg_def
        """
        p[0] = [p[1]]

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_arg_def_1(p):
        """
        arg_def : type ID
        """
        p[0] = ast.Argument(p[2], p[1])

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_arg_def_2(p):
        """
        arg_def : ID ID
        """
        arg_type = ast.CustomType(p[1])
        p[0] = ast.Argument(p[2], arg_type)

    # noinspection PyUnusedLocal, PyIncorrectDocstring
    @staticmethod
    def p_enumeration_defs_1(p):
        """
        enumeration_defs : enumeration_defs enumeration_def
        """
        p[0] = p[1]
        p[0].append(p[2])

    # noinspection PyUnusedLocal, PyIncorrectDocstring
    @staticmethod
    def p_enumeration_defs_2(p):
        """
        enumeration_defs : enumeration_def
        """
        p[0] = [p[1]]

    # noinspection PyUnusedLocal, PyIncorrectDocstring
    @staticmethod
    def p_enumeration_defs_3(p):
        """
        enumeration_defs : empty
        """
        pass

    # noinspection PyUnusedLocal, PyIncorrectDocstring
    @staticmethod
    def p_enumeration_def_1(p):
        """
        enumeration_def : ENUMERATION ID '{' enumerators '}'
        """
        # TODO: Enumberator values
        p[0] = ast.Enumeration(p[2], p[4])

    # noinspection PyUnusedLocal, PyIncorrectDocstring
    @staticmethod
    def p_enumeration_def_2(p):
        """
        enumeration_def : ENUMERATION ID EXTENDS ID '{' enumerators '}'
        """
        # TODO: Enumberator values
        p[0] = ast.Enumeration(p[2], p[6], p[4])

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_enumerators_1(p):
        """
        enumerators : enumerators enumerator
        """
        p[0] = p[1]
        p[0].append(p[2])

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_enumerators_2(p):
        """
        enumerators : enumerator
        """
        p[0] = [p[1]]

    # noinspection PyUnusedLocal, PyIncorrectDocstring
    @staticmethod
    def p_enumerators_3(p):
        """
        enumerators : empty
        """
        pass

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_enumerator_1(p):
        """
        enumerator : ID
        """
        p[0] = ast.Enumerator(p[1], None)

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_enumerator_2(p):
        """
        enumerator : ID '=' INTEGER
        """
        p[0] = ast.Enumerator(p[1], p[3])

    # noinspection PyUnusedLocal, PyIncorrectDocstring
    @staticmethod
    def p_struct_def_1(p):
        """
        struct_def : STRUCT ID '{' struct_fields '}'
        """
        p[0] = ast.Struct(p[2], p[4])

    # noinspection PyUnusedLocal, PyIncorrectDocstring
    @staticmethod
    def p_struct_def_2(p):
        """
        struct_def : STRUCT ID EXTENDS ID '{' struct_fields '}'
        """
        p[0] = ast.Struct(p[2], p[6], p[4])

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_struct_fields_1(p):
        """
        struct_fields : struct_fields struct_field
        """
        p[0] = p[1]
        p[0].append(p[2])

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_struct_fields_2(p):
        """
        struct_fields : struct_field
        """
        p[0] = [p[1]]

    # noinspection PyUnusedLocal, PyIncorrectDocstring
    @staticmethod
    def p_struct_fields_3(p):
        """
        struct_fields : empty
        """
        pass

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_struct_field_1(p):
        """
        struct_field : type ID
        """
        p[0] = ast.StructField(p[2], p[1])

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_struct_field_2(p):
        """
        struct_field : ID ID
        """
        filed_type = ast.CustomType(p[1])
        p[0] = ast.StructField(p[2], filed_type)

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_type(p):
        """
        type : INT8
             | INT16
             | INT32
             | INT64
             | UINT8
             | UINT16
             | UINT32
             | UINT64
             | BOOLEAN
             | FLOAT
             | DOUBLE
             | STRING
             | BYTEBUFFER
        """
        type_class = getattr(ast, p[1])
        p[0] = type_class()

    # noinspection PyUnusedLocal, PyIncorrectDocstring
    @staticmethod
    def p_empty(p):
        """
        empty :
        """
        pass

    # noinspection PyIncorrectDocstring
    @staticmethod
    def p_error(p):
        # TODO: How to handle errors?
        print("Syntax error at line {} near '{}'".format(p.lineno, p.value))

    def __init__(self, the_lexer=None, **kwargs):
        """
        Constructor.

        :param lexer: a lexer object to use.
        """
        if not the_lexer:
            the_lexer = franca_lexer.Lexer()
        self._lexer = the_lexer
        self.tokens = self._lexer.tokens
        # Disable debugging, by default.
        if "debug" not in kwargs:
            kwargs["debug"] = False
        if "write_tables" not in kwargs:
            kwargs["write_tables"] = False
        self._parser = yacc.yacc(module=self, **kwargs)

    def parse(self, data):
        """
        Parse input text

        :param data: Input text to parse.
        :return:
        """
        return self._parser.parse(data)
