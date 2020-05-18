const { spawn, exec } = require('child_process')
const portDescriptor = process.env.PORT_DESCRIPTOR || 'ttyUSB0'

// Init device
// stty -F /dev/ttyUSB0 115200
const stty = spawn('stty', ['-F', '/dev/' + portDescriptor, '115200']);
stty.on('close', () => {
   exec('echo "G0X150" > /dev/' + portDescriptor);
});
