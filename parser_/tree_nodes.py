class ProgramASTs(list):
        """An outer class to hold all the ASTs making up a program."""
        def __init__(self):
                """Initialises the current indent to 0."""

        def __str__(self):
                """Prints out the ASTs in a nice way."""
                out = ''
                for ast in self.__iter__():
                        try:
                                name = ast.children[0].value
                                out += '### AST: ' + name + ' ###\r\n'
                        except AttributeError:
                                pass
                        out += self._print_ast(ast, 0)
                return out

        def _print_ast(self, node, indent):
                """Print out an AST in pre order."""
                # Add tabs
                out = ''
                for _ in range(indent):
                        out += '\t'
                # Build up string to print
                node_str = 'NODE: ' + str(node)
                val_str = 'VALUE: ' + str(node.value)
                type_str = 'TYPE: ' + str(node._type)
                out +=  node_str + ' | ' + val_str + ' | ' + type_str + '\r\n'
                try:
                        # Increase the indentation and print the child nodes
                        indent += 1
                        for child in node.children:
                                out += self._print_ast(child, indent)
                except AttributeError:
                        # It's a child node
                        pass
                return out

class TreeNode(object):
        """A generic tree node class which holds what node_id the node is."""
        def __init__(self, value = ''):
                """Initialise with a node_id, e.g. "int" for an integer node."""
                self._value = value
                self._type = ''

        def _get_value(self):
                return self._value

        def _get_type(self):
                return self._type

        def _set_type(self, type_):
                self._type = type_

        value = property(_get_value)
        type_ = property(_get_type, _set_type)

class InteriorNode(TreeNode):
        """An interior node of the AST tree."""
        def __init__(self, value = ''):
                """Initialise with a node_id."""
                super(InteriorNode, self).__init__(value)
                self._children = []

        def add_child(self, child):
                """Add a child to the list of child nodes."""
                self._children.append(child)

        def add_children(self, children):
                self._children += children

        def _get_children(self):
                """Get all the child nodes."""
                return self._children

        children = property(_get_children)

class NodeWithModifiers(InteriorNode):
        """A node with modifiers, such as static, final etc.
        The modifiers parameter is a list of these modifiers.
        """
        def __init__(self):
                """Initialise the modifiers."""
                super(NodeWithModifiers, self).__init__()
                self._modifiers = []
        
        def _get_modifiers(self):
                return self._modifiers
        
        def _set_modifiers(self, modifiers):
                self._modifiers = modifiers
        
        modifiers = property(_get_modifiers, _set_modifiers)

class ClassNode(NodeWithModifiers):         
        def __str__(self):
                return 'Class Node'

class InterfaceNode(InteriorNode):
        def __str__(self):
                return 'Interface Node'

class ImplementsListNode(InteriorNode):
        def __str__(self):
                return 'Implements List Node'

class ClassBodyNode(InteriorNode):
        def __str__(self):
                return 'Class Body Node'

class InterfaceBodyNode(InteriorNode):
        def __str__(self):
                return 'Interface Body Node'

class ClassAttributeNode(NodeWithModifiers):
        """Class attributes are field, constructors and methods.  They need to
        implement the __lt__ method, so that they can be sorted in such a way
        that they are in the same order as mentioned above.
        """
        def __init__(self, order):
                super(ClassAttributeNode, self).__init__()
                self._order = order
        
        def __lt__(self, other):
                return self._order < other.order
        
        def _get_order(self):
                return self._order
        
        order = property(_get_order)

class FieldDclNode(ClassAttributeNode):
        def __init__(self):
                """Set the order to 0 - appears first."""
                super(FieldDclNode, self).__init__(0)
                
        def __str__(self):
                return 'Field Declaration Node'

class FieldDclAssignNode(ClassAttributeNode):
        def __init__(self):
                """Set the order to 0 - appears first."""
                super(FieldDclAssignNode, self).__init__(0)
                
        def __str__(self):
                return 'Field Declaration Node, of Array Type'

class ConstructorDclNode(ClassAttributeNode):
        def __init__(self):
                """Set the order to 1 - appears second."""
                super(ConstructorDclNode, self).__init__(1)
        
        def __str__(self):
                return 'Constructor Declaration Node'

class MethodDclNode(ClassAttributeNode):
        def __init__(self):
                """Set the order to 2 - appears last."""
                super(MethodDclNode, self).__init__(2)
                
        def __str__(self):
                return 'Method Declaration Node'

class MethodDclArrayNode(ClassAttributeNode):
        def __init__(self):
                """Set the order to 2 - appears last."""
                super(MethodDclArrayNode, self).__init__(2)
                
        def __str__(self):
                return 'Method Declaration (Returns Array) Node'

class AbsMethodDclNode(InteriorNode):
        def __str__(self):
                return 'Abstract Method Declaration Node'

class AbsMethodDclArrayNode(InteriorNode):
        def __str__(self):
                return 'Abstract Method Declaration (Returns Array) Node'

class ParamListNode(InteriorNode):
        def __str__(self):
                return 'Parameters List Node'

