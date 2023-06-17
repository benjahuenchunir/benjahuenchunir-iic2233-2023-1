def encriptar(msg: bytearray, N: int) -> bytearray:
    bytearray_encriptado = bytearray(msg)
    for y in range(len(msg)):
        bytearray_encriptado[(y + N) % len(msg)] = msg[y]
    bytearray_encriptado[N], bytearray_encriptado[0] = (
        bytearray_encriptado[0],
        bytearray_encriptado[N],
    )
    return bytearray_encriptado


def desencriptar(msg: bytearray, N: int) -> bytearray:
    msg[N], msg[0] = msg[0], msg[N],
    bytearray_desencriptado = bytearray(msg)
    for y in range(len(msg)):
        bytearray_desencriptado[y] = msg[(y + N) % len(msg)]
    return bytearray_desencriptado


if __name__ == "__main__":
    # Testear encriptar
    N = 1
    msg_original = bytearray(b'\x01\x02\x03\x04\x05\x06\x07\x08\x09\x00\x01\x02\x03\x04\x05')
    msg_esperado = bytearray(b'\x01\x05\x02\x03\x04\x05\x06\x07\x08\x09\x00\x01\x02\x03\x04')
    msg_encriptado = encriptar(msg_original, N)
    if msg_encriptado != msg_esperado:
        print("[ERROR] Mensaje escriptado erroneamente")
    else:
        print("[SUCCESSFUL] Mensaje escriptado correctamente")
    
    # Testear desencriptar
    msg_desencriptado = desencriptar(msg_esperado, N)
    if msg_desencriptado != msg_original:
        print("[ERROR] Mensaje descencriptado erroneamente")
    else:
        print("[SUCCESSFUL] Mensaje descencriptado correctamente")