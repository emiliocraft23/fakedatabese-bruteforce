 Arquitectura del Proyecto
El proyecto consta de un backend monolítico y dos scripts que representan diferentes estrategias de ataque:

main.py: Es el servidor web. Implementa un CRUD básico para la gestión de usuarios (Crear, Leer, Actualizar, Eliminar) y un endpoint de /login. Al iniciar, genera automáticamente una base de datos local (users.db) con tres usuarios predeterminados:

admin / abc

invitado / 12345

root / toor

ataque_diccionario.py (Opcional): Un script que simula un ataque usando una lista predefinida de contraseñas comunes (estilo rockyou.txt). Es letal y rápido si el usuario utiliza contraseñas genéricas.

ataque_puro.py: El script principal del experimento. Genera combinaciones alfanuméricas de forma incremental (a, b, c... aa, ab, ac...) y las envía contra la API hasta encontrar una coincidencia exacta.

Instrucciones de Ejecución
1. Levantar la API
Abre una terminal en la carpeta del proyecto y ejecuta el servidor de desarrollo:

Bash
uvicorn main:app --reload
La API estará disponible en: http://127.0.0.1:8000

Puedes explorar la documentación interactiva (Swagger) en: http://127.0.0.1:8000/docs

2. Ejecutar el Ataque
Abre una segunda terminal (dejando la API corriendo en la primera) y ejecuta el script de ataque:

Bash
python ataque_puro.py
Conceptos Clave Aprendidos en el Laboratorio
Durante la construcción de este experimento, se demostraron los siguientes principios de ciberseguridad y redes:

El poder de la longitud de la contraseña: Una contraseña de 3 caracteres (abc) cae en un par de segundos (aprox. 1,300 intentos). Una de 4 caracteres (toor) tarda miles de intentos más, demostrando que la seguridad crece exponencialmente por cada carácter añadido.

Agotamiento de Puertos (Port Exhaustion): Ejecutar miles de peticiones HTTP abriendo y cerrando conexiones (requests.post()) colapsa rápidamente el sistema operativo y el servidor.

Connection Pooling (Sesiones HTTP): Para lograr un ataque de fuerza bruta eficiente y estable sin colapsar la máquina local, es vital mantener el túnel TCP abierto utilizando requests.Session(). Esto permite enviar miles de peticiones por segundo de forma sostenida.

La necesidad del Rate Limiting: Al quitar las defensas del endpoint /login, el sistema quedó a merced del atacante. En un entorno de producción, bloquear la IP o la cuenta tras 5 intentos fallidos (devolviendo un error HTTP 429 Too Many Requests) neutraliza por completo la efectividad de este tipo de scripts.
