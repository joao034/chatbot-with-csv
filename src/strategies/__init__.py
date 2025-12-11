from .inventario import consultar_inventario
from .ventas import consultar_ventas

estrategias = {
    'inventario': consultar_inventario,
    'ventas': consultar_ventas
}