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

server.on("connection", client => {
  let cache = null;

  client.on("message", data => {
    data = data.toString();

    if (data !== cache) {
      cache = data;
      data = JSON.parse(data);

      if (data.online) {
        players[data.id] = data;
      } else {
        delete players[data.id];
      }

      console.log(players);

      server.clients.forEach(client => {
        client.send(JSON.stringify(players));
      });
    }
  });

  client.on("ping", data => {
    const playerId = data.toString();
    players[playerId].lastPing = Date.now();
  });
});

setInterval(async () => {
  if (Object.keys(players).length > 0) {
    Object.values(players).forEach(player => {
      const timeInactive = Date.now() - player.lastPing;
      // 5 seconds
      if (timeInactive > 5000) {
        delete players[player.id];
      }
    });
  }

  console.log(players); // Debug
  // 1 second
}, 1000);
