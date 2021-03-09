import sys

# Fisierul de intrare
input_file_name = str(sys.argv[1])

# Citirea datelor
input_file = open(input_file_name, 'r')
data = input_file.read()

infos = data.splitlines()

# Cate stari avem in AFN?
no_states_nfa = int(infos[0])

# Pe ce litere putem schimba starea curenta?
letters = ['eps']

# Procesarea starilor finale
final_states_input = infos[1].split()
final_states_nfa = []
for c in final_states_input:
	final_states_nfa.append(int(c))
final_states_nfa.sort()

# Procesarea lui DELTA pentru AFN
delta_nfa = {}

for i in range(2, len(infos)):
	
	transition = infos[i].split()
	start = int(transition[0]) # starea sursa

	if not start in delta_nfa:
		delta_nfa[start] = {}

	c = transition[1] # calea pe care inaintam
	if not c in letters:
		letters.append(c)

	# Stabilirea starilor destinatie
	s = set()
	for j in range(2, len(transition)):
		end = int(transition[j])
		s.add(end)
	d = {c : s}
	delta_nfa[start].update(d)

	# Adaugarea tranzitiei A --(eps)--> A
	# daca n-avem epsilon-tranzitii din starea curenta
	if not 'eps' in delta_nfa[start]:
		delta_nfa[start]['eps'] = set([start])

	# sau daca nu am gasit tranzitia de mai sus in fisierul de intrare
	elif not start in delta_nfa[start]['eps']:
		delta_nfa[start]['eps'].add(start)

# Completarea lui DELTA_AFN cu seturi goale unde este cazul
for k in range(no_states_nfa):
	if k not in delta_nfa:
		delta_nfa[k] = {}
	for c in letters:
		if not c in delta_nfa[k]:
			if c != 'eps':
				delta_nfa[k][c] = set()
			else:
				delta_nfa[k][c] = set([k])

# Generarea inchiderilor EPSILON
for k in range(no_states_nfa):
	epsilon_1 = delta_nfa[k]['eps']
	epsilon_2 = set()
	while 1:
		for n in epsilon_1:
			epsilon_2 = epsilon_2 | delta_nfa[n]['eps']

		if epsilon_2 == epsilon_1: # Daca {epsilon} nu se mai modifica
			break # iesim din while
		epsilon_1 = epsilon_2.copy()

	delta_nfa[k]['eps'] = epsilon_1

# Generarea lui DELTA pentru AFD
delta_dfa = {}
letters_dfa = letters[1:] # Lucram cu aceleasi litere, mai putin 'eps'
queue = []
queue_index = 0
queue.append(delta_nfa[0]['eps'])

while queue_index < len(queue):
	# frozenset poate fi folosit ca o cheie intr-un dictionar / map
	crt_state = frozenset(queue[queue_index]) # starea curenta in coada
	delta_dfa[crt_state] = {}

	# Vom lucra cu set "unfrozen" pentru o cautare mai rapida
	unfrozen_crt_state = set(crt_state)
	for c in letters_dfa: # iteram prin toate literele

		# Generarea urmatoarei stari din starea si calea curenta
		s = set()
		for x in unfrozen_crt_state:
			y = delta_nfa[x][c]
			for x1 in y:
				s = s | delta_nfa[x1]['eps']
		delta_dfa[crt_state][c] = s.copy()
		if not s in queue:
			queue.append(s)
	queue_index = queue_index + 1
	# Nu folosesc pop,
	# deoarece toate valorile din coada vor fi folosite mai tarziu

# Obtinerea starilor finale
final_states_dfa = []
for s in delta_dfa:
	for f in final_states_nfa:
		if f in s:
			final_states_dfa.append(s)
			break

# Conversia din stari de tip Set in stari numerice
set_to_indices = {}
indices_to_set = {}
for i in range(len(queue)):
	indices_to_set[i] = queue[i]
	set_to_indices[frozenset(queue[i])] = i

nr_stari_dfa = len(queue)
delta_dfa_num = {}
for i in range(nr_stari_dfa):
	delta_dfa_num[i] = {}
	s = frozenset(indices_to_set[i])
	for c in letters_dfa:
		x = frozenset(delta_dfa[s][c])
		y = set_to_indices[x]
		delta_dfa_num[i][c] = y

# Transformarea starilor finale din seturi in numere
for i in range(len(final_states_dfa)):
	final_states_dfa[i] = set_to_indices[final_states_dfa[i]]

# Generarea sirului
final_print = str(nr_stari_dfa) + "\n"
for i in range(len(final_states_dfa) - 1):
	final_print = final_print + str(final_states_dfa[i]) + " "
final_print  = final_print + str(final_states_dfa[-1]) + "\n"
for k in delta_dfa_num:
	for c in delta_dfa_num[k]:
		final_print = final_print + str(k) + " " + c + " "
		final_print = final_print + str(delta_dfa_num[k][c]) + "\n"

# Scrierea sirului de mai sus in fisierul de iesire
output_file_name = str(sys.argv[2])
output_file = open(output_file_name, "w+")

output_file.write(final_print)