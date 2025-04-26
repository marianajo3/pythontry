import socket
import time

from notas_utils import calc_nota_final

SOCK_BUFFER = 1024

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address =("0.0.0.0", 5000)

    print(f"Iniciando servidor en {server_address[0]}: {server_address[1]}")

    sock.bind(server_address)

    sock.listen(5)

    while True:
        print(f"Esperando conexiones...")

        conn, client = sock.accept()

        print(f"Conexion de {client[0]}: {client[1]}")

        try:
            while True:
                data = conn.recv(SOCK_BUFFER)
                if data:

                    inicio = time.perf_counter()
                    valores = data.decode("utf-8").split(",")
                    valores = [int(valor) for valor in valores]
                    nota_final = calc_nota_final(valores[1:])
                    fin_cpu = time.perf_counter()
                    conn.sendall(str(nota_final).encode("utf-8"))
                    fin = time.perf_counter()
                else:
                    print(f"El cliente cerro la conexion de manera abrupta.")
        except ConnectionResetError:
             print("El cliente cerro la conexion de manera abrupta")
        except KeyboardInterrupt:
            print("El usuario termino el programa")
        finally:
            print("Cerrando la conexion")
            conn.close()
            print(f"Total de operacion: {(fin - inicio):.6f} segundos.")
            print(f"Total de CPU: {(fin_cpu - inicio):.6f} segundos.")
            print(f"Total de transmision: {(fin - fin_cpu):.6f} segundos.")
           

        
                
    
