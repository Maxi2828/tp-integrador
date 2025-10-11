from datetime import datetime

# Clase Mensaje
class Mensaje:
    def __init__(self, emisor, receptor, contenido):
        self.emisor = emisor
        self.receptor = receptor
        self.contenido = contenido
        self.fecha = datetime.now()

    def __str__(self):
        return f"[{self.fecha.strftime('%d/%m/%Y %H:%M:%S')}] {self.emisor} → {self.receptor}: {self.contenido}"
    

# Clase Carpeta
class Carpeta:
    def __init__(self, nombre):
        self.nombre = nombre
        self.mensajes = []

    def agregar_mensaje(self, mensaje):
        self.mensajes.append(mensaje)

    def mostrar_mensajes(self):
        print(f"\n Carpeta: {self.nombre}")
        if not self.mensajes:
            print("   (sin mensajes)")
        else:
            for i, msg in enumerate(self.mensajes, start=1):
                print(f"{i}. {msg}")


# Clase Usuario
class Usuario:
    def __init__(self, nombre):
        self.nombre = nombre
        self.entrada = Carpeta("Bandeja de entrada")
        self.enviados = Carpeta("Enviados")

# Clase ServidorCorreo
class ServidorCorreo:
    def __init__(self, nombre_servidor):
        self.nombre_servidor = nombre_servidor
        self.usuarios = {}

    def registrar_usuario(self): # Crea un nuevo usuario
        nombre_usuario = input("Ingrese el nombre del nuevo usuario: ")
        if nombre_usuario in self.usuarios:
            print(f"El usuario '{nombre_usuario}' ya existe.")
        else:
            nuevo = Usuario(nombre_usuario)
            self.usuarios[nombre_usuario] = nuevo
            print(f"Usuario '{nombre_usuario}' registrado correctamente.")

    def enviar_mensaje(self): # Envía un mensaje entre usuarios
        emisor = input("Ingrese el nombre del emisor: ")
        receptor = input("Ingrese el nombre del receptor: ")
        contenido = input("Escriba el mensaje: ")

        if emisor not in self.usuarios:
            print(f"El emisor '{emisor}' no está registrado.")
            return
        if receptor not in self.usuarios:
            print(f"El receptor '{receptor}' no está registrado.")
            return

        mensaje = Mensaje(emisor, receptor, contenido)
        self.usuarios[emisor].enviados.agregar_mensaje(mensaje)
        self.usuarios[receptor].entrada.agregar_mensaje(mensaje)

        print(f"Mensaje enviado de '{emisor}' a '{receptor}'.")

    def mostrar_bandeja(self): # Muestra las bandejas de un usuario
        nombre = input("Ingrese el nombre del usuario: ")
        if nombre not in self.usuarios:
            print(f"El usuario '{nombre}' no existe.")
            return

        user = self.usuarios[nombre]
        print(f"\n--- Bandejas de {nombre} ---")
        user.entrada.mostrar_mensajes()
        user.enviados.mostrar_mensajes()

    def mostrar_usuarios(self): # Muestra todos los usuarios registrados
        print(f"\n Usuarios en el servidor '{self.nombre_servidor}':")
        if not self.usuarios:
            print("   (ninguno todavía)")
        else:
            for usuario in self.usuarios:
                print(f" - {usuario}")


# Programa principal con menú
def main():
    servidor = ServidorCorreo("GMAIL")

    while True:
        print("\n=== SERVIDOR DE CORREO - GMAIL ===")
        print("1. Registrar nuevo usuario")
        print("2. Enviar mensaje")
        print("3. Mostrar bandejas de un usuario")
        print("4. Ver usuarios registrados")
        print("5. Salir")

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
            print("Saliendo del servidor... ¡Hasta luego!")
            break
        else:
            print("Opción inválida, intente nuevamente.")


# Ejecuta el programa
if __name__ == "__main__":
    main()
