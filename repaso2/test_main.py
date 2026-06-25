import pytest
from main import (CajaAhorro, CuentaCorriente, Banco, SaldoInsuficienteError, MontoInvalidoError, transferir)

# =========================================================
# PUNTO 2: Cajas de ahorro y cuentas corrientes
# Testeamos que el polimorfismo del cálculo de interés funcione bien.
# =========================================================
def test_interes_caja_ahorro_aplica_si_supera_el_minimo():
    ana = CajaAhorro("Ana", 150000, 0.05)
    # 150000 * 0.05 = 7500
    assert ana.interes_mensual() == 7500

def test_interes_caja_ahorro_es_cero_si_no_llega_al_minimo():
    beto = CajaAhorro("Beto", 50000, 0.05)
    # Menos de 100.000, no da interés
    assert beto.interes_mensual() == 0

def test_interes_cuenta_corriente_cobra_comision_y_cheques():
    caro = CuentaCorriente("Caro", 200000, 1000, ["luz", "gas"])
    # 1000 (base) + (2 cheques * 200) = 1400. Al ser cobro es negativo.
    assert caro.interes_mensual() == -1400

# =========================================================
# PUNTO 3: El banco
# Testeamos que el banco pueda agrupar cuentas y sumar sus saldos.
# =========================================================
def test_banco_suma_patrimonio_total():
    banco = Banco()
    banco.abrir_cuenta(CajaAhorro("Ana", 150000, 0.05))
    banco.abrir_cuenta(CuentaCorriente("Caro", 200000, 1000))
    
    # 150000 + 200000 = 350000
    assert banco.patrimonio_total() == 350000

# =========================================================
# PUNTO 5: Operar sin mentiras (Manejo de Errores)
# Testeamos que las excepciones vuelen por los aires cuando corresponde.
# =========================================================
def test_extraer_mas_del_saldo_lanza_error():
    beto = CajaAhorro("Beto", 50000, 0.05)
    
    # Atrapamos la explosión por falta de fondos
    with pytest.raises(SaldoInsuficienteError):
        beto.extraer(90000)

def test_depositar_monto_negativo_lanza_error():
    ana = CajaAhorro("Ana", 150000, 0.05)
    
    # Atrapamos la explosión por monto inválido
    with pytest.raises(MontoInvalidoError):
        ana.depositar(-500)

def test_transferencia_falla_por_saldo_y_no_toca_la_plata():
    pobre = CajaAhorro("Pobre", 100, 0.05)
    rico = CajaAhorro("Rico", 100000, 0.05)
    
    # La transferencia tiene que fallar porque "Pobre" intenta pasar $5000
    with pytest.raises(SaldoInsuficienteError):
        transferir(pobre, rico, 5000)
    
    # Comprobamos que como la función falló a la mitad, los saldos NUNCA cambiaron
    assert pobre.saldo == 100
    assert rico.saldo == 100000