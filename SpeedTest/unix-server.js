const net = require('net');
const fs = require('fs');
const os = require('os');
const path = require('path');

const FOREVER = true;

const tempDir = os.tmpdir();
const socketName = 'speedtest.sock';
const SOCKET_PATH = path.join(tempDir, socketName);

// Ensure the socket file is unlinked before starting, if it already exists
if (fs.existsSync(SOCKET_PATH)) {
    fs.unlinkSync(SOCKET_PATH);
}

const unixServer = net.createServer((socket) => {
    socket.on('data', (data) => {
        console.log(`(SERVER) Received ${data.length} bytes`);
    });

    socket.on('error', (err) => {
        console.error(`Socket error: ${err.message}`);
    });
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