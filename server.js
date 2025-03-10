const express = require("express");
const app = express();
const port = 5000;

app.use(express.json()); // Middleware untuk parsing JSON

// Database sementara untuk menyimpan pesan terenkripsi
const messages = [];

// Endpoint untuk mengirim pesan
app.post("/send", (req, res) => {
    const data = req.body;
    messages.push(data);
    res.json({ status: "success", message: "Pesan terkirim!" });
});

// Endpoint untuk menerima pesan berdasarkan penerima
app.get("/receive/:recipient", (req, res) => {
    const recipient = req.params.recipient;
    const userMessages = messages.filter(msg => msg.recipient === recipient);
    res.json(userMessages);
});

// Endpoint untuk melihat semua pesan (hanya untuk debugging)
app.get("/", (req, res) => {
    res.send(`
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Hello World</title>
            <style>
                body {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background-color: #f4f4f4;
                    font-family: Arial, sans-serif;
                }
                h1 {
                    font-size: 3rem;
                    color: #333;
                }
            </style>
        </head>
        <body>
            <h1>Hello World!</h1>
        </body>
        </html>
    `);
});

// Menjalankan server
app.listen(port, () => {
    console.log(`Server berjalan di http://localhost:${port}`);
});