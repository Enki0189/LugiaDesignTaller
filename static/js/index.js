const express = require('express');
const http = require('http');
const cors = require('cors');
const app = express();
const request = require('request');
const bodyParser = require('body-parser');

app.set('port', 3000)

app.use(cors({
    origin: '*',
}));

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.get('/generar', (req, res) => {
    // Crea un objeto de preferencia
    let nombre = document.getElementById("nombre");
    //console.log(nombre)
    let preference = {
        back_urls: {
            success: 'http://localhost:3003/success'
        },
        items: [{
            //acá podría ir con el nombre desde la base de datos o un json el title (escritorio.nombre por ej)
            title: "Escritorio",
            description: "escritorio gamer",
            unit_price: 100,
            currency_id: "ARS",
            quantity: 1,
        }, ],
        //esto tiene una id ficticia por ahora
        notification_url: 'https://379d-191-84-70-23.ngrok-free.app/notificar'
    };

    mercadopago.preferences
        .create(preference)
        .then(function(response) {
            // En esta instancia deberás asignar el valor dentro de response.body.id por el ID de preferencia solicitado en el siguiente paso
            console.log(response.body.init_point);
            //res.send(response.body.init_point);
            res.send(`<a href="${response.body.init_point}"> IR A PAGAR</a>`);
        })
        .catch(function(error) {
            console.log(error);
        });
});

app.get('/success', (req, res) => {
    res.send('Todo salio bien')
})

app.post('/notificar', async(req, res) => {
    console.log("notificar");
    const { query } = req;
    console.log({ query });
    const topic = query.topic || query.type;
    console.log({ topic });
    var merchantOrder;

    switch (topic) {
        case "payment":
            const paymentId = query.id || query['data.id'];
            console.log(topic, 'getting payment', paymentId);
            const payment = await mercadopago.payment.findById(paymentId);
            console.log(payment)
            console.log(topic, 'getting merchant order');
            merchantOrder = await mercadopago.merchant_orders.findById(payment.body.order.id);
            break;
        case "merchant order":
            const orderId = query.id;
            console.log(topic, 'getting merchant order', orderId);
            merchantOrder = await mercadopago.merchant_orders.findById(orderId);
            break;
    }

    //esta parte es del tutorial, tira error y no encuentro qué le pasa, pero hasta antes de esto todo funciona
    //console.log(merchantOrder.body.payment);

    /*    var paidAmount = 0;
        merchantOrder.body.payments.forEach(payment => {
            if (payment.status === 'approved') {
                paidAmount += payment.transaction_amount;
            }
        });

        if (paidAmount >= merchantOrder.body.transaction_amount) {
            console.log('el pago se completó')
        } else {
            console.log('el pago NO se completó')
        }*/

    res.send();
})


// SDK de Mercado Pago
const mercadopago = require("mercadopago");
// Agrega credenciales
mercadopago.configure({
    access_token: "APP_USR-2668653040880546-091716-bbcb8f8503c6715854fdc44f002834f9-1482234495",
});

//de produccion
//access_token = APP_USR-2668653040880546-091716-bbcb8f8503c6715854fdc44f002834f9-1482234495

mercadopago.merchant_orders.findById('11969322880').then(console.log(res => res.body));

http.createServer(app).listen(app.get('port'), () => {
    console.log('HTTP escuchando en puerto ' + app.get('port'));
})