import asyncio

async def main():
    reader, writer = await asyncio.open_connection('127.0.0.1', 5000)

    while True:
        codigo = input("Ingrese el código del alumno (o 'exit' para salir): ")

        if codigo.lower() == 'exit':
            break

        writer.write(codigo.encode('utf-8'))
        await writer.drain()

        respuesta = await reader.readline()
        print(f"Respuesta del servidor: {respuesta.decode('utf-8').strip()}")

    writer.close()
    await writer.wait_closed()

asyncio.run(main())
