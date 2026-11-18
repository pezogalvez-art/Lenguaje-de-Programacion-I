"""Proyecto PC04 - Parte B3: Cifrado Vigenère con clave personal.

Código universitario: 2155263 | Constantes personales: D = 3, P = 6, K = 2.
"""

import unicodedata
from typing import Final

CODIGO_UNIVERSITARIO: Final[int] = 2155263
D: Final[int] = 3
P: Final[int] = 6
K: Final[int] = 2

CLAVE_APELLIDO: Final[str] = "PEZO"
TEXTO_PROYECTO: Final[str] = "Lenguaje de Programación I · UNAP Iquitos 2026"
BASE_ASCII: Final[int] = ord("A")
ALFABETO_LEN: Final[int] = 26


def normalizar_texto(texto: str) -> str:
    """Convierte el texto a mayúsculas sin tildes, transformando Ñ en N."""
    descompuesto = unicodedata.normalize("NFD", texto)
    sin_marcas = "".join(
        ch for ch in descompuesto if unicodedata.category(ch) != "Mn"
    )
    return sin_marcas.upper()


def _limpiar_clave(clave: str) -> str:
    """Valida y normaliza la clave dejando únicamente letras A-Z."""
    clave_norm = normalizar_texto(clave)
    solo_letras = "".join(ch for ch in clave_norm if "A" <= ch <= "Z")
    if not solo_letras:
        raise ValueError("La clave debe contener al menos una letra A-Z")
    return solo_letras


def vigenere(texto: str, clave: str, descifrar: bool = False) -> str:
    """Cifra o descifra un texto con el método Vigenère sobre el alfabeto A-Z.

    Args:
        texto: Mensaje original o cifrado.
        clave: Clave alfabética (se normaliza a A-Z sin tildes).
        descifrar: False para cifrar; True para descifrar.

    Returns:
        Cadena resultante en mayúsculas sin tildes, conservando espacios y signos.
    """
    texto_norm = normalizar_texto(texto)
    clave_limpia = _limpiar_clave(clave)
    largo_clave = len(clave_limpia)

    resultado: list[str] = []
    indice_clave = 0

    for ch in texto_norm:
        if "A" <= ch <= "Z":
            pos_texto = ord(ch) - BASE_ASCII
            desplazamiento = ord(clave_limpia[indice_clave % largo_clave]) - BASE_ASCII
            if descifrar:
                nueva_pos = (pos_texto - desplazamiento) % ALFABETO_LEN
            else:
                nueva_pos = (pos_texto + desplazamiento) % ALFABETO_LEN
            resultado.append(chr(BASE_ASCII + nueva_pos))
            indice_clave += 1
        else:
            resultado.append(ch)

    return "".join(resultado)


def main() -> None:
    """Ejecuta el cifrado Vigenère, verifica ida y vuelta con assert y reporta."""
    # Pruebas de control con assert
    assert vigenere("A B C", "AB") == "A C C"
    assert vigenere("A C C", "AB", descifrar=True) == "A B C"
    assert vigenere("Ñandú 2026!", "SOL") == "FOYVI 2026!"
    assert vigenere("FOYVI 2026!", "SOL", descifrar=True) == "NANDU 2026!"

    # Cifrado y descifrado del texto del proyecto con tu clave personal PEZO
    texto_normalizado = normalizar_texto(TEXTO_PROYECTO)
    cifrado = vigenere(TEXTO_PROYECTO, CLAVE_APELLIDO, descifrar=False)
    descifrado = vigenere(cifrado, CLAVE_APELLIDO, descifrar=True)

    assert descifrado == texto_normalizado, "El descifrado no coincide con el texto normalizado"

    print(f"Clave utilizada    : {CLAVE_APELLIDO}")
    print(f"Texto original     : {TEXTO_PROYECTO}")
    print(f"Texto normalizado  : {texto_normalizado}")
    print(f"Texto cifrado      : {cifrado}")
    print(f"Texto descifrado   : {descifrado}")
    print("Verificación assert exitosa: ida y vuelta exacta.")


if __name__ == "__main__":
    main()