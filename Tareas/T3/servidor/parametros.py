import json


def parametro(llave: str):
    with open("parametros.json", "rt", encoding="utf-8") as f:
        return json.loads(f.read())[llave]