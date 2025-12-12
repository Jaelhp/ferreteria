from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Venta, DetalleVenta
from .forms import VentaForm, DetalleVentaForm
from inventario.models import MovimientoInventario


def _registrar_salida(producto, cantidad, motivo, referencia):
    """Registra un movimiento de SALIDA en inventario y actualiza stock."""
    stock_anterior = producto.stock_actual
    nuevo_stock = stock_anterior - cantidad
    producto.stock_actual = nuevo_stock
    producto.save()

    MovimientoInventario.objects.create(
        producto=producto,
        tipo="salida",
        cantidad=cantidad,
        motivo=motivo,
        referencia=referencia,
        stock_anterior=stock_anterior,
        stock_nuevo=nuevo_stock,
    )


def _revertir_salida(producto, cantidad, motivo, referencia):
    """Revierten una salida (por eliminación/edición de detalle de venta)."""
    stock_anterior = producto.stock_actual
    nuevo_stock = stock_anterior + cantidad
    producto.stock_actual = nuevo_stock
    producto.save()

    MovimientoInventario.objects.create(
        producto=producto,
        tipo="ajuste",
        cantidad=cantidad,
        motivo=motivo,
        referencia=referencia,
        stock_anterior=stock_anterior,
        stock_nuevo=nuevo_stock,
    )


# ---------------------- VENTAS ----------------------


def venta_list(request):
    ventas = Venta.objects.all().order_by("-fecha")
    return render(request, "ventas/venta_list.html", {"ventas": ventas})


def venta_detail(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    detalles = venta.detalles.all()
    return render(
        request,
        "ventas/venta_detail.html",
        {"venta": venta, "detalles": detalles},
    )


def venta_create(request):
    if request.method == "POST":
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            venta.total = 0
            venta.save()
            return redirect("ventas:venta_detail", pk=venta.pk)
    else:
        form = VentaForm()
    return render(request, "ventas/venta_form.html", {"form": form})


def venta_update(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == "POST":
        form = VentaForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            return redirect("ventas:venta_detail", pk=venta.pk)
    else:
        form = VentaForm(instance=venta)
    return render(request, "ventas/venta_form.html", {"form": form, "venta": venta})


def venta_delete(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == "POST":
        # revertir todas las salidas asociadas
        for detalle in venta.detalles.all():
            _revertir_salida(
                detalle.producto,
                detalle.cantidad,
                motivo="Eliminación de venta",
                referencia=f"Venta {venta.numero_venta}",
            )
        venta.delete()
        return redirect("ventas:venta_list")
    return render(request, "ventas/venta_confirm_delete.html", {"venta": venta})


# ----------------- DETALLES DE VENTA -----------------


def detalle_venta_create(request, venta_id):
    venta = get_object_or_404(Venta, pk=venta_id)
    if request.method == "POST":
        form = DetalleVentaForm(request.POST)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.venta = venta
            detalle.save()

            _registrar_salida(
                detalle.producto,
                detalle.cantidad,
                motivo="Venta",
                referencia=f"Venta {venta.numero_venta}",
            )
            return redirect("ventas:venta_detail", pk=venta.pk)
    else:
        form = DetalleVentaForm()
    return render(
        request,
        "ventas/detalle_venta_form.html",
        {"form": form, "venta": venta},
    )


def detalle_venta_update(request, pk):
    detalle = get_object_or_404(DetalleVenta, pk=pk)
    venta = detalle.venta

    if request.method == "POST":
        cantidad_anterior = detalle.cantidad
        producto_anterior = detalle.producto

        form = DetalleVentaForm(request.POST, instance=detalle)
        if form.is_valid():
            # revertir salida anterior
            _revertir_salida(
                producto_anterior,
                cantidad_anterior,
                motivo="Edición de detalle de venta",
                referencia=f"Venta {venta.numero_venta}",
            )

            detalle = form.save()
            _registrar_salida(
                detalle.producto,
                detalle.cantidad,
                motivo="Edición de venta",
                referencia=f"Venta {venta.numero_venta}",
            )
            venta.calcular_total()
            return redirect("ventas:venta_detail", pk=venta.pk)
    else:
        form = DetalleVentaForm(instance=detalle)
    return render(
        request,
        "ventas/detalle_venta_form.html",
        {"form": form, "venta": venta, "detalle": detalle},
    )


def detalle_venta_delete(request, pk):
    detalle = get_object_or_404(DetalleVenta, pk=pk)
    venta = detalle.venta
    if request.method == "POST":
        _revertir_salida(
            detalle.producto,
            detalle.cantidad,
            motivo="Eliminación de detalle de venta",
            referencia=f"Venta {venta.numero_venta}",
        )
        detalle.delete()
        venta.calcular_total()
        return redirect("ventas:venta_detail", pk=venta.pk)
    return render(
        request,
        "ventas/detalle_venta_confirm_delete.html",
        {"detalle": detalle, "venta": venta},
    )
