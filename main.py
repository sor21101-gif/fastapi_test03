from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import text
from sqlalchemy.orm import Session

from database import get_db

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "fortuneToday": "동쪽으로 가면 귀인을 만나요"
        }
    )


@app.get("/post", response_class=HTMLResponse)
def getPosts(request: Request, db: Session = Depends(get_db)):
    query = text("""
        SELECT num, writer, title, content, created_at
        FROM post
        ORDER BY num DESC
    """)
    result = db.execute(query)
    posts = result.fetchall()

    return templates.TemplateResponse(
        request=request,
        name="post/list.html",
        context={
            "posts": posts
        }
    )


@app.get("/post/new", response_class=HTMLResponse)
def postNewForm(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="post/new-form.html"
    )


@app.post("/post/new")
def postNew(
    writer: str = Form(...),
    title: str = Form(...),
    content: str = Form(...),
    db: Session = Depends(get_db)
):
    query = text("""
        INSERT INTO post (writer, title, content)
        VALUES (:writer, :title, :content)
    """)
    db.execute(query, {
        "writer": writer,
        "title": title,
        "content": content
    })
    db.commit()

    return RedirectResponse("/post", status_code=302)


# ✔️ 여러 개 선택 삭제
@app.post("/post/delete")
def delete_posts(
    post_ids: list[int] = Form(...),
    db: Session = Depends(get_db)
):
    query = text("""
        DELETE FROM post
        WHERE num IN :ids
    """)
    db.execute(query, {"ids": tuple(post_ids)})
    db.commit()

    return RedirectResponse("/post", status_code=302)