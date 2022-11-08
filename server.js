const { WebSocketServer } = require("ws");

const server = new WebSocketServer({ port: 3000 });

let players = {};

server.on("connection", stream => {
  stream.on("message", data => {
    data = JSON.parse(data.toString());

    if (data.online) {
      players[data.id] = data;
    } else {
      delete players[data.id];
    }

    console.log(players);

    server.clients.forEach(client => {
      client.send(JSON.stringify(players));
    });
  });
});
