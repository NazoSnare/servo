const WebSocket = require('ws');
const path = require('path');
const {spawn} = require('child_process')

const ws = new WebSocket("ws://10.112.20.171:8080");

ws.on('open', function open() {
    ws.send(JSON.stringify({
        type:"machine:connected",
        data: {
           machine:"liquid-studio"
        }
    }));
    console.log('opened');
  });
  
  ws.on('message', (data) =>{
      let receivedData = JSON.parse(data).data;
      let messageType = JSON.parse(data).type;

      if (messageType === "user:redeemed") {
        console.log("user redeemed", receivedData);
        //spaw reece serve
        let reece = spawn('python smartvent-kyc.py',[]);
      }

  });