import os
import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
from google import genai
from google.genai import types
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

app = FastAPI(title="AI Course Builder AISERVICE", version="2.0.0")

# --- Environment Ingress Configurations ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# --- Structured Pydantic Data Contracts ---
class QuizItem(BaseModel):
    question: str = Field(description="The multiple-choice question context.")
    options: List[str] = Field(description="Exactly 4 distinct plausible options.")
    correctAnswer: str = Field(description="The precise string value matching the correct option.")

class LessonItem(BaseModel):
    title: str = Field(description="Comprehensive name of the specific lesson sub-topic.")
    contentMarkdown: str = Field(description="In-depth educational content strictly written in clear Markdown format.")
    youtubeQuery: str = Field(description="An optimized, distinct search string targeting YouTube to fetch matching tutorials.")
    youtubeVideoUrl: str = Field(default="", description="Hydrated runtime URL populated dynamically by the system.")

class ModuleItem(BaseModel):
    moduleTitle: str = Field(description="High-level category block title.")
    lessons: List[LessonItem]

class CourseStructureResponse(BaseModel):
    topic: str
    curriculum: List[ModuleItem]

class GenerationRequest(BaseModel):
    prompt: str

# --- Asynchronous Helper Services ---
async def fetch_youtube_video_link(search_query: str) -> str:
    """
    Executes an asynchronous background crawl to extract the
    top-ranking video URL from the YouTube Data API.
    """
    if not YOUTUBE_API_KEY or "YOUR_FALLBACK" in YOUTUBE_API_KEY:
        return "https://www.youtube.com/watch?v=dQw4w9WgXcQ" # Graceful development fallback

    try:
        # Running in an executor to avoid blocking the main async event loop
        loop = asyncio.get_event_loop()
        def sync_youtube_call():
            youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
            request = youtube.search().list(
                q=search_query,
                part="id",
                maxResults=1,
                type="video"
            )
            return request.execute()

        response = await loop.run_in_executor(None, sync_youtube_call)
        items = response.get("items", [])
        if items:
            video_id = items[0]["id"]["videoId"]
            return f"https://www.youtube.com/embed/{video_id}"
        return ""
    except HttpError as err:
        print(f"⚠️ YouTube API quota or connectivity limit warning: {err}")
        return ""

# --- API Generation Endpoint Router ---
@app.post("/api/v1/generate", response_model=CourseStructureResponse)
async def generate_course_blueprint(payload: GenerationRequest):
    """
    Day 2 Core Generation Pipeline. Intercepts ingress prompt constraints,
    forces structural JSON compilation from Gemini, and hydrates the video tracks.
    """
    if not payload.prompt.strip():
        raise HTTPException(status_code=400, detail="Inbound prompt context string cannot be blank.")

    try:
        # Initialize Google GenAI Client
        client = genai.Client(api_key=GEMINI_API_KEY)

        system_instruction = (
            "You are an elite, production-grade educational curriculum architect. Your objective is to design a "
            "comprehensive, high-value technical course on the user's topic. You must structure the syllabus "
            "into clear modules, populate lessons with comprehensive, readable markdown content, and write "
            "precise multiple-choice questions for evaluation. You must strictly output JSON matching the exact schema."
        )

        # Enforce structural type generation directly through the model configuration
        response = client.models.generate_content(
            model='gemini-2.5-pro', # Deployed standard industry model
            contents=f"Generate a highly technical course covering the topic: {payload.prompt}",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=CourseStructureResponse,
                temperature=0.3 # Reduced variance to enforce strict factual mapping
            ),
        )

        # Parse the structural response directly into our Pydantic schema model
        course_data = CourseStructureResponse.model_validate_json(response.text)

        # --- Asynchronous Concurrent Video Hydration Processing ---
        youtube_hydration_tasks = []
        lesson_reference_pointers = []

        for module in course_data.curriculum:
            for lesson in module.lessons:
                # Capture future resolving structures in parallel
                task = fetch_youtube_video_link(lesson.youtubeQuery)
                youtube_hydration_tasks.append(task)
                lesson_reference_pointers.append(lesson)

        # Execute all scraping lookups concurrently to prevent linear blocking performance drops
        resolved_video_urls = await asyncio.gather(*youtube_hydration_tasks)

        # Map URLs back onto their respective memory pointers
        for index, video_url in enumerate(resolved_video_urls):
            lesson_reference_pointers[index].youtubeVideoUrl = video_url

        return course_data

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Pipeline Execution Exception: {str(e)}")