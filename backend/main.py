import base64
import json
from typing import Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from backend.utils import create_image


LANGUAGES = [
    {"code": "ko", "label": "Korean"},
    {"code": "en", "label": "English"},
    {"code": "zh", "label": "Chinese"},
    {"code": "th", "label": "Thai"},
    {"code": "ms", "label": "Malaysian"},
]


class ImageRequest(BaseModel):
    caution: str = Field(..., description="오늘의 주의사항")
    location: str = Field(..., description="주의해야 하는 위치")
    checks: str = Field(..., description="마무리 작업 시 필수 확인사항")
    size: str = Field(
        "1024x1024",
        description="Image size to request from the generation model.",
        examples=["1024x1024", "1536x1024", "1024x1536", "auto"],
    )


class TranslatedFields(BaseModel):
    caution: str
    location: str
    checks: str


class GeneratedImage(BaseModel):
    language: str
    label: str
    translation: TranslatedFields
    image: str


class ImageResponse(BaseModel):
    images: List[GeneratedImage]


app = FastAPI(title="Safety Toolbox Image Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def translate_fields(payload: Dict[str, str], language: str) -> Dict[str, str]:
    from openai import OpenAI

    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "Translate the provided construction safety notes into "
                    f"{language}. Return JSON with keys caution, location, and checks only."
                ),
            },
            {
                "role": "user",
                "content": json.dumps(payload, ensure_ascii=False),
            },
        ],
    )
    content = completion.choices[0].message.content
    return json.loads(content)


def build_prompt(language: str, translated: Dict[str, str]) -> str:
    return (
        "Create a clear, modern construction site toolbox meeting safety poster in "
        f"{language}. Use bold safety colors (yellow, orange, navy), pictograms for hard hat, "
        "gloves, harness, and clear typography. Use structured bullet points with minimal text. "
        "Add a small header 'Safety Focus of the Day' and focus on clarity over ornamentation. "
        "Keep background clean with subtle diagonal stripes."
        "\nToday's caution: "
        f"{translated['caution']}"
        "\nLocation: "
        f"{translated['location']}"
        "\nFinal checks before wrap-up: "
        f"{translated['checks']}"
    )


def encode_image(image_bytes: bytes) -> str:
    return f"data:image/png;base64,{base64.b64encode(image_bytes).decode('utf-8')}"


@app.post("/api/generate", response_model=ImageResponse)
def generate_images(request: ImageRequest) -> ImageResponse:
    try:
        payload = {
            "caution": request.caution,
            "location": request.location,
            "checks": request.checks,
        }

        images: List[GeneratedImage] = []
        for language in LANGUAGES:
            translated = translate_fields(payload, language["label"])
            prompt = build_prompt(language["label"], translated)
            image_bytes = create_image(prompt, size=request.size)

            images.append(
                GeneratedImage(
                    language=language["code"],
                    label=language["label"],
                    translation=TranslatedFields(**translated),
                    image=encode_image(image_bytes),
                )
            )

        return ImageResponse(images=images)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(exc)) from exc
