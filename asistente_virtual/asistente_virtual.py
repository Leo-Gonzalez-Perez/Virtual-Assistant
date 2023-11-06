import pyttsx3
import speech_recognition as sr
import  pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

# opciones de voz / idioma
id_1 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
id_2 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"
id_3 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0"
id_4 = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-MX_SABINA_11.0"


# Escuchar el mic y transformar lo escuchado como texto (str)
def transformar_audio_en_texto():
    # Almacenar recognizer en una variable
    r = sr.Recognizer()

    # Configurar el microfono
    with sr.Microphone() as origen:

        # Establecer tiempo de espera entre que se active el mic y el comienzo de la grabacion
        r.pause_threshold = 0.8

        # Informar que comenzo la grabacion, para confirmar que el mic esta funcionando
        print("Ya puedes hablar")

        # Guardar lo que escuche como audio
        audio = r.listen(origen)

        try:
            # Guardo en una variable lo que trae una demanda a Google para que transforme en texto el audio
            pedido = r.recognize_google(audio, language="es-ar")

            # Prueba para ver si hay texto
            print("Dijiste: " + pedido)

            # Devolver pedido
            return pedido

        # En caso de que no comprenda el audio
        except sr.UnknownValueError:

            # Prueba de que no comprendio el audio
            print("ups, no entendi")

            # devolver error
            return "Sigo esperando..."

        # En caso de no resolver el pedido
        except sr.RequestError:

            # Prueba de que no resolvio el pedido
            print("ups, no pude resolver el pedido")

            # devolver error
            return "Sigo esperando..."

        except:

            # Prueba de que algo ha fallado
            print("ups, algo ha fallado")

            # devolver error
            return "Sigo esperando..."


# Funcion para que el asistente pueda ser escuchado
def hablar(mensaje):

    # Encender el motor de pyttsx3. Por protocolo se usa engine
    engine = pyttsx3.init()
    engine.setProperty('voice', id_4)

    # pronunciar el mensaje con la voz que tiene seteada Windows
    engine.say(mensaje)

    # Y se queda esperando
    engine.runAndWait()


# informar el dia de la semana
def pedir_dia():

    # crear variable con datos de hoy
    dia = datetime.date.today()
    print(dia)

    # crear variable para el dia de semana
    dia_semana = dia.weekday()
    print(dia_semana)

    # diccionario con nombres de dias
    calendario = {0: 'domingo',
                  1: 'lunes',
                  2: 'martes',
                  3: 'miércoles',
                  4: 'jueves',
                  5: 'viernes',
                  6: 'sábado'}

    # decir dia de la semana
    hablar(f"Hoy es {calendario[dia_semana]}")


# Informar que hora es
def pedir_hora():

    # Crear una variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f"En este momento son las {hora.hour} horas con {hora.minute} minutos y {hora.second} segundos"
    print(hora)

    # decir la hora
    hablar(hora)


def saludo_inicial():


    # Crear variable con datos de la hora
    hora = datetime.datetime.now()
    if hora.hour > 20 or hora.hour < 6:
        momento = "Buenas noches"
    elif hora.hour >= 6 and hora.hour < 13:
        momento = "Buenos días"
    else:
        momento = "Buenas tardes"

    # Decir el saludo
    hablar(f"{momento}, soy Nicasio. Dime en qué te puedo ayudar")


# Funcion central del asistente
def pedir_cosas():

    # Activar saludo inicial
    saludo_inicial()

    # generamos variable de corte
    comenzar = True

    # loop central, que mantendra al asistente funcionando tras cumplir un pedido y hasta que comenzar sea False
    while comenzar:

        # activar el micro y guardar el pedido en un string
        pedido = transformar_audio_en_texto().lower()

        if "abrir youtube" in pedido:
            hablar("Con gusto, estoy abriendo YouTube")
            webbrowser.open("https://www.youtube.com")
            continue
        elif "abrir un buscador" in pedido:
            hablar("Claro, ya abro un buscador")
            webbrowser.open("https://www.google.com")
            continue
        elif "qué día es hoy" in pedido:
            pedir_dia()
            continue
        elif "qué hora es" in pedido:
            pedir_hora()
            continue
        elif "busca en wikipedia" in pedido:
            hablar("Claro, ya busco en Wikipedia lo que me pidas")
            pedido = pedido.replace("busca en wikipedia", "")
            wikipedia.set_lang("es")
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar(f"Esto es lo que dice Wikipedia sobre {pedido}:")
            hablar(resultado)
            continue
        elif "busca en internet" in pedido:
            hablar("Claro, ya busco en la web eso:")
            pedido = pedido.replace("busca en internet", "")
            pywhatkit.search(pedido)
            hablar("Esto es lo que he encontrado")
            continue
        elif "reproducir" in pedido:
            hablar("Dale, ya le doy al botón de play")
            pywhatkit.playonyt(pedido)
            continue
        elif "chiste" in pedido:
            hablar(pyjokes.get_joke("es"))
            continue
        elif "precio de las acciones" in pedido:
            accion = pedido.split("de")[-1].strip()
            cartera = {"apple":"APPL",
                       "amazon":"AMZN",
                       "google":"GOOGL"}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info["regularMarketPrice"]
                hablar(f"La encontré, el precio de la acción de {accion} es {precio_actual}")
                continue
            except:
                hablar("Lo siento, algo ocurrió y no he logrado hallar el precio de la acción pedida")
                continue
        elif "adiós nicasio" in pedido:
            hablar("Chau, me voy a dormir.")
            break

pedir_cosas()