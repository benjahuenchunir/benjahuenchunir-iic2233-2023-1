import json
import pickle
import socket

def parametro(llave: str):
    with open("parametros.json", "rt", encoding="utf-8") as f:
        return json.loads(f.read())[llave]


class Mensaje:
    def __init__(self, operacion=None, data=None):
        self.operacion = operacion
        self.data = data

    def __repr__(self):
        return f"{self.operacion}: {self.data}"

    def __eq__(self, obj):
        return self.operacion == obj


def decodificar_mensaje(mensaje: bytes, largo: int) -> bytearray:
    mensaje_decodificado = bytearray()
    for i in range(
        0,
        len(mensaje)
        - (parametro("TAMANO_CHUNKS_BLOQUE") + parametro("TAMANO_CHUNKS_MENSAJE")),
        parametro("TAMANO_CHUNKS_BLOQUE") + parametro("TAMANO_CHUNKS_MENSAJE"),
    ):
        mensaje_decodificado.extend(
            mensaje[
                i
                + parametro("TAMANO_CHUNKS_BLOQUE") : i
                + parametro("TAMANO_CHUNKS_MENSAJE")
                + parametro("TAMANO_CHUNKS_BLOQUE")
            ]
        )
    mensaje_decodificado.extend(
        mensaje[-parametro("TAMANO_CHUNKS_MENSAJE") :][
            : largo
            - (parametro("TAMANO_CHUNKS_MENSAJE"))
            * (largo // parametro("TAMANO_CHUNKS_MENSAJE"))
        ]
    )
    return mensaje_decodificado


def codificar_mensaje(mensaje: bytearray) -> bytearray:
    mensaje_codificado = bytearray(
        len(mensaje).to_bytes(parametro("TAMANO_CHUNKS_BLOQUE"), "little")
    )
    for i in range(0, len(mensaje), parametro("TAMANO_CHUNKS_MENSAJE")):
        mensaje_codificado.extend(
            i.to_bytes(parametro("TAMANO_CHUNKS_BLOQUE"), "big")
        )
        chunk = mensaje[i : i + parametro("TAMANO_CHUNKS_MENSAJE")]
        if len(chunk) < parametro("TAMANO_CHUNKS_MENSAJE"):
            chunk.extend(bytearray(parametro("TAMANO_CHUNKS_MENSAJE") - len(chunk)))
        mensaje_codificado.extend(chunk)
    return mensaje_codificado


def log(usuario, evento, detalles="-"):
    print(f"{usuario:^17.15}|{evento:^24.22}|{detalles:^24}")
