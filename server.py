import uasyncio as asyncio
import socket
from machine import Pin, Timer, freq
import network
from hx711 import HX711

# Configuración inicial del servidor y la luz
luz = Pin(2, Pin.OUT)
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect('Zildjan', 'uuuu0000')

# Configuración inicial del SSR y el sensor HX711
freq(160000000)
ssr = Pin(10, Pin.OUT)
driver = HX711(d_out=13, pd_sck=12)
driver.channel = HX711.CHANNEL_B_32

# Define los valores de encendido y apagado del SSR
VALOR_ENCENDIDO = 7000000
VALOR_APAGADO = 3000000

# Variable global para controlar el temporizador
timer_activo = False
tim = Timer(-1)  # Crear el temporizador pero sin inicializar

# Función para manejar la presión y controlar el SSR
def manejar_presion(timer):
    try:
        presion = driver.read()  # Lee el valor de la variable

        if presion < VALOR_APAGADO:
            ssr.value(1)  # Enciende el SSR
            print("SSR encendido")
        elif presion >= VALOR_ENCENDIDO:
            ssr.value(0)  # Apaga el SSR
            print("SSR apagado")
    except Exception as e:
        print(f"Error leyendo la presión: {e}")

# Función para iniciar el temporizador
def iniciar_timer():
    global timer_activo
    if not timer_activo:
        tim.init(period=2000, mode=Timer.PERIODIC, callback=manejar_presion)
        timer_activo = True
        print("Temporizador iniciado")

# Función para detener el temporizador
def detener_timer():
    global timer_activo
    if timer_activo:
        tim.deinit()  # Detener el temporizador
        timer_activo = False
        print("Temporizador detenido")

async def handle_client(client):
    try:
        request = client.recv(1024)
        if isinstance(request, bytes):  # Verificar si el request es bytes antes de decodificar
            request = request.decode()

        request_line = request.split("\r\n")[0]
        print("Request:", request_line)

        if 'OPTIONS' in request_line:
            response = 'HTTP/1.1 204 No Content\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Methods: GET, POST, OPTIONS\r\nAccess-Control-Allow-Headers: Content-Type\r\n\r\n'
            client.send(response.encode())

        elif 'GET /apagar HTTP/1.1' in request_line:
            luz.on()  # Apaga la luz
            detener_timer()  # Detener el temporizador
            response = 'HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\nContent-Type: application/json\r\n\r\n{"status":"success","message":"Luz apagada y temporizador detenido"}'

        elif 'GET /prender HTTP/1.1' in request_line:
            luz.off()  # Enciende la luz
            iniciar_timer()  # Iniciar el temporizador
            response = 'HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\nContent-Type: application/json\r\n\r\n{"status":"success","message":"Luz encendida y temporizador iniciado"}'

        else:
            response = 'HTTP/1.1 404 Not Found\r\nAccess-Control-Allow-Origin: *\r\nContent-Type: application/json\r\n\r\n{"status":"error","message":"Recurso no encontrado"}'

        client.send(response.encode())

    except Exception as e:
        print("Error handling client:", e)

    finally:
        client.close()

# Lógica del servidor
async def start_server():
    try:
        addr_info = socket.getaddrinfo('0.0.0.0', 8082)
        addr = addr_info[0][-1]

        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(addr)
        s.listen(1)
        print('Listening on', addr)

        while True:
            client, addr = s.accept()
            print('Client connected from', addr)
            await handle_client(client)

    except OSError as e:
        print(f"OSError: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")

# Iniciar el servidor
async def main():
    await start_server()

asyncio.run(main())
