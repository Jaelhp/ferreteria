from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Compra, DetalleCompra
from .forms import CompraForm, DetalleCompraForm
from inventario.models import MovimientoInventario


def _registrar_entrada(producto, cantidad, motivo, referencia):
    """Registra un movimiento de ENTRADA en inventario y actualiza stock."""
    stock_anterior = producto.stock_actual
    nuevo_stock = stock_anterior + cantidad
    producto.stock_actual = nuevo_stock
    producto.save()

    MovimientoInventario.objects.create(
        producto=producto,
        tipo="entrada",
        cantidad=cantidad,
        motivo=motivo,
        referencia=referencia,
        stock_anterior=stock_anterior,
        stock_nuevo=nuevo_stock,
    )


def _revertir_entrada(producto, cantidad, motivo, referencia):
    """Revierten una entrada (por eliminación de detalle, por ejemplo)."""
    stock_anterior = producto.stock_actual
    nuevo_stock = stock_anterior - cantidad
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


# ---------------------- COMPRAS ----------------------


def compra_list(request):
    compras = Compra.objects.all().order_by("-fecha")
    return render(request, "compras/compra_list.html", {"compras": compras})


def compra_detail(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    detalles = compra.detalles.all()
    return render(
        request,
        "compras/compra_detail.html",
        {"compra": compra, "detalles": detalles},
    )


def compra_create(request):
    if request.method == "POST":
        form = CompraForm(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            # total se calcula a partir de los detalles
            compra.total = 0
            compra.save()
            return redirect("compras:compra_detail", pk=compra.pk)
    else:
        form = CompraForm()
    return render(request, "compras/compra_form.html", {"form": form})


def compra_update(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    if request.method == "POST":
        form = CompraForm(request.POST, instance=compra)
        if form.is_valid():
            form.save()
            return redirect("compras:compra_detail", pk=compra.pk)
    else:
        form = CompraForm(instance=compra)
    return render(request, "compras/compra_form.html", {"form": form, "compra": compra})


def compra_delete(request, pk):
    compra = get_object_or_404(Compra, pk=pk)
    if request.method == "POST":
        # Antes de borrar la compra, revertimos todas las entradas al inventario
        for detalle in compra.detalles.all():
            _revertir_entrada(
                detalle.producto,
                detalle.cantidad,
                motivo="Eliminación de compra",
                referencia=f"Compra {compra.numero_compra}",
            )
        compra.delete()
        return redirect("compras:compra_list")
    return render(request, "compras/compra_confirm_delete.html", {"compra": compra})


# ----------------- DETALLES DE COMPRA -----------------


def detalle_compra_create(request, compra_id):
    compra = get_object_or_404(Compra, pk=compra_id)
    if request.method == "POST":
        form = DetalleCompraForm(request.POST)
        if form.is_valid():
            detalle = form.save(commit=False)
            detalle.compra = compra
            detalle.save()  # calcula subtotal y actualiza total de la compra

            _registrar_entrada(
                detalle.producto,
                detalle.cantidad,
                motivo="Compra",
                referencia=f"Compra {compra.numero_compra}",
            )
            return redirect("compras:compra_detail", pk=compra.pk)
    else:
        form = DetalleCompraForm()
    return render(
        request,
        "compras/detalle_compra_form.html",
        {"form": form, "compra": compra},
    )


def detalle_compra_update(request, pk):
    detalle = get_object_or_404(DetalleCompra, pk=pk)
    compra = detalle.compra

    if request.method == "POST":
        # Para simplificar, primero revertimos el movimiento anterior,
        # luego aplicamos el nuevo.
        stock_cantidad_anterior = detalle.cantidad
        producto_anterior = detalle.producto

        form = DetalleCompraForm(request.POST, instance=detalle)
        if form.is_valid():
            # revertir movimiento anterior
            _revertir_entrada(
                producto_anterior,
                stock_cantidad_anterior,
                motivo="Edición de detalle de compra",
                referencia=f"Compra {compra.numero_compra}",
            )

            detalle = form.save()
            _registrar_entrada(
                detalle.producto,
                detalle.cantidad,
                motivo="Edición de compra",
                referencia=f"Compra {compra.numero_compra}",
            )
            # recalcular total
            compra.calcular_total()
            return redirect("compras:compra_detail", pk=compra.pk)
    else:
        form = DetalleCompraForm(instance=detalle)
    return render(
        request,
        "compras/detalle_compra_form.html",
        {"form": form, "compra": compra, "detalle": detalle},
    )


def detalle_compra_delete(request, pk):
    detalle = get_object_or_404(DetalleCompra, pk=pk)
    compra = detalle.compra
    if request.method == "POST":
        _revertir_entrada(
            detalle.producto,
            detalle.cantidad,
            motivo="Eliminación de detalle de compra",
            referencia=f"Compra {compra.numero_compra}",
        )
        detalle.delete()
        compra.calcular_total()
        return redirect("compras:compra_detail", pk=compra.pk)
    return render(
        request,
        "compras/detalle_compra_confirm_delete.html",
        {"detalle": detalle, "compra": compra},
    )
