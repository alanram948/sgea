function filtrar(){
        const texto = document.getElementById('buscador').value.toLowerCase();
        const productos = document.querySelectorAll('.card');

        productos.forEach(producto => {
            const nombre = producto.querySelector('h3').innerText.toLowerCase();
            const sku = producto.querySelector('span').innerText.toLowerCase();
            if (nombre.includes(texto) || sku.includes(texto)) {
                producto.style.display = "block";
            }else{
                producto.style.display = "none";
            }
        
        });
    }
    let carrito=[]
    let totalAcumulado=0;
    function mostrar_menu(elemento) {
        const menu = elemento.querySelector('.mini-menu');
        document.querySelectorAll('.mini-menu').forEach(m => {
            if (m !== menu) m.style.display = 'none';
        });
        menu.style.display = menu.style.display === 'none' ? 'block' : 'none';
    }
    function agregarALaCuenta(idArticulo, nombre, stockDisponibleT, boton) {
        const contenedorMenu = boton.parentElement;
        const tarjeta = contenedorMenu.parentElement;
        
        const cantidad = parseFloat(contenedorMenu.querySelector('.cantidad-input').value);
        const precioTexto = tarjeta.querySelector('.precio').innerText.replace('$', '').trim();
        const precio = parseFloat(precioTexto);
        const stockDisponible = parseInt(stockDisponibleT);
        
        if (cantidad > stockDisponible) {
            alert(`Stock insuficiente. Solo quedan ${stockDisponible} unidades de ${nombre}.`);
            return;
        }

        
        const indiceExistente = carrito.findIndex(item => item.id_articulo === idArticulo);

        if (indiceExistente !== -1) {
            
            if (carrito[indiceExistente].cantidad + cantidad > stockDisponible) {
                alert(`No puedes agregar más. Límite de stock alcanzado para ${nombre}.`);
                return;
            }
            
            carrito[indiceExistente].cantidad += cantidad;
            carrito[indiceExistente].subtotal += (precio * cantidad);
        } else {
            
            carrito.push({
                id_articulo: idArticulo,
                nombre: nombre, 
                cantidad: cantidad,
                precio_unitario: precio,
                subtotal: (precio * cantidad)
            });
        }

        actualizarCarritoUI();
        
        
        contenedorMenu.style.display = 'none';
        contenedorMenu.querySelector('.cantidad-input').value = 1;
    }

    function quitarDeLaCuenta(index) {
        
        carrito.splice(index, 1); 
        
        actualizarCarritoUI();
    }

    
    function actualizarCarritoUI() {
        const lista = document.getElementById('items-cuenta');
        lista.innerHTML = ''; 
        totalAcumulado = 0; 

        
        carrito.forEach((item, index) => {
            totalAcumulado += item.subtotal;

            const li = document.createElement('li');
            li.style.marginBottom = "12px";
            li.style.display = "flex";
            li.style.justifyContent = "space-between";
            li.style.alignItems = "center";
            li.style.borderBottom = "1px solid var(--hover)";
            li.style.paddingBottom = "8px";

            
            li.innerHTML = `
                <span>${item.cantidad}x ${item.nombre}</span>
                <div style="display: flex; gap: 12px; align-items: center;">
                    <strong>$${item.subtotal.toFixed(2)}</strong>
                    <button onclick="quitarDeLaCuenta(${index})" style="background: transparent; border: none; color: #EF4444; font-size: 1.2rem; cursor: pointer; padding: 0 5px;" title="Quitar producto">✖</button>
                </div>
            `;
            lista.appendChild(li);
        });

        
        document.getElementById('total-cuenta').innerHTML = `<span>Total:</span> <span>$${totalAcumulado.toFixed(2)}</span>`;
    }

    function procesarVenta() {
        if(carrito.length === 0) {
            alert("El ticket está vacío. Agrega productos primero.");
            return;
     
        }
        const btnCobrar = document.getElementById('btn-cobrar');
        btnCobrar.innerText = "Procesando...";
        btnCobrar.disabled = true;
        fetch('/ventas/procesar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                items: carrito, 
                total: totalAcumulado 
            })
        })
        .then(response => response.json())
        .then(data => {
            if(data.exito) {
                alert("¡Venta registrada con éxito! Folio: " + data.folio);
                window.location.reload();
        } else {
                alert("Error al procesar la venta: " + data.error);
                btnCobrar.innerText = "Cobrar e Imprimir";
                btnCobrar.disabled = false;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert("Ocurrió un error de conexión.");
            btnCobrar.innerText = "Cobrar e Imprimir";
            btnCobrar.disabled = false;
        });
    
    }