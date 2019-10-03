const WebSocket = require('ws');
const path = require('path');
const util = require("util");
const { spawn } = require('child_process')

const ws = new WebSocket("ws://ec2-54-89-128-43.compute-1.amazonaws.com:3000");

ws.on('open', function open() {
    ws.send(JSON.stringify({
        type: "machine:connected",
        data: {
            machine: "liquid-studio"
        }
    }));
    console.log('opened');
});

ws.on('message', (data) => {
    let receivedData = JSON.parse(data).data;
    let messageType = JSON.parse(data).type;

    if (messageType === "user:redeemed") {
        console.log("user redeemed", receivedData);
        console.log('PRODUCT', receivedData.product);
        let product = receivedData.product;
        let productSlot = "1";
        switch (product.name) {
            case "Coke Zero": {
                productSlot = "1";
                break;
            }

            case "Fanta Orange": {
                productSlot = "2";
                break;
            }

            case "Coke": {
                productSlot = "3";
                break;
            }

            case "Sprite": {
                productSlot = "4";
                break;
            }


            default: {
                productSlot = "5";
                break;
            }

        }
        console.log("SLOT",productSlot);
        //spaw reece serve
        let process = spawn('python', ['smartvend-kyc.py', productSlot]);


        process.stdout.on('data', function (chunk) {

            var textChunk = chunk.toString('utf8');// buffer to string

            util.log(textChunk);
        });
    }

});