class ParamDclNode(InteriorNode):
        def __str__(self):
                return 'Parameter Declaration Node'

class BlockNode(InteriorNode):
        def __str__(self):
                return 'Block Node'

class VarDclNode(InteriorNode):
        def __str__(self):
                return 'Variable Declaration Node'

class VarDclAssignNode(InteriorNode):
        def __str__(self):
                return 'Variable Declaration with Assignment Node'

class IfNode(InteriorNode):
        def __str__(self):
                return 'If Node'

class WhileNode(InteriorNode):
        def __str__(self):
                return 'While Node'

class ForNode(InteriorNode):
        def __str__(self):
                return 'For Node'

class ReturnNode(InteriorNode):
        def __str__(self):
                return 'Return Node'

class AssignNode(InteriorNode):
        def __str__(self):
                return 'Assignment Node'

class CondNode(InteriorNode):
        def __str__(self):
                return 'Conditional Expression Node'

class EqNode(InteriorNode):
        def __str__(self):
                return 'Equality Expression Node'

class RelNode(InteriorNode):
        def __str__(self):
                return 'Relational Expression Node'

class AddNode(InteriorNode):
        def __str__(self):
                return 'Addition/Subtraction Node'

class MulNode(InteriorNode):
        def __str__(self):
                return 'Multiplication/Division Node'

class NotNode(InteriorNode):
        def __str__(self):
                return 'Boolean Not Node'

class PosNode(InteriorNode):
        def __str__(self):
                return 'Positive/Negative Node'

class IncNode(InteriorNode):
        def __str__(self):
                return 'Increment/Decrement Node'

class ArrayDclNode(InteriorNode):
        def __str__(self):
                return 'Array Declaration Node'

class ArrayElementNode(InteriorNode):
        def __str__(self):
                return 'Array Element Node'

class MethodCallNode(InteriorNode):
        def __str__(self):
                return 'Method Call Node'

class MethodCallLongNode(InteriorNode):
        def __str__(self):
                return 'Method Call Long Node'

class MethodCallThisNode(InteriorNode):
        def __str__(self):
                return 'Method Call to "this" Node'

class MethodCallSuperNode(InteriorNode):
        def __str__(self):
                return 'Method Call to "super" Node'

class SuperConstructorCallNode(InteriorNode):
        def __str__(self):
                return 'Call to "supers" Constructor'

class FieldRefNode(InteriorNode):
        def __str__(self):
                return 'Reference to a field'

class FieldRefSuperNode(InteriorNode):
        def __str__(self):
                return 'Reference to a field of the Super Class'

class ArgsListNode(InteriorNode):
        def __str__(self):
                return 'Arguments List Node'

class ObjectCreatorNode(InteriorNode):
        def __str__(self):
                return 'Object Creator Node'

class ArrayInitNode(InteriorNode):
        def __str__(self):
                return 'Array Initialisation Node'

class LeafNode(TreeNode): pass


class ExtendsNode(LeafNode):
        def __str__(self):
                return 'Extends Node'

class ImplementsNode(LeafNode):
        def __str__(self):
                return 'Implements Node'

class IdNode(LeafNode):
        def __str__(self):
                return 'Identifier Node'

class ArrayIdNode(LeafNode):
        def __str__(self):
                return 'Array Identifier Node'

class DimensionsNode(LeafNode):
        def __str__(self):
                return 'Array Dimensions Node'

class TypeNode(LeafNode):
        def __str__(self):
                return 'Type Node'

class ClassTypeNode(LeafNode):
        def __str__(self):
                return 'Class Type Node'

class ReturnVoidNode(LeafNode):
        def __str__(self):
                return 'Return Void Node'

class EmptyNode(LeafNode):
        def __str__(self):
                return 'Empty Node'

class LiteralNode(LeafNode): pass

class StringLNode(LiteralNode):
        def __str__(self):
                return 'String Literal Node'

class CharLNode(LiteralNode):
        def __str__(self):
                return 'Char Literal Node'

class IntLNode(LiteralNode):
        def __str__(self):
                return 'Int Literal Node'

class LongLNode(LiteralNode):
        def __str__(self):
                return 'Long Literal Node'

class FloatLNode(LiteralNode):
        def __str__(self):
                return 'Float Literal Node'

class DoubleLNode(LiteralNode):
        def __str__(self):
                return 'Double Literal Node'

class BooleanLNode(LiteralNode):
        def __str__(self):
                return 'Boolean Literal Node'

class NullLNode(LiteralNode):
        def __str__(self):
                return 'Null Literal Node'

def create_bin_node(parent, l_child, r_child):
        """Provides a convenient way of creating interior nodes with two child
        nodes.
        """
        parent.add_child(l_child)
        parent.add_child(r_child)
        return parent

def create_array_dcl(name, dimensions):
        """Used to quickly create an array leaf node with node_id, value and
        dimensions.
        """
        node = ArrayDclNode()
        node.add_child(ArrayIdNode(name))
        node.add_child(DimensionsNode(dimensions))
        return node