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
let online = {};

server.on("connection", client => {
  let cache = undefined;

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

      // console.log(players);

      server.clients.forEach(client => {
        client.send(JSON.stringify(players));
      });
    }
  });

  client.on("ping", data => {
    const playerId = data.toString();
    online[playerId] = Date.now();
  });
});

setInterval(async () => {
  if (Object.keys(online).length > 0) {
    for (const [playerId, lastPing] of Object.entries(online)) {
      const timeInactive = Date.now() - lastPing;

      // 5 seconds
      if (timeInactive > 5000) {
        delete online[playerId];
        if (Object.keys(players).includes(playerId)) {
          delete players[playerId];
        }
      }
    }
  }

  // Debug
  console.log(players);
  console.log(online);

  // 1 second
}, 1000);
