from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()


app.mount("/static", StaticFiles(directory="static"), name="static")# Подключаем статические файлы


templates = Jinja2Templates(directory="templates")# Указываем директорию с шаблонами.


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Отображение стартовой страницы с приветствием пользователя.

    :param request: Объект запроса.
    :return: HTML-страница с приветствием.
    """
    return templates.TemplateResponse("index.html", {"request": request})  # Добавлен context.



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)