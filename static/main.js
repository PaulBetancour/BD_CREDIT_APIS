async function subirYProcesar() {
    const fileInput = document.getElementById('excelInput');
    const btn = document.getElementById('btnProcesar');
    const textBtn = document.getElementById('textBtn');

    // 1. Validar que se seleccionó un archivo
    if (!fileInput || !fileInput.files[0]) {
        alert("⚠️ Por favor, selecciona un archivo .xlsx primero.");
        return;
    }

    // 2. Efecto visual de carga
    if(btn) btn.disabled = true;
    if(textBtn) textBtn.innerText = "⏳ Procesando...";

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    try {
        // 3. Llamada a la API (FastAPI)
        const response = await fetch("http://127.0.0.1:8000/procesar-datos", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("No se pudo procesar el archivo en el servidor.");
        }

        const data = await response.json();

        // 4. Actualizar números de las tarjetas (Semana 1)
        const elementos = document.querySelectorAll("#content-1 .text-2xl.font-bold");
        if (elementos.length >= 3) {
            elementos[0].innerText = data.variables_analizadas;
            elementos[1].innerText = data.completitud;
            elementos[2].innerText = data.duplicados;
        }

        // 5. Actualizar lista de columnas
        const listaTexto = document.getElementById('listaColumnas');
        if(listaTexto && data.columnas_lista) {
            listaTexto.innerText = data.columnas_lista;
        }

        // 6. Actualizar el gráfico (Chart.js)
        if (window.chart1) {
            window.chart1.data.datasets[0].data = [
                data.promedios.score, 
                (data.promedios.ingresos / 1000).toFixed(1), // Escalado a Miles (K)
                (data.promedios.solicitado / 1000).toFixed(1), 
                1.5 
            ];
            window.chart1.update();
        }

        alert("✅ Dataset procesado y actualizado con éxito.");

    } catch (error) {
        console.error("Error:", error);
        alert("❌ Error de conexión: Verifica que FastAPI esté corriendo en http://127.0.0.1:8000");
    } finally {
        // 7. Restaurar estado del botón
        if(btn) btn.disabled = false;
        if(textBtn) textBtn.innerText = "Procesar y Limpiar Datos";
    }
}