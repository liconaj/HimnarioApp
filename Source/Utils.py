import re
import unicodedata


def normalizetxt(texto: str) -> str:
    texto = re.sub(r'[^\w\s]', '', texto.lower())
    texto = ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')
    return texto
