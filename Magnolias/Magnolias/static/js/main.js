function calculateFields() {
    // Extraer días de cobertura (puedes ajustar este valor o hacerlo dinámico si es necesario)
    let diasDeCobertura = 21;

    document.querySelectorAll("tbody tr").forEach(function (row, idx) {
        // Verifica que los selectores coincidan con los nombres y clases en el HTML
        let conteoFisico = parseInt(row.querySelector("input[name^='conteo_fisico']").value) || 0;
        let porVencer = parseInt(row.querySelector("input[name^='por_vencer']").value) || 0;
        let devolucion = parseInt(row.querySelector("input[name^='devolucion']").value) || 0;
        let canje = parseInt(row.querySelector("input[name^='canje']").value) || 0;
        let inventarioAMPM = parseInt(row.querySelector("input[name^='inventario_ampm']").value) || 0;
        let minimoDisplay = parseInt(row.querySelector("input[name^='minimo_display']").value) || 0;
        let inventarioInicial = parseInt(row.querySelector("input[name^='inventario_inicial']").value) || 0;

        // Acceder al elemento <p> por su atributo name
        let diasEntreVisitasElement = document.querySelector("p[name='dvisitas']");

        // Extraer solo el número usando una expresión regular
        let diasEntreVisitas = diasEntreVisitasElement ? parseInt(diasEntreVisitasElement.textContent.match(/\d+/)[0]) || 0 : 0;

        // Calcular ajuste
        let ajuste = conteoFisico + porVencer + devolucion + canje - inventarioAMPM;
        let ajusteInput = row.querySelector("input[name^='ajuste']");
        if (ajusteInput) {
            ajusteInput.value = ajuste;
        }

        // Calcular venta (inventario_inicial - conteo_fisico - por_vencer - canje - devolucion)
        let venta = inventarioInicial - conteoFisico - porVencer - canje - devolucion;

        // Calcular promedio diario de ventas
        let promedioDiarioVenta = (diasEntreVisitas > 0) ? venta / diasEntreVisitas : 0;

        // Calcular venta estimada (recomendado por Magnolias)
        let ventaEstimada = promedioDiarioVenta * diasDeCobertura;
        let vari = Math.max(ventaEstimada, minimoDisplay) - conteoFisico - porVencer;
        let cantidadEntregar = Math.max(vari + Math.round(porVencer * 0.5), Math.round(porVencer * 0.5));
        let recomendadoMagnolia = vari;
        
        let recomendadoInput = row.querySelector("input[name^='recomendado_M']");
        if (recomendadoInput) {
            recomendadoInput.value = Math.round(recomendadoMagnolia);
        }

        // Calcular entregado real (entrega_final)
        let entregadoRealInput = row.querySelector("input[name^='entregado_real']");
        if (entregadoRealInput) {
            entregadoRealInput.value = Math.round(cantidadEntregar);
        }
    });

    // Actualizar los totales de venta y devolución
    let t = 0;
    let d = 0;

    // Obtener todos los inputs de devolución y entregado real en la tabla
    var devolucionInputs = document.querySelectorAll("input[name^='devolucion_']");
    var entregadoInputs = document.querySelectorAll("input[name^='entregado_real_']");
    var precios = JSON.parse('{{ precios_productos|escapejs }}');  // Lista de precios con IVA desde Django

    // Verificar que las longitudes coincidan y realizar las operaciones
    if (devolucionInputs.length === precios.length && entregadoInputs.length === precios.length) {
        for (let i = 0; i < precios.length; i++) {
            let devolucion = parseFloat(devolucionInputs[i].value) || 0;
            let entregado = parseFloat(entregadoInputs[i].value) || 0;

            t += entregado * precios[i];  // Multiplicar cada valor de entregado por el precio correspondiente
            d += devolucion * precios[i];  // Multiplicar cada valor de devolución por el precio correspondiente
        }
    } else {
        console.error("Las listas de precios y los inputs de devolución/entregado no tienen la misma longitud.");
    }

    // Actualizar los valores en los elementos HTML
    document.getElementById("venta_total").value = t.toFixed(2);
    document.getElementById("devolucion_total").value = d.toFixed(2);
}

// Actualizar los totales de venta y devolución
    let t = 0;
    let d = 0;

    // Obtener todos los inputs de devolución y entregado real en la tabla
    var devolucionInputs = document.querySelectorAll("input[name^='devolucion_']");
    var entregadoInputs = document.querySelectorAll("input[name^='entregado_real_']");
    var precios = JSON.parse('{{ precios_productos|escapejs }}');  // Lista de precios con IVA desde Django

    // Verificar que las longitudes coincidan y realizar las operaciones
    if (devolucionInputs.length === precios.length && entregadoInputs.length === precios.length) {
        for (let i = 0; i < precios.length; i++) {
            let devolucion = parseFloat(devolucionInputs[i].value) || 0;
            let entregado = parseFloat(entregadoInputs[i].value) || 0;

            t += entregado * precios[i];  // Multiplicar cada valor de entregado por el precio correspondiente
            d += devolucion * precios[i];  // Multiplicar cada valor de devolución por el precio correspondiente
        }
    } else {
        console.error("Las listas de precios y los inputs de devolución/entregado no tienen la misma longitud.");
    }

    // Actualizar los valores en los elementos HTML
    document.getElementById("venta_total").value = t.toFixed(2);
    document.getElementById("devolucion_total").value = d.toFixed(2);

// Llamar a la función cuando los valores cambien
document.addEventListener("input", calculateFields);