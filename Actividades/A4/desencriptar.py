from typing import List
import json
from errors import JsonError, SequenceError


def deserializar_diccionario(mensaje_codificado: bytearray) -> dict:
    try:
        return json.loads(mensaje_codificado.decode("UTF-8"))
    except json.JSONDecodeError:
        raise JsonError()


def decodificar_largo(mensaje: bytearray) -> int:
    return int.from_bytes(mensaje[0:4], 'big')


def separar_msg_encriptado(mensaje: bytearray) -> List[bytearray]:
    m_bytes_secuencia = bytearray()
    m_reducido = bytearray()
    secuencia_codificada = bytearray()

    largo = decodificar_largo(mensaje)
    m_bytes_secuencia.extend(mensaje[4: 4 + largo])
    secuencia_codificada.extend(mensaje[len(mensaje) - 2 * largo:])
    m_reducido.extend(mensaje[4 + largo: len(mensaje) - 2 * largo])

    return [m_bytes_secuencia, m_reducido, secuencia_codificada]


def decodificar_secuencia(secuencia_codificada: bytearray) -> List[int]:
    numeros_transformados = []
    for indice in range(0, len(secuencia_codificada), 2):
        numeros_transformados.append(int.from_bytes(secuencia_codificada[indice: indice + 2], byteorder='big'))
    return numeros_transformados


def desencriptar(mensaje: bytearray) -> bytearray:
    m_bytes_secuencia, m_reducido, secuencia_codificada = separar_msg_encriptado(mensaje)
    secuencia = decodificar_secuencia(secuencia_codificada)

    pos_byte = sorted(list(zip(secuencia, m_bytes_secuencia)), key=lambda x: x[0])
    for pos, byte in pos_byte:
        m_reducido.insert(pos, byte)
    return m_reducido


if __name__ == "__main__":
    mensaje = bytearray(b'\x00\x00\x00\x04\x0A\x05\x03\x04\x08\x02\x03\x05\x09\x05\x09\x01\xFF\x00\x0B\x00\x00\x00\x02\x00\x04')
    desencriptado = desencriptar(mensaje)
    diccionario = deserializar_diccionario(desencriptado)
    print(diccionario)
