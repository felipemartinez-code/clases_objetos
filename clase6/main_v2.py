# Clase 6: Manejo de errores

# los errores ahora son clases: tienen nombre propio y pueden contener atributos
# en las excepciones, los atributos sirven para poder agregar datos contextuales a las mismas
# en este caso: que personaje no tiene mana y cuanto mana requiere.
class ManaInsuficiente(Exception):
    def __init__(self, personaje, cantidad_de_mana_requerida):
        self.personaje = personaje
        self.cantidad_de_mana_requerida = cantidad_de_mana_requerida

    # definiendo el metodo __str__ podemos cambiar como se imprime una Exception.
    # Esto es util si queremos un mensaje personalizado que haga uso de los atributos de la misma. 
    # en este caso damos mas informacion utilizando los atributos personaje y cantidad_de_mana_requerida.
    def __str__(self):
        nombre_del_personaje = self.personaje.nombre
        mana_que_necesita = self.cantidad_de_mana_requerida
        mana_que_tiene = self.personaje.mana
        return f"el personaje #{nombre_del_personaje} necesita #{mana_que_necesita}, pero tiene #{mana_que_tiene}"

# En caso de que no definamos __init__, el argumento que toma una Exception y sus subclases al ser creada es un string (el mensaje)
# En este caso cuando instancio un objeto de clase EnemigoMuerto, debo pasar el mensaje:
# EnemigoMuerto("Mensaje")
class EnemigoMuerto(Exception):
    pass

class Personaje:
    def __init__(self, nombre, vida, mana):
        self.nombre = nombre
        self.vida = vida
        self.mana = mana

    def lanzar_hechizo(self, enemigo):
        # ahora SIEMPRE devuelve el danio realizado (un numero)
        # el raise de una Excepcion no cuenta como valor de retorno.
        if self.mana < 10:
            raise ManaInsuficiente(self, 10)
        if enemigo.vida <= 0:
            raise EnemigoMuerto(f"{enemigo.nombre} ya esta muerto")
        danio = self.mana * 0.5
        enemigo.vida = enemigo.vida - danio
        self.mana = self.mana - 10
        return danio


def main():
    mago = Personaje("Gandalf", vida=100, mana=15)
    orco = Personaje("Azog", vida=50, mana=0)

    # el camino feliz queda adentro del try, cada error en su except.
    # si me equivoco en el nombre de la excepcion, el interprete me avisa
    # (mejora frente a usar strings)
    try:
        danio = mago.lanzar_hechizo(orco)
        print("hechizo lanzado! danio realizado:", danio)
    except ManaInsuficiente as error:
        print("no se pudo lanzar el hechizo:", error)
    except EnemigoMuerto as error:
        print("no se pudo lanzar el hechizo:", error)
    except ValueError:
        print("paso algo malo")
    # poniendo en el except a Exception, atrapo toda posible Exception y sus subclases
    except Exception as error:
        print(f"Ocurrio un error :( : {error})")

    # si nadie maneja la exception, el programa se corta en este momento,
    # con un traceback que nombra el error y apunta al raise original
    otro_danio = mago.lanzar_hechizo(orco)  # ya no tiene mana
    vida_restante = orco.vida - otro_danio  # esta linea nunca llega a ejecutarse
    print("vida restante del orco:", vida_restante)


if __name__ == "__main__":
    main()
