# Clase 6: Manejo de errores
# ATENCION: El codigo en este archivo esta resuelto de manera incorrecta (no usar como referencia cuando estudien)
# La resolucion correcta desde una perspectiva de la programacion orientada a objetos esta en el archivo main_v2.py

class Personaje:
    def __init__(self, nombre, vida, mana):
        self.nombre = nombre
        self.vida = vida
        self.mana = mana

    def lanzar_hechizo(self, enemigo):
        # devuelve el danio realizado o un string si algo salio mal
        if self.mana < 10:
            # ATENCION:
            # devolver un string es incorrecto desde el punto de vista del polimorfismo.
            # Ya que dependiendo de la rama del if que se tome se devuelve un objeto de distinto tipo
            # (string o int e neste caso)
            return "mana insuficiente"
        if enemigo.vida <= 0:
            return "el enemigo ya esta muerto"
        danio = self.mana * 0.5
        enemigo.vida = enemigo.vida - danio
        self.mana = self.mana - 10
        return danio

# Funcion principal para probar el codigo de los personajes.
def main():
    mago = Personaje("Gandalf", vida=100, mana=15)
    orco = Personaje("Lurk", vida=50, mana=0)

    resultado = mago.lanzar_hechizo(orco)

    # ATENCION
    # el que llama a `mago.lanzar_hechizo(orco)` esta obligado a conocer los strings exactos que puede devolver
    if resultado == "mana insuficiente":
        print("no se pudo lanzar el hechizo: falta mana")
    elif resultado == "el enemigo esta muerto":  # BUG: no coincide con el string que devuelve el metodo
        print("no se pudo lanzar el hechizo: el enemigo ya murio")
    else:
        # si llego aca asumo que salio bien, sera verdad?
        print("hechizo lanzado! danio realizado:", resultado)

    # peor todavia: si nadie chequea el resultado, el error viaja como
    # si fuera un numero y explota lejos de donde se origino. Esto lleva a muchos bugs. 
    otro_resultado = mago.lanzar_hechizo(orco)  # ya no tiene mana
    vida_restante = orco.vida - otro_resultado  # BUG: TypeError: int - str. No se puede restar un string a un entero.



# Estas 2 lineas de codigo sirve para que cuando corramos este archivo como un script,
# con uv run main.py, se ejecute la funcion main.
if __name__ == "__main__":
    main()
