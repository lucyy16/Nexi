import speech_recognition as sr
import pyttsx3
import json
import os

engine = pyttsx3.init()

# Cargar o crear base de datos local
if not os.path.exists("db.json"):
    data = {
        "usuario": "Usuario",
        "pin": "1234",
        "tarjetas": [
            {"nombre": "Débito", "saldo": 8000},
            {"nombre": "Ahorros", "saldo": 3000}
        ]
    }
    with open("db.json", "w") as f:
        json.dump(data, f)
else:
    with open("db.json", "r") as f:
        data = json.load(f)

def hablar(texto):
    print(f"Asistente: {texto}")
    engine.say(texto)
    engine.runAndWait()

def escuchar():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("...")
        try:
            audio = r.listen(source, timeout=5)
            return r.recognize_google(audio, language='es-MX').lower()
        except: return ""

# Inicio del programa
hablar(f"Hola {data['usuario']}, sistema de voz activo.")

while True:
    voz = escuchar()
    if "banquero" in voz:
        hablar(f"Dime {data['usuario']}, ¿qué quieres hacer?")
        accion = escuchar()

        if "transferencia" in accion:
            hablar("¿A quién enviamos?")
            destino = escuchar()
            hablar("¿Qué cantidad?")
            monto_input = escuchar()
            monto = int(''.join(filter(str.isdigit, monto_input)))

            hablar(f"Confirmando {monto} para {destino}. Dime tu PIN.")
            pin = escuchar().replace(" ", "")

            if pin == data['pin']:
                # Descontar de la primera tarjeta por defecto
                if data['tarjetas'][0]['saldo'] >= monto:
                    data['tarjetas'][0]['saldo'] -= monto
                    with open("db.json", "w") as f: json.dump(data, f)
                    hablar(f"Listo. Tu nuevo saldo en {data['tarjetas'][0]['nombre']} es {data['tarjetas'][0]['saldo']}")
                else:
                    hablar("Saldo insuficiente.")
            else:
                hablar("PIN incorrecto.")
        
        elif "salir" in accion:
            hablar("Hasta pronto.")
            break