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

/*
data = {
  type: "player" | "bullet" | "watcher",
  payload: {
    // Player payload
    id: string,
    hp: number,
    pos: number[],
    rot: number[],
    color: number[]

    // Bullet payload
    origin: string (player id),
    target: string (player id),
    hit: boolean
  }
}
*/

server.on("connection", client => {
  let cache = undefined;
  let playerId = undefined;

  client.on("message", data => {
    data = data.toString();

    if (data !== cache) {
      cache = data;
      data = JSON.parse(data);
      const payload = data.payload ?? {};

      switch (data.type) {
        // Player connection
        case "player":
          if (playerId === undefined) {
            playerId = payload.id;
          }

          players[playerId] = payload;
          sendAll(players);

          break;

        // Bullet connection
        case "bullet":
          break;

        // Watcher connection
        case "watcher":
          client.send(JSON.stringify(players));
          break;
      }
    }
  });

  client.on("close", () => {
    if (playerId !== undefined) {
      delete players[playerId];
      sendAll(players);
    }
  });
});
