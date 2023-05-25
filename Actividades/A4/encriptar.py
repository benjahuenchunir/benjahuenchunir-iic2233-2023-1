from typing import List
import json
from errors import JsonError, SequenceError


def serializar_diccionario(dictionary: dict) -> bytearray:
    try:
        return bytearray(json.dumps(dictionary).encode("UTF-8"))
    except TypeError:
        raise JsonError()


def verificar_secuencia(mensaje: bytearray, secuencia: List[int]) -> None:
    if max(secuencia) >= len(mensaje) or len(set(secuencia)) != len(secuencia):
        raise SequenceError()


def codificar_secuencia(secuencia: List[int]) -> bytearray:
    secuencia_codificada = bytearray()
    for numero in secuencia:
        secuencia_codificada.extend(numero.to_bytes(length=2, byteorder='big'))
    return secuencia_codificada


def codificar_largo(largo: int) -> bytearray:
    return bytearray(largo.to_bytes(length=4, byteorder='big'))


def separar_msg(mensaje: bytearray, secuencia: List[int]) -> List[bytearray]:
    m_bytes_secuencia = bytearray()
    m_reducido = bytearray()
    # Completar

    return [m_bytes_secuencia, m_reducido]


def encriptar(mensaje: dict, secuencia: List[int]) -> bytearray:
    verificar_secuencia(mensaje, secuencia)

    m_bytes_secuencia, m_reducido = separar_msg(mensaje, secuencia)
    secuencia_codificada = codificar_secuencia(secuencia)

    return (
        codificar_largo(len(secuencia))
        + m_bytes_secuencia
        + m_reducido
        + secuencia_codificada
    )


if __name__ == "__main__":
    original = serializar_diccionario({"tama": 1})
    encriptado = encriptar(original, [1, 5, 10, 3])
    print(original)
    print(encriptado)
