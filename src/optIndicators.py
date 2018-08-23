class Indicator:
	def __init__(self, op, left, right, assign_to=None):
		self.op = op
		self.left = left
		self.right = right
		self.assign = false
		self.indicator = ""
		
	def addition(self):
		if all([
			self.op == 'plus', 
			self.left == 0 or self.right == 0, 
			self.assign = true, 
			assign_to == self.left or assign_to == self.right
			]):
			self.indicator = "STRENGTH_REDUCTION"
		elif self.op == 'plus' and (self.left == 0 or self.right == 0):
			self.indicator = "NEUTRAL"
	def subtraction(self):
		if all([
			self.op == 'minus', 
			self.left == 0 or self.right == 0, 
			self.assign = true, 
			assign_to == self.left or assign_to == self.right
			]):
			self.indicator = "STRENGTH_REDUCTION"
		elif self.op == 'minus' and (self.left == 0 or self.right == 0):
			self.indicator = "NEUTRAL"
	def multiplication(self):
		if all([
			self.op == 'mul', 
			self.left == 1 or self.right == 1, 
			self.assign = true, 
			assign_to == self.left or assign_to == self.right
			]):
			self.indicator = "STRENGTH_REDUCTION"
		elif self.op == 'mul' and (self.left == 1 or self.right == 1):
			self.indicator = "NEUTRAL"
	def division(self):
		if all([
			self.op == 'div', 
			self.left == 0, 
			self.assign = true, 
			assign_to == self.left
			]):
			self.indicator = "STRENGTH_REDUCTION"
		if self.op == 'div' and self.right == 1:
			self.indicator = "NEUTRAL"
	