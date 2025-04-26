import socket
import time
import asyncio
from notas_utils import calc_nota_final, busca_notas


SOCK_BUFFER = 1024


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    print("Cliente conectado")

    try:
        while True:
            data = await reader.read(SOCK_BUFFER)

            if data:
                codigo = data.decode("utf-8")
                valores = busca_notas(codigo)
                nota_final = calc_nota_final(valores)
                writer.write(str(nota_final).encode("utf-8"))
                await writer.drain()
            else:
                print(f"No hay mas datos")
                break
    except IndexError:
        print("No existen notas par el alumno")
    except ConnectionResetError:
        print("El cliente cerro la conexion de manera abrupta")
    except KeyboardInterrupt:
        print("El usuario termino el programa")
    finally:
        writer.close()
        await writer.wait_closed()

async def main():
    server_address = ("0.0.0.0", 5000)

    server = await asyncio.start_server(handle_client,server_address[0], server_address[1])

    print(f"Iniciando servidor en {server_address[0]}:{server_address[1]}")

    #sock.bind(server_address)
    await server.serve_forever()

    #sock.listen(5)
    

if __name__ == '__main__':
    asyncio.run(main())