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
    res.json({ messages });
});

// Menjalankan server
app.listen(port, () => {
    console.log(`Server berjalan di http://localhost:${port}`);
});