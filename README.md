# codex-handson-starter-repo
Starter repo for ADs' codex vibe coding session

## Objective
Create a simple web app involving image gen that could help one of your clients. Some ideas for inspiration:
- Product images for ecommerce platforms such as Amazon/Shopee, etc
- Posters for marketing
- Workflow diagram to visualise business process
- Charcter turnaround sheets for movie / anime production

## Setup steps (ask SA/SEs to help with this setup if needed)
- in terminal, type `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r requirements.txt`
- `cp .env.example .env`
- replace `OPENAI_API_KEY` in .env with actual OpenAI API Key

## Starter Prompt for Codex
```
## Objective
Your task is to create a simple web app with Python backend and React frontend, that uses OpenAI's image-gen-1 model to edit uploaded image based on user prompt

## Frontend requirements
1. Any frontend requirements

## Backend requirements
1. Two functions to create and edit image based on image-gen-1 model is available in the utils.py folder
    1. `create_image` generates the image from image-gen-1 model, based on the input prompt and the desired output size. It returns the generated image in bytes format
    2. `edit_image` edits the image based on image-gen-1 model, taking in the editting prompt and the image bytes and returns the edited image in bytes

2. Other backend/function requirements

## Folder access
- edits the code in /backend and /frontend folder. 
- add all the necessary files for setup (e.g., package.json etc) at root folder
- strictly no access / edits in other folders

## Test
- npm run build should pass
- Screenshot the frontend, display the screenshot in preview
```