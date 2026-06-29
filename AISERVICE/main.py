from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="AI Course Builder Core Engine", version="1.0.0")


class QuizItem(BaseModel):
    question: str
    options: List[str]
    correctAnswer: str


class LessonItem(BaseModel):
    title: str
    contentMarkdown: str
    youtubeQuery: str


class ModuleItem(BaseModel):
    moduleTitle: str
    lessons: List[LessonItem]


class CourseStructureResponse(BaseModel):
    topic: str
    curriculum: List[ModuleItem]


class GenerationRequest(BaseModel):
    prompt: str


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ai-core-engine"}


@app.post("/api/v1/generate", response_model=CourseStructureResponse)
async def generate_course_blueprint(payload: GenerationRequest):
    """Day 1 scaffolding endpoint for validating service-to-service payload flow."""
    if not payload.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt context string cannot be empty.")

    try:
        return {
            "topic": payload.prompt,
            "curriculum": [
                {
                    "moduleTitle": "Foundational Concept Overview",
                    "lessons": [
                        {
                            "title": f"Introduction to {payload.prompt}",
                            "contentMarkdown": (
                                f"# Deep Dive into {payload.prompt}\n\n"
                                "This is a placeholder markdown content representing Day 1 baseline "
                                "transmission metrics structural components."
                            ),
                            "youtubeQuery": f"Complete concept overview of {payload.prompt}",
                        }
                    ],
                }
            ],
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"AI Engine Exception Trace: {str(exc)}")