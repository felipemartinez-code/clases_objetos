# Tests para main_v2: verificamos que lanzar_hechizo arroja las excepciones correctas. 
# Se corre con el siguiente comando: uv run pytest

import pytest

from main_v2 import EnemigoMuerto, ManaInsuficiente, Personaje


def test_sin_mana_suficiente_arroja_mana_insuficiente():
    mago = Personaje("Gandalf", vida=100, mana=5)
    orco = Personaje("Azog", vida=50, mana=0)

    # el test pasa (verde) si el codigo de adentro del with arroja ManaInsuficiente,
    # y falla (rojo) si no se arroja nada (o se arroja otra excepcion distinta a ManaInsuficiente)
    with pytest.raises(ManaInsuficiente):
        mago.lanzar_hechizo(orco)


def test_atacar_enemigo_muerto_arroja_enemigo_muerto():
    mago = Personaje("Gandalf", vida=100, mana=20)
    orco = Personaje("Azog", vida=0, mana=0)

    with pytest.raises(EnemigoMuerto):
        mago.lanzar_hechizo(orco)


def test_el_mensaje_del_error_lleva_los_datos():
    # las excepciones son objetos: ademas del tipo podemos verificar
    # el mensaje que llevan adentro, con el parametro match
    mago = Personaje("Gandalf", vida=100, mana=5)
    orco = Personaje("Azog", vida=50, mana=0)

    with pytest.raises(ManaInsuficiente, match="Gandalf tiene 5 de mana"):
        mago.lanzar_hechizo(orco)


def test_si_falla_no_se_modifica_el_estado():
    # el raise corta la funcion antes de descontar mana y vida
    mago = Personaje("Gandalf", vida=100, mana=5)
    orco = Personaje("Azog", vida=50, mana=0)

    with pytest.raises(ManaInsuficiente):
        mago.lanzar_hechizo(orco)

    assert mago.mana == 5
    assert orco.vida == 50


def test_camino_feliz_no_arroja_nada():
    # si hay mana y el enemigo esta vivo, no hay excepcion y la funcion devuelve el danio
    mago = Personaje("Gandalf", vida=100, mana=15)
    orco = Personaje("Azog", vida=50, mana=0)

    danio = mago.lanzar_hechizo(orco)

    assert danio == 7.5
    assert orco.vida == 42.5
    assert mago.mana == 5


@pytest.mark.skip(reason="ejercicio: completar el assert y sacar este skip")
def test_enemigo_muerto_y_sin_mana_cual_gana():
    # TODO(ejercicio): si el mago NO tiene mana y el enemigo YA esta muerto,
    # las dos condiciones de error se cumplen a la vez... pero solo una
    # excepcion puede arrojarse. Mira el orden de los if en lanzar_hechizo,
    # decidi cual esperas, y escribi el pytest.raises correspondiente.
    mago = Personaje("Gandalf", vida=100, mana=0)
    orco = Personaje("Azog", vida=0, mana=0)
