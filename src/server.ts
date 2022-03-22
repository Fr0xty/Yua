import express from 'express';
const app = express();

app.get('/', async (req, res) => {
    res.send('Yuna is currently online.');
});

app.listen(3000);
