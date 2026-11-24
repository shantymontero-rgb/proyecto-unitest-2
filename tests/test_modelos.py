import unittest
from decimal import Decimal
from datetime import datetime

from app.modelos.cliente import Cliente
from app.modelos.producto import Producto
from app.modelos.pedido import Pedido, EstadoPedido
from app.modelos.detalle_pedido import DetallePedido


class TestCliente(unittest.TestCase):

    def test_creacion_cliente(self):

        cliente = Cliente(
            id_cliente=1,
            rut_cliente="12.345.678-5",
            nombre_cliente="Juan",
            apellido_cliente="Perez",
            correo_cliente="juan@gmail.com",
            fecha_nacimiento_cliente="2000-12-25",
        )

        self.assertEqual(cliente.id_cliente, 1)

        self.assertEqual(
            cliente.rut_cliente,
            "12.345.678-5"
        )

        self.assertNotEqual(
            cliente.rut_cliente,
            "12.345.678-9"
        )

        self.assertEqual(
            cliente.nombre_cliente,
            "Juan"
        )

        self.assertNotEqual(
            cliente.nombre_cliente,
            "Hola"
        )

        self.assertEqual(
            cliente.correo_cliente,
            "juan@gmail.com"
        )

        self.assertEqual(
            cliente.fecha_nacimiento_cliente,
            "2000-12-25"
        )


class TestProducto(unittest.TestCase):

    def test_creacion_producto(self):

        producto = Producto(
            id_producto=1,
            sku_producto="SKU001",
            nombre_producto="Teclado",
            descripcion_producto="Teclado mecanico USB",
            precio_producto=Decimal("19990.00"),
            producto_habilitado=True,
        )

        self.assertEqual(
            producto.id_producto,
            1
        )

        self.assertEqual(
            producto.sku_producto,
            "SKU001"
        )

        self.assertNotEqual(
            producto.sku_producto,
            "SKU999"
        )

        self.assertEqual(
            producto.nombre_producto,
            "Teclado"
        )

        self.assertNotEqual(
            producto.nombre_producto,
            "Mouse"
        )

        self.assertEqual(
            producto.descripcion_producto,
            "Teclado mecanico USB"
        )

        self.assertEqual(
            producto.precio_producto,
            Decimal("19990.00")
        )

        self.assertTrue(
            producto.producto_habilitado
        )


class TestPedido(unittest.TestCase):

    def test_creacion_pedido(self):

        cliente = Cliente(
            id_cliente=1,
            rut_cliente="12.345.678-5",
            nombre_cliente="Juan",
            apellido_cliente="Perez",
            correo_cliente="juan@gmail.com",
            fecha_nacimiento_cliente="2000-12-25",
        )

        fecha = datetime(
            2026,
            11,
            23,
            12,
            0,
            0
        )

        pedido = Pedido(
            id_pedido=1,
            cliente_pedido=cliente,
            fecha_pedido=fecha,
            total_pedido=Decimal("39980.00"),
            estado_pedido=EstadoPedido.PEND,
            pedido_habilitado=True,
        )

        self.assertEqual(
            pedido.id_pedido,
            1
        )

        self.assertEqual(
            pedido.cliente_pedido,
            cliente
        )

        self.assertEqual(
            pedido.fecha_pedido,
            fecha
        )

        self.assertEqual(
            pedido.total_pedido,
            Decimal("39980.00")
        )

        self.assertEqual(
            pedido.estado_pedido,
            EstadoPedido.PEND
        )

        self.assertNotEqual(
            pedido.estado_pedido,
            EstadoPedido.CANC
        )

        self.assertTrue(
            pedido.pedido_habilitado
        )


class TestDetallePedido(unittest.TestCase):

    def test_creacion_detalle_pedido(self):

        cliente = Cliente(
            id_cliente=1,
            rut_cliente="12.345.678-5",
            nombre_cliente="Juan",
            apellido_cliente="Perez",
            correo_cliente="juan@gmail.com",
            fecha_nacimiento_cliente="2000-12-25",
        )

        producto = Producto(
            id_producto=1,
            sku_producto="SKU001",
            nombre_producto="Teclado",
            descripcion_producto="Teclado mecanico USB",
            precio_producto=Decimal("19990.00"),
            producto_habilitado=True,
        )

        pedido = Pedido(
            id_pedido=1,
            cliente_pedido=cliente,
            fecha_pedido=datetime(
                2026,
                11,
                23,
                12,
                0,
                0
            ),
            total_pedido=Decimal("39980.00"),
            estado_pedido=EstadoPedido.PEND,
            pedido_habilitado=True,
        )

        detalle = DetallePedido(
            id_detalle_pedido=1,
            id_pedido=pedido,
            id_producto=producto,
            cantidad=2,
            precio_unitario=Decimal("19990.00"),
            habilitado=True,
        )

        self.assertEqual(
            detalle.id_detalle_pedido,
            1
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

        self.assertNotEqual(
            detalle.cantidad,
            1
        )

        self.assertEqual(
            detalle.precio_unitario,
            Decimal("19990.00")
        )

        self.assertTrue(
            detalle.habilitado
        )


if __name__ == "__main__":
    unittest.main()
