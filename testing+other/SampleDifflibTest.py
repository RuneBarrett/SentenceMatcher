from difflib import SequenceMatcher

a0 = "I Danmarks Lærerforening erklærer formand Anders Bondo Christensen sig enig i behovet for et kvalitativt løft af uddannelsen og ønsker sig en femårig kandidatuddannelse. Om det er i regi af universitet er ikke afgørende for ham."
a1 = "i Danmarks Lærerforening er Claire formand Anders Bondo Christensen sig enig i behovet for et kvalitativt løft af uddannelsen og ønsker sig en 5 årig kandidatuddannelse om det i regi af Universitetet er ikke afgørende for ham"

b0 = "I Danmarks Lærerforening erklærer formand Anders Bondo Christensen sig enig i behovet for et kvalitativt løft af uddannelsen og ønsker sig en femårig kandidatuddannelse"
b1 = "i Danmarks Lærerforening er Claire formand Anders Bondo Christensen sig enig i behovet for et kvalitativt løft af uddannelsen og ønsker sig en 5 årig kandidatuddannelse"

b2 = "Om det er i regi af universitet er ikke afgørende for ham"
b3 = "om det i regi af Universitetet er ikke afgørende for ham"

b4 = "er Claire"
b5 = "erklærer"

inp = "abc. bcd. cde. def. efg."
tra = "abc. bcc. cdt. def. efg."

# cut sentence until first . / get next sentence in array
inpList = inp.split(".")
print(inpList)


ratio = SequenceMatcher(None, b4.lower(), b5.lower()).ratio()
print(ratio)
