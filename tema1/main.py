import sys

# Obtinerea tuturor literelor distincte din pattern-ul dat
def distinctLetters(pattern):
	result = []
	for c in pattern:
		if c in result:
			continue
		result.append(c)
	result.sort() # aranjarea literelor in ordine alfabetica
	return result

# Vom retine starile intr-un dictionar cu rol de matrice
# Linia i -> analizam prefixul de lungime i
# Coloana c -> starea in care ajungem
def getDelta(pattern):
	delta = {}
	d = {} # dictionar auxiliar
	s = ''
	dist = distinctLetters(pattern)
	for i in range(len(pattern) + 1):
		for c in dist:
			s = pattern[0:i] + c
			if s == pattern[0:i + 1]:
				d[c] = i + 1 # inaintarea in pattern
			else: # daca nu inaintam in pattern
				if i == 0: # cazul sirului vid
					d[c] = 0
				else:
					idx = i
					aux = str(s) # copie a lui s
					while idx >= 0:
						# Eliminam prima litera succesiv
						# pana cand gasim
						# o stare corespunzatoare
						aux = aux[1:]
						idx = idx - 1
						if aux == pattern[0:idx] + c:
							d[c] = delta[idx][c]
							break

		# Atribuim starile rezultate la cheia i (prefixul de lungime i)
		delta[i] = d.copy()
	return delta

# Observatie: se genereaza coloane doar pentru literele din pattern 
# pentru eficienta spatiala

def solve(pattern, text):
	result = []
	delta = getDelta(pattern)
	dist = distinctLetters(pattern)
	s = 0
	for i in range(len(text)):
		c = text[i]
		if c not in dist: # Literelor care nu sunt in text
			s = 0 # le vom atribui mereu starea 0
			continue
		s = delta[s][c] # testam caracterul c din starea curenta
		if s == len(pattern): # am ajuns la finalul pattern-ului
			result.append(i + 1 - s) 
	return result

###############################################################################
#                                    MAIN                                     #
###############################################################################

# Fisierul de intrare
input_file_name = str(sys.argv[1])

# Citirea datelor
input_file = open(input_file_name, 'r')
data = input_file.read()

inputs = data.split()
pattern = inputs[0]
text = inputs[1]

# Rezolvarea problemei
solution = solve(pattern, text)

# Fisierul de iesire
output_file_name = str(sys.argv[2])
output_file = open(output_file_name, "w+")

# Formatarea afisarii rezultatului dorit
if not solution:
	quit()
final_print = ""
for x in solution:
	final_print = final_print + str(x) + " "
final_print = final_print + "\n"

# Scrierea rezultatului
output_file.write(final_print)
