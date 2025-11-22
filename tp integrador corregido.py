from datetime import datetime
import heapq
from collections import deque

# ==========================
# Clase Mensaje
# ==========================
class Mensaje:
    def __init__(self, emisor, receptor, contenido, urgente=False):
        self.emisor = emisor
        self.receptor = receptor
        self.contenido = contenido
        self.urgente = urgente
        self.fecha = datetime.now()

    def __str__(self):
        etiqueta = " URGENTE! " if self.urgente else ""
        return (f"[{self.fecha.strftime('%d/%m/%Y %H:%M:%S')}] "
                f"{self.emisor} → {self.receptor}\n"
                f"   Mensaje: {self.contenido}")


# ==========================
# Clase Carpeta (estructura de árbol)
# ==========================
class Carpeta:
    def __init__(self, nombre):
        self.nombre = nombre
        self.archivos = []
        self.subcarpetas = []
        self.mensajes = []

    def agregar_archivo(self, archivo):
        self.archivos.append(archivo)

    def agregar_subcarpeta(self, carpeta):
        self.subcarpetas.append(carpeta)

    def agregar_mensaje(self, mensaje):
        self.mensajes.append(mensaje)

    def mostrar_mensajes(self):
        print(f"\n Carpeta: {self.nombre}")
        if not self.mensajes:
            print("   (sin mensajes)")
        else:
            for i, msg in enumerate(self.mensajes, start=1):
                print(f"\n--- Mensaje {i} ---")
                print(msg)

    def __str__(self):
        return f"{self.nombre}"


# ==========================
# Clase Usuario
# ==========================
class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre
        self.entrada = Carpeta("Bandeja de entrada")
        self.enviados = Carpeta("Enviados")
    
     # Filtros automáticos → diccionario
        self.filtros = {
            "promociones": ["oferta", "rebaja", "promo"],
            "trabajo": ["curriculum", "empleo", "entrevista"],
            "personal": ["hola", "como estas", "familia"],
        }
 # Carpetas creadas por filtros
        self.carpetas_filtro = {
            "promociones": Carpeta("Promociones"),
            "trabajo": Carpeta("Trabajo"),
            "personal": Carpeta("Personal")
        }
 # Cola de prioridad para mensajes urgentes
        self.urgentes = []  # heapq (priority queue)

    # ---------- Aplica filtros y prioridades ----------
    def procesar_mensaje(self, mensaje):
     # Si es urgente → va a cola de prioridad
        if mensaje.urgente:
         heapq.heappush(self.urgentes, (0, mensaje))
         return
     
     # Si coincide con un filtro → se guarda en esa carpeta
        contenido = mensaje.contenido.lower()
        for carpeta, palabras in self.filtros.items():
            if any(pal in contenido for pal in palabras):
                self.carpetas_filtro[carpeta].agregar_mensaje(mensaje)
                return
      # Si no coincide → va a bandeja normal
        self.entrada.agregar_mensaje(mensaje)

# Muestra urgentes
    def mostrar_urgentes(self):
        print("\n--- URGENTES ---")
        if not self.urgentes:
         print("  (no hay urgentes)")
        else:
         while self.urgentes:
             _, msg = heapq.heappop(self.urgentes)
             print(msg)    


