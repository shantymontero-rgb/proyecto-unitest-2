import unittest
from decimal import Decimal
from unittest.mock import MagicMock, patch

from app.modelos.cliente import Cliente
from app.modelos.pedido import EstadoPedido, Pedido
from app.modelos.producto import Producto

from app.negocio.nego_detalle_pedido import (
    _recalcular_total_pedido,
    _validar_cantidad,
    crear_detalle_pedido,
)

from app.negocio.nego_pedido import crear_pedido


class TestNegocioPedido(unittest.TestCase):

    @patch(
        "app.negocio.nego_pedido.guardar_pedido",
        return_value=1
    )
    def test_crear_pedido_inicia_total_en_cero(
        self,
        mock_guardar_pedido
    ):

        cliente = Cliente(
            id_cliente=1,
            rut_cliente="12.345.678-5",
            nombre_cliente="Juan",
            apellido_cliente="Perez",
            correo_cliente="juan@gmail.com",
            fecha_nacimiento_cliente="2000-12-25",
        )

        pedido = crear_pedido(cliente)

        self.assertIsNotNone(pedido)

        self.assertEqual(
            pedido.cliente_pedido,
            cliente
        )

        self.assertEqual(
            pedido.total_pedido,
            Decimal("0.00")
        )

        self.assertEqual(
            pedido.estado_pedido,
            EstadoPedido.PEND
        )

        self.assertTrue(
            pedido.pedido_habilitado
        )

        mock_guardar_pedido.assert_called_once_with(
            pedido
        )

    def test_cantidad_detalle_debe_ser_entero_mayor_que_cero(
        self
    ):

        _validar_cantidad(1)
        _validar_cantidad(5)

        for cantidad in (
            0,
            -1,
            1.5,
            "2",
            True
        ):

            with self.subTest(cantidad=cantidad):

                with self.assertRaises(ValueError):
                    _validar_cantidad(cantidad)

    @patch(
        "app.negocio.nego_detalle_pedido._recalcular_total_pedido"
    )
    @patch(
        "app.negocio.nego_detalle_pedido.guardar_detalle_pedido",
        return_value=1
    )
    @patch(
        "app.negocio.nego_detalle_pedido.base_datos"
    )
    def test_crear_detalle_copia_precio_producto(
        self,
        mock_base_datos,
        mock_guardar_detalle,
        mock_recalcular
    ):

        conexion = MagicMock()
        mock_base_datos.return_value = conexion

        pedido = Pedido(
            id_pedido=1
        )

        producto = Producto(
            id_producto=1,
            sku_producto="SKU001",
            nombre_producto="Teclado",
            descripcion_producto="Teclado mecanico USB",
            precio_producto=Decimal("19990.00"),
            producto_habilitado=True,
        )

        detalle = crear_detalle_pedido(
            pedido,
            producto,
            2
        )

        self.assertEqual(
            detalle.id_pedido,
            pedido
        )

        self.assertEqual(
            detalle.id_producto,
            producto
        )

        self.assertEqual(
            detalle.cantidad,
            2
        )

        self.assertEqual(
            detalle.precio_unitario,
            Decimal("19990.00")
        )

        self.assertTrue(
            detalle.habilitado
        )

        mock_guardar_detalle.assert_called_once_with(
            detalle
        )

        mock_recalcular.assert_called_once_with(
            pedido
        )

        conexion.atomic.assert_called_once()

    @patch(
        "app.negocio.nego_detalle_pedido.guardar_pedido",
        return_value=1
    )
    @patch(
        "app.negocio.nego_detalle_pedido.detalle_pedido_por_pedido"
    )
    def test_recalcular_total_pedido_suma_solo_detalles_habilitados(
        self,
        mock_detalles,
        mock_guardar_pedido
    ):

        pedido = Pedido(
            id_pedido=1,
            total_pedido=Decimal("0.00")
        )

        detalle_1 = MagicMock()
        detalle_1.precio_unitario = Decimal("10000.00")
        detalle_1.cantidad = 2
        detalle_1.habilitado = True

        detalle_2 = MagicMock()
        detalle_2.precio_unitario = Decimal("5000.00")
        detalle_2.cantidad = 1
        detalle_2.habilitado = True

        detalle_deshabilitado = MagicMock()
        detalle_deshabilitado.precio_unitario = Decimal("99999.00")
        detalle_deshabilitado.cantidad = 10
        detalle_deshabilitado.habilitado = False

        mock_detalles.return_value = [
            detalle_1,
            detalle_2,
            detalle_deshabilitado,
        ]

        _recalcular_total_pedido(pedido)

        self.assertEqual(
            pedido.total_pedido,
            Decimal("25000.00")
        )

        mock_detalles.assert_called_once_with(1)

        mock_guardar_pedido.assert_called_once_with(
            pedido
        )


if __name__ == "__main__":
    unittest.main()
