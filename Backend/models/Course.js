import mongoose from 'mongoose';

const QuizItemSchema = new mongoose.Schema({
  question: { type: String, required: true },
  options: [{ type: String, required: true }],
  correctAnswer: { type: String, required: true }
});

const LessonItemSchema = new mongoose.Schema({
  title: { type: String, required: true },
  contentMarkdown: { type: String, required: true },
  youtubeQuery: { type: String, required: true },
  youtubeVideoUrl: { type: String, default: "" }
});

const ModuleItemSchema = new mongoose.Schema({
  moduleTitle: { type: String, required: true },
  lessons: [LessonItemSchema]
});

const CourseSchema = new mongoose.Schema({
  topic: { type: String, required: true, index: true },
  curriculum: [ModuleItemSchema],
  createdAt: { type: Date, default: Date.now }
});

// Enforcing an index lookup optimization on the topic field
export const Course = mongoose.model('Course', CourseSchema);