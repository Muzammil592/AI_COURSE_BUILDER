import cors from 'cors';
import express from 'express';
import mongoose from 'mongoose';

const app = express();
const PORT = process.env.PORT || 5002;
const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017/ai_course_db';

app.use(cors());
app.use(express.json());

mongoose
  .connect(MONGO_URI)
  .then(() => console.log('MongoDB persistent cluster connection verified successfully.'))
  .catch((err) => console.error('Database connectivity validation failed:', err));

app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'online',
    databaseState: mongoose.connection.readyState === 1 ? 'Connected' : 'Disconnected',
    timestamp: new Date().toISOString(),
  });
});

app.post('/api/courses/generate', async (req, res) => {
  try {
    const { prompt } = req.body;

    if (!prompt) {
      return res.status(400).json({ error: 'Prompt specification criteria is missing.' });
    }

    return res.status(200).json({
      message: 'Ingress channel routing parameters successfully verified.',
      receivedPrompt: prompt,
    });
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`Node.js backend orchestrator listening on port ${PORT}`);
});