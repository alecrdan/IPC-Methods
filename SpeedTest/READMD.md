# Speed Test (Port vs Unix Socket)
- There will be two processes both will send a large file over a network port and other will send over a Unix Domain Socket.
- Unix Sockets are faster.

## Real World
- This is why databases like PostgreSQL or Redis use Unix Sockets by default when the app is on the same server. It's a free performance boost!