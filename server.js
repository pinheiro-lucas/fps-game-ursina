const http = require("http");
const fs = require("fs");
const path = require("path");
const { WebSocketServer } = require("ws");

// Parse .env file
require("dotenv").config();

const serverInfo = {
  ip: process.env.SERVER_IP ?? "localhost",
  port: process.env.SERVER_PORT ?? 3000,
};

// Create HTTP server
const server = http.createServer((req, res) => {
  console.log(req.url);
  fs.readFile(
    path.join(__dirname, "live-map", req.url === "/" ? "/index.html" : req.url),
    (err, data) => {
      if (err) {
        res.writeHead(404);
        res.end(`Error opening ${req.url}`);
        return;
      }
      res.writeHead(200);
      res.end(data);
    }
  );
});

// Create WebSocket server
const ws = new WebSocketServer({ server });

// Global objects to store game data
let players = {};
let score = {};

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
    origin: string (player id),
    pos: number[],
    rot: number[]
  }
}
*/

ws.on("connection", client => {
  // Define client variables
  let playerId = undefined;

  client.on("message", data => {
    data = data.toString();

    // Parse received data
    data = JSON.parse(data);
    const payload = data.payload ?? {};

    switch (data.type) {
      // Player message
      case "player": {
        if (playerId === undefined) {
          // Check if username already exists in the current game
          if (Object.keys(players).includes(payload.id)) {
            // Send error to client
            client.send(
              JSON.stringify({
                error: "This username already exists in the current game",
              })
            );
            // Disconnect client
            client.close();
            return;
          } else {
            // Initialize client variables
            playerId = payload.id;
            score[playerId] = 0;
          }
        }

        // Populate global players object
        players[playerId] = payload;
        players[playerId].score = score[playerId];

        break;
      }

      // Hit message
      case "hit": {
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

        break;
      }

      // Bullet message
      case "bullet": {
        // Parse bullet payload
        const { origin, pos, rot } = payload;

        if (Object.keys(players).includes(origin)) {
          players[origin].bullet = {
            pos: pos,
            rot: rot,
          };
        }

        break;
      }

      // Watcher message
      case "watcher": {
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
    }
  });
});

server.listen(serverInfo.port, () => {
  const host = `${serverInfo.ip}:${serverInfo.port}`;
  console.log(`[*] WS => ws://${host}`);
  console.log(`[*] Map => http://${host}`);

  // Debug
  setInterval(() => console.log(players), 1000);
});
