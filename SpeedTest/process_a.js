const net = require('net');
const fs = require('fs');
const os = require('os');
const path = require('path');

const FOREVER = true;

const tempDir = os.tmpdir();
const socketName = 'speedtest.sock';
const SOCKET_PATH = path.join(tempDir, socketName);
const socket = null;

// Ensure the socket file is unlinked before starting, if it already exists
if (fs.existsSync(SOCKET_PATH)) {
    fs.unlinkSync(SOCKET_PATH);
}

const sendMessage = (socket) => {
    const message = "Heartbeat or Data";
    socket.write(message, () => {
        console.log(`(A) Transmitted`);
    });
}

const unixServer = net.createServer((socket) => {
    socket.on('data', (data) => {
        // Sleep
        setTimeout(() => { }, 2000);

        console.log(`(A) Received ${data.length} bytes`);
        sendMessage(socket);
    });

    socket.on('error', (err) => {
        console.error(`Socket error: ${err.message}`);
    });

    // Kick off chatter back and forth.
    sendMessage(socket);
});

unixServer.listen(SOCKET_PATH, () => {
    console.log(`Unix server listening on ${SOCKET_PATH}`);
});

const cleanupSocket = () => {
    if (fs.existsSync(SOCKET_PATH)) {
        fs.unlinkSync(SOCKET_PATH);
    }
};

process.on('exit', cleanupSocket);
process.on('SIGINT', () => {
    cleanupSocket();
    process.exit(0);
});
process.on('SIGTERM', () => {
    cleanupSocket();
    process.exit(0);
});