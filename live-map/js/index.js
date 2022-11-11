const canvas = document.querySelector("canvas");
const playerList = document.querySelector("#player-list");
const form = document.querySelector("form");
const serverInput = document.querySelector("#input-server");

const ctx = canvas.getContext("2d");

const mapSize = 130;
const playerSize = 25;
const mapFix = canvas.width / 2 - playerSize / 2;

function drawPlayer(x, y, color) {
  ctx.fillStyle = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
  ctx.fillRect(x * 2 + mapFix, y * 2 + mapFix, playerSize, playerSize);
}

form.addEventListener("submit", event => {
  event.preventDefault();

  const socket = new WebSocket(serverInput.value);

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

    socket.send(JSON.stringify({ type: "watcher" }));
  });

  socket.addEventListener("message", ({ data }) => {
    data = JSON.parse(data);

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const playerListChildren = [];

    Object.values(data).forEach(player => {
      const { id, hp, pos, rot, color } = player;

      const li = document.createElement("li");
      li.innerHTML = id;
      li.style.color = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
      li.style.fontWeight = "bold";

      playerListChildren.push(li);

      drawPlayer(pos[0], pos[2], color);
    });

    playerList.replaceChildren(...playerListChildren);
  });
});