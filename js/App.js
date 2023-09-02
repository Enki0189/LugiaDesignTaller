// Código del servidor (Node.js y Express)
import { loadMercadoPago } from "@mercadopago/sdk-js";
const express = require('express');
const app = express();
const mercadopago = require('mercadopago'); // Asegúrate de instalar la biblioteca mercadopago

const access_token = 'TEST-6306101317624376-060219-a45c93a10a3aef2fcf5a3df0561fe9d3-207146047'; // Reemplaza con tu access token de MercadoPago




await loadMercadoPago();
const mp = new window.MercadoPago("TEST-62ad525c-240c-465a-aaa0-eb1e1a9f8591");
app.use(express.json());

app.post('/iniciar-pago', async (req, res) => {
    try {
        // Configura MercadoPago con tu access token
        mercadopago.configure({
            access_token
        });

        // Crea la preferencia de pago con los detalles del carrito
        const preference = {
            items: req.body.carrito,
            // Otros detalles de la preferencia de pago
        };

        const response = await mercadopago.preferences.create(preference);

        // Responde con la URL de redirección proporcionada por MercadoPago
        res.json({ init_point: response.body.init_point });
    } catch (error) {
        console.error('Error al iniciar el pago:', error);
        res.status(500).json({ error: 'Error al iniciar el pago' });
    }
});

app.listen(3000, () => {
    console.log('Servidor escuchando en el puerto 3000');
});