# ==========================
# Clase ServidorCorreo
# ==========================
class ServidorCorreo: 
    def __init__(self, nombre_servidor):
        self.nombre_servidor = nombre_servidor
        self.usuarios = {}
        self.conexiones = []  # conexiones con otros servidores (grafo)

    def conectar(self, otro):
        if not isinstance(otro, ServidorCorreo):
            print("Error: solo se puede conectar con otro servidor.")
            return
        
        if otro not in self.conexiones:
            self.conexiones.append(otro)

        if self not in otro.conexiones:
            otro.conexiones.append(self)

    def registrar_usuario(self):
        nombre = input("Nombre de usuario: ")
        if nombre in self.usuarios:
            print("Ya existe.")
        else:
            self.usuarios[nombre] = Usuario(nombre)
            print("Usuario creado.")

    # envío por BFS por la red de servidores
    def enviar_por_red(self, destino):
        visitados = set()
        cola = deque([(self, [self.nombre_servidor])])

        while cola:
            actual, camino = cola.popleft()

            if actual.nombre_servidor == destino.nombre_servidor:
                return camino

            visitados.add(actual)

            for vecino in actual.conexiones:
                if vecino not in visitados:
                    cola.append((vecino, camino + [vecino.nombre_servidor]))

        return None

    # enviar mensaje
    def enviar_mensaje(self, red):
        emisor = input("Emisor: ")
        receptor_full = input("Receptor (servidor:usuario): ")

        try:
            serv_dest, receptor_usr = receptor_full.split(":")
        except:
            print("Formato inválido. Usa servidor:usuario")
            return

        contenido = input("Contenido: ")
        urgente = input("¿Urgente? (s/n): ").lower() == "s"

        # Validaciones
        if serv_dest not in red:
            print("Servidor inexistente.")
            return

        servidor_destino = red[serv_dest]

        if emisor not in self.usuarios:
            print("El emisor no existe en este servidor.")
            return

        if receptor_usr not in servidor_destino.usuarios:
            print("El receptor no existe en ese servidor.")
            return

        ruta = self.enviar_por_red(servidor_destino)
        if not ruta:
            print("No hay ruta disponible.")
            return

        print(f"Ruta encontrada: {' → '.join(ruta)}")

        # Crear mensaje
        msg = Mensaje(emisor, receptor_usr, contenido, urgente)

        # Guardar en la carpeta "Enviados"
        self.usuarios[emisor].enviados.agregar_mensaje(msg)

        # Procesar en el receptor (filtros, urgencia, cola, etc.)
        servidor_destino.usuarios[receptor_usr].procesar_mensaje(msg)

        print("Mensaje enviado correctamente.")

    def mostrar_bandeja(self):
        nombre = input("Ingrese el nombre del usuario: ")
        if nombre not in self.usuarios:
            print(f" El usuario '{nombre}' no existe.")
            return

        user = self.usuarios[nombre]
        print(f"\n Bandejas de {nombre}:")
        print("\nBandeja de entrada:")
        user.entrada.mostrar_mensajes()
        print("\nEnviados:")
        user.enviados.mostrar_mensajes()

    def mostrar_usuarios(self):
        print(f"\n Usuarios en el servidor '{self.nombre_servidor}':")
        if not self.usuarios:
            print("   (ninguno todavía)")
        else:
            for usuario in self.usuarios:
                print(f" - {usuario}")


# ==========================
# Función para mostrar estructura de carpetas (tipo árbol)
# ==========================
def mostrar_estructura(carpeta, nivel=0):
    indentacion = "    " * nivel
    print(f"{indentacion}{carpeta.nombre}")

    for archivo in carpeta.archivos:
        print(f"{indentacion}├── {archivo}")

    for subcarpeta in carpeta.subcarpetas:
        mostrar_estructura(subcarpeta, nivel + 1)
# ==========================
# Programa principal con menú
# ==========================
def main():
    servidor = ServidorCorreo("GMAIL")

    # creaión de red de servidores(grafo)
gmail = ServidorCorreo("gmail")
outlook = ServidorCorreo("outlook")

    # conexiones en grafo
gmail.conectar(outlook)   

red = {
    "gmail": gmail,
    "outlook": outlook   
}
    
servidor_actual = gmail

# Crear estructura de carpetas tipo árbol (ejemplo)
raiz = Carpeta("Raíz")
src = Carpeta("src")
docs = Carpeta("docs")
raiz.agregar_subcarpeta(src)
raiz.agregar_subcarpeta(docs)
raiz.agregar_archivo("README.md")

componentes = Carpeta("componentes")
servicios = Carpeta("servicios")
src.agregar_subcarpeta(componentes)
src.agregar_subcarpeta(servicios)
src.agregar_archivo("index.js")

componentes.agregar_archivo("Boton.jsx")
utilidades = Carpeta("utilidades")
componentes.agregar_subcarpeta(utilidades)
utilidades.agregar_archivo("helper.js")
docs.agregar_archivo("manual.pdf")

while True:
        print("\n=== MENU SERVDOR")
        print("1. Registrar nuevo usuario")
        print("2. Enviar mensaje por red")
        print("3. Mostrar bandejas de un usuario")
        print("4. Ver usuarios registrados")
        print("5. Mostrar estructura de carpetas")
        print("6. ver mensajes urgentes")
        print("7. cambiar de servidor")
        print("8. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            servidor.registrar_usuario()
        elif opcion == "2":
            servidor.enviar_mensaje()
        elif opcion == "3":
            servidor.mostrar_bandeja()
        elif opcion == "4":
            servidor.mostrar_usuarios()
        elif opcion == "5":
            mostrar_estructura(raiz)
        elif opcion == "6":
            usuario = input("Usuario: ")
            if usuario in servidor_actual.usuarios:
                servidor_actual.usuarios[usuario].mostrar_urgentes()
        elif opcion == "7":
            nuevo = input("ingrese nombre del servidor (gmail/outlook): ")
            if nuevo in red:
                servidor_actual = red[nuevo]
            else:
                print("este servidor no existe!")
        elif opcion == "8":
            print(" Saliendo del servidor... ¡Hasta luego!")
            break
        else:
            print(" Opción inválida, intente nuevamente.")

if __name__ == "__main__":
    main()

