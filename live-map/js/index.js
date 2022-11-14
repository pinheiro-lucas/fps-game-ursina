const canvas = document.querySelector("canvas");
const playerList = document.querySelector("#player-list");
const form = document.querySelector("form");
const serverInput = document.querySelector("#input-server");

const ctx = canvas.getContext("2d");

const mapSize = 172;
const playerSize = 20;
const mapFix = canvas.width / 2 - playerSize / 2;

serverInput.value = localStorage.getItem("ws-fps-url") ?? "ws://localhost:3000";

function drawPlayer(x, y, color, name) {
  x = x * 3 + mapFix;
  y = y * 3 + mapFix;
  ctx.fillStyle = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
  ctx.font = "bold 18px sans-serif";
  ctx.textAlign = "center";
  ctx.fillText(name, x, y - playerSize / 2.5);
  ctx.fillRect(x, y, playerSize, playerSize);
}

form.addEventListener("submit", event => {
  event.preventDefault();

  localStorage.setItem("ws-fps-url", serverInput.value ?? "");

  const socket = new WebSocket(serverInput.value);

  window.socket = socket;

  socket.addEventListener("open", () => {
    console.log("CONECTADO");

    form.childNodes.forEach(child => {
      child.disabled = true;
    });

    const connected = document.createElement("span");
    connected.style.color = "green";
    connected.style.textDecoration = "underline";
    connected.innerHTML = "Conectado";

    form.appendChild(connected);

    setInterval(() => {
      socket.send(JSON.stringify({ type: "watcher" }));
    }, 1000);
  });

  socket.addEventListener("message", ({ data }) => {
    data = JSON.parse(data);

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const playerListChildren = [];

    Object.values(data).forEach(player => {
      const { id, hp, score, pos, rot, color } = player;

      const li = document.createElement("li");
      li.innerHTML = `${id} - HP: ${hp} - Score: ${score}`;
      li.style.color = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
      li.style.fontWeight = "bold";

      playerListChildren.push(li);

      drawPlayer(pos[0], pos[2], color, id);
    });

    playerList.replaceChildren(...playerListChildren);
  });
});
