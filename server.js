// server.js
const { spawn } = require('child_process');
const express = require('express');
const http = require('http');
const socketIo = require('socket.io');

const app = express();
const server = http.createServer(app);
const io = socketIo(server);

app.use(express.static('public'));

io.on('connection', (socket) => {
    console.log('New client connected');

    // prints the text output from the python script in the console
    socket.on('chat message', (msg) => {
      // Broadcast the message to all connected clients
      io.emit('chat message', { text: 'User: ' + msg, sender: 'user' });

      // Run the Python script with the message as an argument
      const python = spawn('python', ['agent.py', msg]);
      let pythonResponse = '';
      let pythonError = '';
  
      // python.stdout.on('data', (data) => {
        // pythonResponse += data.toString();
      // });

      python.stderr.on('data', (data) => {
        pythonError += data.toString();
      });

      python.stdout.on('data', (data) => {
        console.log(`Python stdout: ${data}`);
       });
  
      python.on('close', (code) => {
        if (code !== 0) {
          console.log(`Python script exited with code ${code}`);
          console.log(`Error message: ${pythonError}`);
        }
        // Send the Python script's response back to the sender
        socket.emit('chat message', { text: 'Agent: ' + pythonResponse, sender: 'agent' });
      });
    });
  
    socket.on('disconnect', () => {
      console.log('Client disconnected');
    });
  });
  
  server.listen(3000, () => {
    console.log('Listening on *:3000');
  });