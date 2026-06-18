# Repaso: Café Delta

La cafetería **Café Delta** necesita un sistema para administrar su menú y cobrar los pedidos de sus clientes. El sistema tiene que representar los productos del menú, calcular el precio de cada uno según sus características, armar pedidos y cobrarlos sin sorpresas.

Trabajá en un único archivo `main.py`. Cada punto usa lo construido en el anterior.

## Punto 1: el menú

Modelar la clase `Producto` con:

- `nombre` (string), `precio_base` (número), `apto_vegano` (booleano) y `stock` (entero).
- Un método `precio()` que, por ahora, devuelve el precio base.

## Punto 2: bebidas y postres

No todos los productos se cobran igual:

- **`Bebida`**: además de lo anterior, tiene un tamaño en mililitros (`ml`). Las bebidas de **500 ml o más** pagan un **40% de recargo** sobre el precio base.
- **`Postre`**: tiene una lista de `toppings` (strings). Cada topping suma **$300** al precio base.

Requisitos:

- `Bebida` y `Postre` deben **heredar** de `Producto` y redefinir `precio()`.
- Los constructores deben reutilizar el de `Producto` mediante `super()`, sin copiar la asignación de atributos.
- El precio debe resolverse por **polimorfismo**: está prohibido preguntar de qué tipo es un producto (nada de `isinstance` ni atributos tipo `producto.tipo == "bebida"`).

## Punto 3: el pedido

Modelar la clase `Pedido`:

- Un pedido nuevo empieza **vacío**.
- `agregar(producto)`: agrega un producto al pedido.
- `total()`: devuelve la suma de los precios de todos sus productos.

`Pedido` no debe saber si tiene bebidas, postres o productos a secas: le pide a cada uno su `precio()` y el polimorfismo hace el resto.

## Punto 4: promociones y consultas

Implementar las siguientes funcionalidades:

- `menu_apto_vegano(productos)`: dada una lista de productos, devuelve la lista de los aptos veganos.
- `crear_descuento(porcentaje)`: devuelve una **función** que recibe un producto y devuelve su precio con el descuento aplicado. Por ejemplo, `con_promo = crear_descuento(10)` permite calcular los precios del happy hour con `list(map(con_promo, productos))`.
- `hay_stock_de_todo(productos)`: `True` si **todos** los productos tienen `stock > 0`.
- `hay_opcion_barata(productos, tope)`: `True` si **al menos un** producto tiene precio menor que `tope`.

## Punto 5: cobrar sin mentiras

Llega el momento de cobrar, y con él los problemas:

- `Pedido.cobrar()`: devuelve el total, pero si el pedido está **vacío** debe lanzar la excepción `PedidoVacioError`.
- `Pedido.agregar(producto)`: si el producto **no tiene stock**, debe lanzar la excepción `SinStockError`. Si tiene, se agrega al pedido y su stock baja en 1.

Requisitos:

- `PedidoVacioError` y `SinStockError` deben ser clases propias que hereden de `Exception`.
- Está **prohibido** señalar errores devolviendo strings o `None` 
- Escribir un `main()` que arme un pedido, lo cobre, y muestre con `try/except` qué pasa al cobrar un pedido vacío y al agregar un producto agotado.

## Ejemplo

Con este menú:

| Producto           | Tipo            | Precio base | Apto vegano | Stock |
|--------------------|-----------------|------------:|-------------|------:|
| Café americano     | Bebida, 250 ml  | $2.000      | sí          | 10    |
| Latte              | Bebida, 500 ml  | $2.800      | no          | 3     |
| Brownie            | Postre          | $3.500      | no          | 0     |
| Ensalada de frutas | Postre          | $3.000      | sí          | 5     |

- El latte cuesta $2.800 × 1,4 = **$3.920** (tiene 500 ml, paga el recargo).
- Un brownie con dos toppings (dulce de leche y nueces) cuesta $3.500 + 2 × $300 = **$4.100**... pero agregarlo a un pedido lanza `SinStockError` (stock 0).
- Un pedido con el latte y la ensalada de frutas totaliza $3.920 + $3.000 = **$6.920**.
- `crear_descuento(10)` aplicado al café americano da **$1.800**.
- `hay_stock_de_todo(menu)` da `False` (el brownie está agotado); `hay_opcion_barata(menu, 2500)` da `True`.

## Tests

Escribir tests con `pytest` para los puntos 2, 3 y 5.
