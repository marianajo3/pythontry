import socket
import time
import asyncio
import datetime
from notas_utils import calc_nota_final, busca_notas

SOCK_BUFFER = 1024
TIMEOUT_SECONDS = 10
LOG_FILE = "registro.log"

async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    client_address = writer.get_extra_info('peername')
    print(f"Cliente conectado desde {client_address}")

    try:
        while True:
            try:
                # Leer datos con timeout
                data = await asyncio.wait_for(reader.read(SOCK_BUFFER), timeout=TIMEOUT_SECONDS)
            except asyncio.TimeoutError:
                print("Timeout alcanzado: cerrando conexión")
                break

            if not data:
                print("No hay más datos, cerrando conexión")
                break

            codigo = data.decode("utf-8").strip()
            
            # Mecanismo de apagado especial
            if codigo.lower() == "shutdown":
                print("Se recibió comando de apagado.")
                writer.close()
                await writer.wait_closed()
                asyncio.get_event_loop().stop()
                return

            # Validar código
            if not codigo.isdigit():
                mensaje_error = "ERROR: Código inválido.\n"
                writer.write(mensaje_error.encode("utf-8"))
                await writer.drain()
                continue

            # Procesar código
            try:
                valores = busca_notas(codigo)
                nota_final = calc_nota_final(valores)

                # Registrar en log
                with open(LOG_FILE, "a") as log:
                    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log.write(f"{ahora} | Código: {codigo} | Nota final: {nota_final}\n")

                # Enviar respuesta
                writer.write(f"{nota_final}\n".encode("utf-8"))
                await writer.drain()
            except IndexError:
                writer.write(b"ERROR: No existen notas para el alumno\n")
                await writer.drain()

    except ConnectionResetError:
        print(f"Cliente {client_address} cerró la conexión abruptamente")
    except KeyboardInterrupt:
        print("Servidor interrumpido manualmente")
    finally:
        writer.close()
        await writer.wait_closed()
        print(f"Conexión cerrada con {client_address}")

async def main():
    server_address = ("0.0.0.0", 5000)

    server = await asyncio.start_server(handle_client, server_address[0], server_address[1])

    print(f"Iniciando servidor en {server_address[0]}:{server_address[1]}")

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServidor detenido manualmente.")
