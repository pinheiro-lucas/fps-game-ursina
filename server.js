const { WebSocketServer } = require("ws");

require("dotenv").config();

const serverInfo = {
  ip: process.env.SERVER_IP ?? "localhost",
  port: process.env.SERVER_PORT ?? 3000,
};

const server = new WebSocketServer(
  {
    port: serverInfo.port,
  },
  () => {
    console.log(`ws://${serverInfo.ip}:${serverInfo.port}`);
  }
);

let players = {};

function sendAll(payload) {
  server.clients.forEach(client => {
    client.send(JSON.stringify(payload));
  });
  console.log(payload);
}

server.on("connection", client => {
  let cache = undefined;
  let playerId = undefined;

  client.on("message", data => {
    data = data.toString();

    if (data !== cache) {
      cache = data;
      data = JSON.parse(data);

      if (playerId === undefined) {
        playerId = data.id;
      }

      if (data.online) {
        players[playerId] = data;
      }

      sendAll(players);
    }
  });

  client.on("close", () => {
    if (playerId !== undefined) {
      delete players[playerId];
      sendAll(players);
    }
  });
});
