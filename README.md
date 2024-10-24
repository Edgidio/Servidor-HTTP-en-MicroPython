# Documentación del Servidor HTTP en MicroPython

## Descripción del Código

Este script implementa un servidor HTTP básico en **MicroPython**, diseñado para automatizar y controlar una bomba mediante el manejo de un relé de estado sólido (SSR) y la lectura de presión a través de un sensor **HX711**. El servidor permite encender y apagar una luz conectada a un pin digital y activar o desactivar la bomba de acuerdo a los valores de presión recibidos.

El servidor no utiliza ningún framework externo, lo que lo hace ligero y adecuado para sistemas embebidos con recursos limitados, como los microcontroladores. A través de la red Wi-Fi, se puede acceder al servidor para controlar el estado de la luz y del temporizador que maneja la bomba de manera remota.

## Funcionalidades

1. **Control del SSR y la bomba**: Se utiliza un sensor de presión conectado al módulo HX711. Dependiendo de los valores leídos, el SSR (conectado al pin 10) se enciende o apaga para activar o desactivar la bomba.

2. **Control remoto**: A través de solicitudes HTTP, el servidor puede:
   - **GET `/prender`**: Enciende la luz, activa el temporizador y comienza a monitorear la presión.
   - **GET `/apagar`**: Apaga la luz y detiene el temporizador, dejando de controlar la bomba.

3. **Configuración de red**: El servidor se conecta a una red Wi-Fi mediante el módulo de red `network`, y escucha solicitudes en el puerto `8082`.

4. **Automatización basada en presión**: El temporizador lee continuamente el valor del sensor de presión y controla el estado del SSR basado en los umbrales configurados (`VALOR_ENCENDIDO` y `VALOR_APAGADO`).

## Explicación del Código

1. **Configuración de la red y pines**:
   - El servidor se conecta a una red Wi-Fi definida con `sta_if.connect`.
   - Se configuran pines específicos para la luz, el SSR y el sensor de presión.

2. **Manejo de presión y control del SSR**:
   - La función `manejar_presion` lee el valor de presión del sensor HX711. Si el valor es menor que `VALOR_APAGADO`, el SSR se enciende; si es mayor o igual a `VALOR_ENCENDIDO`, el SSR se apaga.
   
3. **Servidor HTTP**:
   - El servidor responde a peticiones HTTP, permitiendo controlar la luz y el temporizador mediante las rutas `/prender` y `/apagar`.
   - Se utilizan respuestas JSON para indicar el éxito o fracaso de las operaciones.

4. **Temporizador**:
   - El temporizador se activa o desactiva mediante las funciones `iniciar_timer` y `detener_timer`. Este controla la frecuencia con la que se mide la presión y se ajusta el estado del SSR.

5. **Manejo de solicitudes**:
   - La función `handle_client` maneja las solicitudes HTTP recibidas, identificando la ruta y realizando la acción correspondiente (encender o apagar la luz y controlar el temporizador).

## Notas Importantes

- **Sin uso de frameworks**: Este servidor es ligero y no requiere dependencias adicionales, lo cual es ideal para dispositivos de bajos recursos como los microcontroladores.
- **Automatización**: El sistema automatiza el control de la bomba basado en lecturas de presión, lo que permite un funcionamiento autónomo.
- **Conectividad Wi-Fi**: El microcontrolador se conecta a una red inalámbrica, permitiendo la operación remota mediante HTTP.
