

module.exports = function connection(ws) {
	// console.log(request)
 //    const connection = request.accept(null, request.origin);
 //    connection.on('message', function(message) {
 //      console.log('Received Message:', message.utf8Data);
 //    });
 //    connection.on('close', function(reasonCode, description) {
 //        console.log('Client has disconnected.');
 //    });
    ws.on('message', function incoming(message) {
        console.log('received: %s', message);

        
    });

}