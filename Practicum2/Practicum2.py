class Rule:
	def __init__(self, lhs = '', rhs = ''):
		self.lhs = lhs
		self.rhs = rhs

	def __eq__(self, other):
		return self.lhs == other.lhs and self.rhs == other.rhs

	def __hash__(self):
		return hash(self.rhs) ^ hash(self.lhs)

	def __str__(self):
		return "{0} -> {1}".format(self.lhs, self.rhs)


class Situation:
	def __init__(self, _rule, point = 0, start = 0):
		self.rule = _rule
		self.point_index = point
		self.start_index = start

	def __eq__(self, other):
		return self.rule == other.rule and self.point_index == other.point_index\
		and self.start_index == other.start_index

	def __hash__(self):
		return hash(self.rule) ^ hash(self.point_index) ^ hash(self.start_index)

	def __str__(self):
		return "Situation({}, {}, {})".format(self.rule, self.point_index, self.start_index)

	def finished(self):
		return self.point_index >= len(self.rule.rhs)

	def next_symbol(self):
		if self.finished():
			return "#"
		else:
			return self.rule.rhs[self.point_index]

def add_situation(situation, D_set, D_list, k):
	if situation not in D_set[k]:
		D_set[k].add(situation)
		D_list[k].append(situation)

def predict(situation, D_set, D_list, k, P):
	for rule in P:
		if rule.lhs == situation.next_symbol():
			add_situation(Situation(rule, 0, k), D_set, D_list, k)

def complete(situation, D_set, D_list, k):
	position = 0
	while position < len(D_list[situation.start_index]):
		s_to_complete = D_list[situation.start_index][position]
		if s_to_complete.next_symbol() == situation.rule.lhs:
			add_situation(Situation(s_to_complete.rule, s_to_complete.point_index + 1, \
				s_to_complete.start_index), D_set, D_list, k)
		position += 1


def scan(situation, D_set, D_list, k, word):
	if word[k] == situation.next_symbol():
		add_situation(Situation(situation.rule, situation.point_index + 1,\
			situation.start_index), D_set, D_list, k + 1)

def is_terminal(symbol):
	return symbol.islower() and symbol.isalpha()

def parse(word, P):
	D_set = [set() for i in range(len(word) + 1)]
	D_list = [[] for i in range(len(word) + 1)]

	add_situation(Situation(P[0], 0, 0), D_set, D_list, 0)

	for k in range(len(word) + 1):
		position = 0
		while position < len(D_list[k]):
			situation = D_list[k][position]
			if situation.finished():
				complete(situation, D_set, D_list, k)
			else:
				if is_terminal(situation.next_symbol()) and k < len(word):
					scan(situation, D_set, D_list, k, word)
				else:
					predict(situation, D_set, D_list, k, P)
			position += 1
	return Situation(P[0], 1, 0) in D_set[len(word)]

if __name__ == '__main__':
	word = input()

	P = [] 
	P.append(Rule('T', 'S'))
	P.append(Rule('S', 'C'))
	P.append(Rule('S', 'CS'))
	P.append(Rule('C', 'Dc'))
	P.append(Rule('D', 'aDb'))
	P.append(Rule('D', ''))

	print(parse(word, P))