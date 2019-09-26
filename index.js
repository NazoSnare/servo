const WebSocket = require('ws');
const path = require('path');
const util = require("util");
const { spawn } = require('child_process')

const ws = new WebSocket("ws://10.112.20.171:8080");

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
        //spaw reece serve
        let process = spawn('python', ['smartvent-kyc.py']);


        process.stdout.on('data', function (chunk) {

            var textChunk = chunk.toString('utf8');// buffer to string

            util.log(textChunk);
        });
    }

});