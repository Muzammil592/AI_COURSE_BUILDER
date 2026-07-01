import express from 'express';
import cors from 'cors';
import mongoose from 'mongoose';
import axios from 'axios';
import { Course } from './models/Course.js';

const app = express();
const PORT = process.env.PORT || 5002;
const MONGO_URI = process.env.MONGO_URI || 'mongodb://mongodb:27017/ai_course_db';
const AI_ENGINE_URL = process.env.AI_ENGINE_URL || 'http://AISERVICE:8000';

app.use(cors());
app.use(express.json());

// Persistent Database Connection Ingress
mongoose.connect(MONGO_URI)
  .then(() => console.log('🍃 MongoDB Cluster connection successfully bound.'))
  .catch((err) => console.error('❌ MongoDB Connection Failure:', err));

// Diagnostics Endpoint
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'online',
    database: mongoose.connection.readyState === 1 ? 'Connected' : 'Disconnected',
    aiServiceTarget: AI_ENGINE_URL
  });
});

/**
 * 🚀 CORE ENGINE GENERATION ROUTE
 * Intercepts user prompt strings, delegates generation to the AISERVICE container,
 * and caches the structural blueprint mapping directly inside MongoDB.
 */
app.post('/api/courses/generate', async (req, res) => {
  try {
    const { prompt } = req.body;

    if (!prompt || !prompt.trim()) {
      return res.status(400).json({ error: 'Payload validation error: Prompt target string is mandatory.' });
    }

    const cleanPrompt = prompt.trim();

  const existingCourse = await Course.findOne({ 
    topic: { $regex: `^${cleanPrompt.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&')}$`, $options: 'i' } 
  });
    if (existingCourse) {
      console.log(`🎯 Cache Hit matching topic: [${cleanPrompt}] - Returning document record.`);
      return res.status(200).json({ source: 'database', data: existingCourse });
    }

    console.log(`🛰️ Cache Miss. Routing transmission requests directly to AI engine endpoint: ${AI_ENGINE_URL}/api/v1/generate`);

    // 2. Dispatch cross-container communication payload to the FastAPI engine
    const aiEngineResponse = await axios.post(`${AI_ENGINE_URL}/api/v1/generate`, {
      prompt: cleanPrompt
    }, {
      headers: { 'Content-Type': 'application/json' }
    });

    const validatedCourseData = aiEngineResponse.data;

    // 3. Hydrate the document map layout and persist into the database
    const newCourse = new Course({
      topic: validatedCourseData.topic,
      curriculum: validatedCourseData.curriculum
    });

    const savedCourseRecord = await newCourse.save();
    console.log(`💾 Course record matching [${cleanPrompt}] successfully committed to global storage.`);

    return res.status(201).json({ source: 'generative_engine', data: savedCourseRecord });

  } catch (error) {
    console.error('❌ Orchestrator Pipeline Interruption Error:', error.message);
    
    if (error.code === 'ECONNREFUSED') {
      return res.status(502).json({ 
        error: 'Bad Gateway: The AISERVICE pipeline container is currently unreachable or building.' 
      });
    }

    return res.status(error.response?.status || 500).json({
      error: 'Backend Orchestrator compilation failure',
      details: error.response?.data || error.message
    });
  }
});

/**
 * 📑 RETRIEVE COURSE BY ID
 */
app.get('/api/courses/:id', async (req, res) => {
  try {
    const course = await Course.findById(req.clamp.id);
    if (!course) {
      return res.status(404).json({ error: 'Requested course curriculum profile not found.' });
    }
    return res.status(200).json(course);
  } catch (error) {
    return res.status(500).json({ error: 'Failed to extract database tracking record.', details: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`🚂 Node.js Gateway Active and listening on port ingress track ${PORT}`);
});