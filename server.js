const { WebSocketServer } = require("ws");

require("dotenv").config();

const server_info = {
  ip: process.env.SERVER_IP ?? "localhost",
  port: process.env.SERVER_PORT ?? 3000,
};

const server = new WebSocketServer(
  {
    port: server_info.port,
  },
  () => {
    console.log(`ws://${server_info.ip}:${server_info.port}`);
  }
);

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
