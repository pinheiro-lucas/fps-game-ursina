const { WebSocketServer } = require("ws");

// Parse .env file
require("dotenv").config();

const serverInfo = {
  ip: process.env.SERVER_IP ?? "localhost",
  port: process.env.SERVER_PORT ?? 3000,
};

// Create WebSocket server
const server = new WebSocketServer(
  {
    port: serverInfo.port,
  },
  () => {
    console.log(`ws://${serverInfo.ip}:${serverInfo.port}`);
  }
);

// Global objects to store game data
let players = {};
let score = {};

// Global functions
function sendAll(payload) {
  // Send the payload to all connected clients
  server.clients.forEach(client => {
    client.send(JSON.stringify(payload));
  });
  console.log(payload);
}

/*
Sever payload

data = {
  type: "player" | "hit" | "bullet" | "watcher",
  payload: {
    // Player payload
    id: string,
    hp: number,
    pos: number[],
    rot: number[],
    color: number[]

    // Hit payload
    origin: string (player id),
    target: string (player id)

    // Bullet payload
    pos: number[],
    rot: number[]
  }
}
*/

server.on("connection", client => {
  // Define client variables
  let cache = undefined;
  let playerId = undefined;

  client.on("message", data => {
    data = data.toString();

    // Simple cache
    if (data !== cache) {
      cache = data;

      // Parse received data
      data = JSON.parse(data);
      const payload = data.payload ?? {};

      switch (data.type) {
        // Player message
        case "player":
          // Initialize client variables
          if (playerId === undefined) {
            playerId = payload.id;

            score[playerId] = 0;
          }

          // Populate global players object
          players[playerId] = payload;
          players[playerId].score = score[playerId];

          // Send data to all clients on each player message
          sendAll(players);
          break;

        // Hit message
        case "hit":
          // Hit variables
          const { origin, target } = payload;
          const damage = 20;

          // Apply damage to target player
          if (Object.keys(players).includes(target)) {
            players[target].hp -= damage;

            // Check target player death
            if (players[target].hp <= 0) {
              players[target].hp = 0;

              // Update score
              if (Object.keys(score).includes(origin)) {
                score[origin]++;
                players[origin].score = score[origin];
              }
            }
          }

          sendAll(players);
          break;

        // Watcher message
        case "watcher":
          // Send initial payload only to the watcher client
          client.send(JSON.stringify(players));
          break;
      }
    }
  });

  client.on("close", () => {
    if (playerId !== undefined) {
      // Remove player from server and notify clients
      delete players[playerId];
      delete score[playerId];

      sendAll(players);
    }
  });
});
