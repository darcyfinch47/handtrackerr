const { exec } = require('child_process');
const express = require('express');
const cors = require("cors");
const rateLimit = require('express-rate-limit');

const app = express();
const port = 3000;
const limiter = rateLimit({
    windowMs: 1 * 1000, // 1 sec
    max: 1, // limit each IP to 1 requests per windowMs
});
  
app.use(limiter);
app.use(cors());

// Endpoint to lock the computer
app.get('/lock-computer', (req, res) => {
  // Lock the computer on Windows
  const lockCommand = 'rundll32.exe user32.dll,LockWorkStation';

  exec(lockCommand, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error locking the computer: ${error}`);
      res.status(500).send('Error locking the computer');
      return;
    }
    console.log('Computer locked successfully.');
    res.status(200).send('Computer locked successfully.');
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
