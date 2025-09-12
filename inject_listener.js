/*
Injects a listener into the game page to receive shield direction updates from the server.
The information is sent via WebSocket using Socket.IO and updates the shield direction in real-time.
Apply this script using a browser extension like Tampermonkey or directly in the browser console.

Author: Powercube
*/

let s = document.createElement("script");
s.src = "https://cdn.socket.io/4.7.5/socket.io.min.js";
s.onload = () => {
  const socket = io("http://localhost:5000");

  socket.on("shield_update", (data) => {
    console.log("Shield update:", data);

    if (data.status !== "error" && game_started === true) {
      heart.setShieldDir(data.shield_direction);
    }
  });
};
document.head.appendChild(s);
