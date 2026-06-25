# =================================================================
# 1. DECLARACIÓN DE ERRORES
# =================================================================
class SaldoInsuficienteError(Exception):
    pass

class MontoInvalidoError(Exception):
    pass

# =================================================================
# 2. CLASES (Cuentas)
# =================================================================
class Cuenta:
    def __init__(self, titular, saldo):
        self.titular = titular
        self.saldo = saldo

    def depositar(self, monto):
        if monto <= 0:
            raise MontoInvalidoError("El monto debe ser mayor a cero.")
        self.saldo = self.saldo + monto

    def extraer(self, monto):
        if monto <= 0:
            raise MontoInvalidoError("El monto debe ser mayor a cero.")
        if monto > self.saldo:
            raise SaldoInsuficienteError("Fondos insuficientes.")
        self.saldo = self.saldo - monto

    def interes_mensual(self):
        return 0

class CajaAhorro(Cuenta):
    def __init__(self, titular, saldo, tasa):
        super().__init__(titular, saldo)
        self.tasa = tasa

    def interes_mensual(self):
        if self.saldo >= 100000:
            return self.saldo * self.tasa
        return 0

class CuentaCorriente(Cuenta):
    def __init__(self, titular, saldo, comision_base, cheques=None):
        super().__init__(titular, saldo)
        self.comision_base = comision_base
        self.cheques = cheques if cheques is not None else []

    def interes_mensual(self):
        cantidad_cheques = len(self.cheques)
        return -(self.comision_base + (cantidad_cheques * 200))

# =================================================================
# 3. CLASE BANCO
# =================================================================
class Banco:
    def __init__(self):
        self.cuentas = []

    def abrir_cuenta(self, cuenta):
        self.cuentas.append(cuenta)

    def patrimonio_total(self):
        suma = 0
        for c in self.cuentas:
            suma = suma + c.saldo
        return suma

    def total_intereses_del_mes(self):
        suma_intereses = 0
        for c in self.cuentas:
            suma_intereses += c.interes_mensual()
        return suma_intereses

# =================================================================
# 4. FUNCIONES Y CONSULTAS
# =================================================================
def transferir(origen, destino, monto):
    origen.extraer(monto)
    destino.depositar(monto)

def cuentas_en_rojo(cuentas):
    return list(filter(lambda c: c.saldo < 0, cuentas))

def crear_ajuste(porcentaje):
    return lambda c: c.saldo * (1 + porcentaje / 100)

def todas_con_fondos(cuentas):
    return all(map(lambda c: c.saldo > 0, cuentas))

def hay_cuenta_rica(cuentas, tope):
    return any(map(lambda c: c.saldo > tope, cuentas))

# =================================================================
# 5. EL MAIN (Para probar todo)
# =================================================================
def main():
    ana = CajaAhorro("Ana", 150000, tasa=0.05)
    beto = CajaAhorro("Beto", 50000, tasa=0.05)
    caro = CuentaCorriente("Caro", 200000, comision_base=1000, cheques=["luz", "gas"])
    dani = CuentaCorriente("Dani", -5000, comision_base=1000)

    banco = Banco()
    banco.abrir_cuenta(ana)
    banco.abrir_cuenta(beto)
    banco.abrir_cuenta(caro)
    banco.abrir_cuenta(dani)

    # --- PROBANDO EXCEPCIONES ---
    try:
        print("Intentando que ANA extraiga 999.999")
        ana.extraer(999999)
    except SaldoInsuficienteError as error:
        print("Fallo la extraccion: Saldo insuficiente")
        
    try:
        print("Probando de que ana deposite -100")
        ana.depositar(-100)
    except MontoInvalidoError as error:
        print("Fallo el deposito: Monto invalido")
        
    try:
        print("Probando transferir sin fondos")
        transferir(caro, ana, 300000)
    except SaldoInsuficienteError as error:
        print("Fallo de transferencia: Saldo insuficiente")

    # --- PROBANDO CONSULTAS Y ORDEN SUPERIOR ---
    print("\n----------------------------------")
    cuentas = [ana, beto, caro, dani]

    print("Interés de Ana:", ana.interes_mensual())
    print("Ajuste de Caro:", caro.interes_mensual())
    print("Patrimonio total:", banco.patrimonio_total())

    en_rojo = cuentas_en_rojo(cuentas)
    print("En rojo:", [c.titular for c in en_rojo])

    con_ajuste = crear_ajuste(10)
    saldos_ajustados = []
    for c in cuentas:
        saldos_ajustados.append(con_ajuste(c))
    print("Saldos con 10 de ajuste:", saldos_ajustados)

    print("¿Todas con fondos?", todas_con_fondos(cuentas))
    print("¿Hay cuenta con más de 100000?", hay_cuenta_rica(cuentas, 100000))

    # --- PRINTS FINALES ---
    print("\n----------------------------------")
    print(f"Saldo Ana: ${ana.saldo} (Nunca le llegó la transferencia fallida de Caro)")
    print(f"Saldo Caro: ${caro.saldo} (No se le descontó nada por fallar la transferencia)")
    print(f"Patrimonio Total del Banco: ${banco.patrimonio_total()}")

if __name__ == "__main__":
    main()