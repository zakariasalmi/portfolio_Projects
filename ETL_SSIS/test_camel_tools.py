import re
from camel_tools.utils.normalize import normalize_unicode, normalize_alef_maksura_ar, normalize_teh_marbuta_ar
from camel_tools.tokenizers.word import simple_word_tokenize

# Exemple de texte en arabe
texte = "أحب البرمجة، و أتمنى أن أكون مبرمجًا ماهرًا."

# Normalisation des lettres
texte = normalize_unicode(texte)
texte = normalize_alef_maksura_ar(texte)
texte = normalize_teh_marbuta_ar(texte)

# Suppression des diacritiques
texte_sans_diacritiques = re.sub(r'[ًٌٍَُِّْ]', '', texte)

# Suppression des caractères spéciaux et chiffres
texte_normalise = re.sub(r'[^ا-ي\s]', '', texte_sans_diacritiques)

# Tokenisation
tokens = simple_word_tokenize(texte_normalise)

print("Texte normalisé:", texte_normalise)
print("Tokens:", tokens)