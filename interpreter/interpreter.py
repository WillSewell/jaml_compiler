"""An interpreter which will interpret an AST produced by the parser."""
from semantic_analysis import semantic_analyser
from parser_.tree_nodes import InteriorNode
from parser_.tree_nodes import LeafNode
#CONSIDER USING BUILT IN FUNCTION EVAL()
class Interpreter(object):
	"""The interpreter class which provides the method to interpret an AST."""
	# Used to hold variables seen so far, along with their current values
	_var = dict()
	
	def _interpret(self, node):
		"""Recursively traverses the AST executing Python oporators on child nodes when it visits an equivilant Java interior node."""
		# Check if it's an interior before getting the children
		if isinstance(node, InteriorNode):
			children = node.get_children()
			
			# Iteratively interpret each child of a block
			if node.node_id == "block":
				for child in children:
						self._interpret(child)
			
			# Variables are added to _var when a declartion is found
			if node.node_id == "var_dcl":
				#If it's a simple declaration
				if isinstance(children[1], LeafNode):
					# Set value to None because not yet known
					self._var[children[1].value] = None
				else: # There is an assignment statement, so the value of the right side of the assignment can be added to _var
					name = children[1].get_children()[0].value
					value = self._interpret(children[1].get_children()[1])
					self._var[name] = value
			
			if node.node_id == "if":
				# First see if the boolean expression is True
				if self._interpret(children[0]) is True:
					# If it is interpret the first child
					self._interpret(children[1])
				else:
					try:
						# Interpret the second child if the expression was false, and if there is one
						self._interpret(children[2])
					except IndexError:
						pass
			
			if node.node_id == "while":
				# Iteratively interpret the right child while the left child holds as True
				while self._interpret(children[0]) is True:
					self._interpret(children[1])
			
			if node.node_id == "for":
				# Interpret the assignment statement
				self._interpret(children[0])
				# Works similarly to while statements, although the third child (the incremental statement) also must be interpreted
				while self._interpret(children[1]) is True:
					self._interpret(children[2])
					self._interpret(children[3])
			
			# Simply print the child to the Python terminal
			if node.node_id == "print":
				print self._interpret(children[0])
			
			# Assign the value of the right child to the referenced item in _var
			if node.node_id == "=":
				self._var[children[0].value] = self._interpret(children[1])
			
			# The following statements all just convert to equivilant python oporations
			
			if node.node_id == "||":
				return self._interpret(children[0])  == True or self._interpret(children[1])  == True
			
			if node.node_id == "&&":
				return self._interpret(children[0]) == True and self._interpret(children[1])  == True
			
			if node.node_id == "==":
				return self._interpret(children[0])  == self._interpret(children[1])
			
			if node.node_id == "!=":
				return self._interpret(children[0])  != self._interpret(children[1])
			
			if node.node_id == ">":
				return self._interpret(children[0])  > self._interpret(children[1])
			
			if node.node_id == "<":
				return self._interpret(children[0])  < self._interpret(children[1])
			
			if node.node_id == ">=":
				return self._interpret(children[0])  >= self._interpret(children[1])
			
			if node.node_id == "<=":
				return self._interpret(children[0])  <= self._interpret(children[1])
			
			if node.node_id == "+":
				return self._interpret(children[0])  + self._interpret(children[1])
			
			if node.node_id == "-":
				return self._interpret(children[0])  - self._interpret(children[1])
			
			if node.node_id == "*":
				return self._interpret(children[0])  * self._interpret(children[1])
			
			if node.node_id == "/":
				return self._interpret(children[0])  / self._interpret(children[1])
			
			if node.node_id == "not":
				return not self._interpret(children[0]) 
			
			if node.node_id == "neg":
				return -self._interpret(children[0])
			
			if node.node_id == "pos":
				return +self._interpret(children[0])
			
			if node.node_id == "inc":
				self._var[children[0].value] += 1
			
			if node.node_id == "dec":
				self._var[children[0].value] -= 1
		
		else: # It's a leaf
			# If it's an identifier, look up its current value in _var
			if node.node_id == "id":
				return self._var[node.value]
			# If it's a literal, return its value
			else:
				return node.value
	
	def run_interpreter(self, program):
		"""Runs the interpreter on source code (program)."""
		ast = semantic_analyser.analyse(program)
		Interpreter()._interpret(ast)