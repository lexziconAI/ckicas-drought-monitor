#!/usr/bin/env node
/**
 * Eco Dairy Bot - Node.js Backend
 * Integrates with AXIOM-X system and provides API endpoints
 */

import express from 'express';
import cors from 'cors';
import { WebSocketServer } from 'ws';
import { GoogleGenerativeAI } from '@google/generative-ai';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const PORT = process.env.PORT || 8001;

// Middleware
app.use(cors());
app.use(express.json());

// Initialize Gemini AI
const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY || process.env.GEMINI_API_KEY);

// Routes
app.get('/', (req, res) => {
  res.json({
    status: "Eco Dairy Bot API Running",
    version: "1.0.0",
    backend: "Node.js",
    endpoints: [
      "GET /",
      "POST /generate/narrative",
      "POST /generate/image",
      "WebSocket /ws/conversation"
    ]
  });
});

app.post('/generate/narrative', async (req, res) => {
  try {
    const { prompt } = req.body;

    if (!prompt) {
      return res.status(400).json({ error: "Prompt is required" });
    }

    // Use Gemini for narrative generation
    const model = genAI.getGenerativeModel({ model: "gemini-2.5-pro" });
    const result = await model.generateContent(
      `Generate a short, engaging narrative continuation for a branching scenario. The user's choice led to this. Keep it to one or two paragraphs. Prompt: "${prompt}"`
    );

    const narrative = result.response.text();

    res.json({
      narrative,
      provider: "gemini-2.5-pro",
      backend: "Node.js"
    });

  } catch (error) {
    console.error('Narrative generation error:', error);
    res.status(500).json({
      error: "Failed to generate narrative",
      details: error.message
    });
  }
});

app.post('/generate/image', async (req, res) => {
  try {
    const { prompt } = req.body;

    if (!prompt) {
      return res.status(400).json({ error: "Prompt is required" });
    }

    // Use Gemini for image generation
    const model = genAI.getGenerativeModel({
      model: "gemini-2.5-flash-image",
      generationConfig: {
        responseModalities: ["image"]
      }
    });

    const result = await model.generateContent({
      parts: [
        { text: `Create an educational image for sustainable dairy farming: ${prompt}` }
      ]
    });

    // Extract image data
    let imageData = null;
    for (const part of result.response.candidates[0].content.parts) {
      if (part.inlineData) {
        imageData = part.inlineData.data;
        break;
      }
    }

    if (!imageData) {
      throw new Error("No image generated");
    }

    res.json({
      image_url: `data:image/png;base64,${imageData}`,
      model: "gemini-2.5-flash-image",
      backend: "Node.js"
    });

  } catch (error) {
    console.error('Image generation error:', error);
    res.status(500).json({
      error: "Failed to generate image",
      details: error.message
    });
  }
});

// WebSocket server for live conversation
const wss = new WebSocketServer({ noServer: true });

wss.on('connection', (ws) => {
  console.log('WebSocket client connected');

  ws.on('message', (message) => {
    console.log('Received:', message.toString());
    // Echo back for now - can be extended for actual conversation logic
    ws.send(JSON.stringify({
      type: 'message',
      data: `Echo: ${message.toString()}`,
      timestamp: new Date().toISOString()
    }));
  });

  ws.on('close', () => {
    console.log('WebSocket client disconnected');
  });

  // Send initial connection confirmation
  ws.send(JSON.stringify({
    type: 'connected',
    message: 'WebSocket connection established',
    backend: 'Node.js'
  }));
});

// Upgrade HTTP server to handle WebSocket
const server = app.listen(PORT, () => {
  console.log(`🚀 Eco Dairy Bot API running on port ${PORT}`);
  console.log(`📡 WebSocket available at ws://localhost:${PORT}/ws/conversation`);
});

server.on('upgrade', (request, socket, head) => {
  if (request.url === '/ws/conversation') {
    wss.handleUpgrade(request, socket, head, (ws) => {
      wss.emit('connection', ws, request);
    });
  } else {
    socket.destroy();
  }
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('Shutting down gracefully...');
  server.close(() => {
    console.log('Server closed');
    process.exit(0);
  });
});

process.on('SIGINT', () => {
  console.log('Received SIGINT, shutting down gracefully...');
  server.close(() => {
    console.log('Server closed');
    process.exit(0);
  });
});