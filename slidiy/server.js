var express = require('express');
var app = express();

app.use(express.static('public'));
app.get('/index.htm', function (req, res) {
   res.sendFile(__dirname + "/" + "index.htm");
})

app.get('/process_get', function (req, res) {
   // Prepare output in JSON format
   response = {
      command: req.query.comm
   };
   console.log(response);
   console.log(req.query.comm);

   const { spawn, exec } = require('child_process')
   const portDescriptor = process.env.PORT_DESCRIPTOR || 'ttyUSB0'

   // Init device
   //stty -F /dev/ttyUSB0 115200;
   const stty = spawn('stty', ['-F', '/dev/' + portDescriptor, '115200']);
   stty.on('close', () => {
      //exec('echo "G0X40" > /dev/' + portDescriptor);
      exec('echo "' + req.query.comm + '" > /dev/' + portDescriptor);
   });

   res.end(JSON.stringify(response));

})

app.get('/process_unlock', function (req, res) {

   const unlockCommand = '$20=0'

   response = {
      command: unlockCommand
   };
   console.log(response);
   console.log(req.query.comm);

   const { spawn, exec } = require('child_process')
   const portDescriptor = process.env.PORT_DESCRIPTOR || 'ttyUSB0'

   const stty = spawn('stty', ['-F', '/dev/' + portDescriptor, '115200']);
   stty.on('close', () => {
      exec('echo "' + unlockCommand + '" > /dev/' + portDescriptor);
   });

   res.end(JSON.stringify(response));

})

var server = app.listen(8081, function () {
   var host = server.address().address
   var port = server.address().port

   console.log("Example app listening at http://localhost:8081");
})
