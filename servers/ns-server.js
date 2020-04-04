
var onConnect = function test(socket) {
  
  socket.on('data', logData);
  socket.write('Server: Hello There!\n');
  //socket.end('Closing connection...\n')
};


module.exports.onConnect = onConnect
