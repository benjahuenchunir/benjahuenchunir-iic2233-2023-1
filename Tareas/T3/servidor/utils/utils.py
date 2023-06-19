import json


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