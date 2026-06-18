# Café Delta — solución de los puntos 1 a 5


# Punto 1 y 2: el menú, bebidas y postres
class Producto:
    def __init__(self, nombre, precio_base, apto_vegano, stock,
                 tipo="simple", ml=0, toppings=None):
        self.nombre = nombre
        self.precio_base = precio_base
        self.apto_vegano = apto_vegano
        self.stock = stock
        self.tipo = tipo
        self.ml = ml
        self.toppings = toppings if toppings is not None else []

    def precio(self):
        if self.tipo == "bebida":
            if self.ml >= 500:
                return round(self.precio_base * 1.4, 2)
            return self.precio_base
        elif self.tipo == "postre":
            recargo = 0
            for _ in self.toppings:
                recargo = recargo + 300
            return self.precio_base + recargo
        else:
            return self.precio_base


# Punto 3 y 5: el pedido
class Pedido:
    def __init__(self):
        self.productos = []

    def agregar(self, producto):
        if producto.stock <= 0:
            return "Error: " + producto.nombre + " no tiene stock"
        self.productos.append(producto)
        producto.stock = producto.stock - 1

    def total(self):
        suma = 0
        for p in self.productos:
            suma = suma + p.precio()
        return suma

    def cobrar(self):
        if len(self.productos) == 0:
            return "Error: el pedido está vacío"
        total = 0
        for p in self.productos:
            total = total + p.precio()
        return total


# Punto 4: promociones y consultas
def menu_apto_vegano(productos):
    resultado = []
    for p in productos:
        if p.apto_vegano:
            resultado.append(p)
    return resultado


def crear_descuento(porcentaje):
    def aplicar(producto):
        return producto.precio() * (1 - porcentaje / 100)
    return aplicar


def hay_stock_de_todo(productos):
    for p in productos:
        if p.stock <= 0:
            return False
    return True


def hay_opcion_barata(productos, tope):
    for p in productos:
        if p.precio() < tope:
            return True
    return False


def main():
    cafe = Producto("Café americano", 2000, True, 10, tipo="bebida", ml=250)
    latte = Producto("Latte", 2800, False, 3, tipo="bebida", ml=500)
    brownie = Producto("Brownie", 3500, False, 0, tipo="postre",
                       toppings=["dulce de leche", "nueces"])
    ensalada = Producto("Ensalada de frutas", 3000, True, 5, tipo="postre")
    menu = [cafe, latte, brownie, ensalada]

    print("Precio del latte:", latte.precio())
    print("Precio del brownie:", brownie.precio())

    pedido = Pedido()
    pedido.agregar(latte)
    pedido.agregar(ensalada)
    print("Total del pedido:", pedido.cobrar())

    veganos = menu_apto_vegano(menu)
    print("Aptos veganos:", [p.nombre for p in veganos])

    con_promo = crear_descuento(10)
    precios_promo = []
    for p in menu:
        precios_promo.append(con_promo(p))
    print("Precios con 10% off:", precios_promo)

    print("¿Hay stock de todo?", hay_stock_de_todo(menu))
    print("¿Hay opción barata (< 2500)?", hay_opcion_barata(menu, 2500))

    # Punto 5: cobrar un pedido vacío
    resultado = Pedido().cobrar()
    if type(resultado) == str:
        print("No se pudo cobrar:", resultado)

    # Punto 5: agregar un producto agotado
    error = pedido.agregar(brownie)
    if error is not None:
        print("No se pudo agregar:", error)


if __name__ == "__main__":
    main()
