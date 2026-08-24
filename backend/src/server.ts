import express from 'express';
import mongoose from 'mongoose';
import cors from 'cors';
import dotenv from 'dotenv';
import rentalsRouter from './routes/rentals';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 5000;
const MONGO_URI = process.env.MONGO_URI || 'mongodb://mongodb:27017/flyrent';

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use('/api/rentals', rentalsRouter);

app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date() });
});

// MongoDB connection
mongoose
  .connect(MONGO_URI)
  .then(() => {
    console.log('Connected to MongoDB successfully at:', MONGO_URI);
    app.listen(PORT, () => {
      console.log(`FlyRent backend running on port ${PORT}`);
    });
  })
  .catch((err) => {
    console.error('Failed to connect to MongoDB:', err);
    // Allow fallback or retry logic in Docker
    process.exit(1);
  });
