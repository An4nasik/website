from fastapi import FastAPI, Form, status, Request
from fastapi.responses import FileResponse, RedirectResponse, PlainTextResponse, HTMLResponse
import sqlite3
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from data.users import User
from data import db_session

app = FastAPI()
app.mount("/front", StaticFiles, "front")
con = sqlite3.connect("users_db", check_same_thread=False)
cur = con.cursor()
db_session.global_init("db/users_db")
templates = Jinja2Templates(directory="templates")


def main():
    db_session.global_init("db/users_db")
    db_sess = db_session.create_session()


@app.get("/log_in")
def log_in(request: Request, msg=""):
    return templates.TemplateResponse("log_in.html", {"request": request, "msg": msg})


@app.get("/register")
def register(request: Request, msg=""):
    return templates.TemplateResponse("register.html", {"request": request, "msg": msg})


@app.get("/style.css")
def register():
    return FileResponse("front/style.css")


@app.post("/registration")
def registration(email=Form(), password=Form(), username=Form()):
    c = {"name": username, "email": email, "password": password}
    db_sess = db_session.create_session()
    b = db_sess.query(User).filter(User.email == email).first()
    if not b:
        user = User(
            name=username,
            email=email,
        )
        user.set_password(password)
        db_sess.add(user)
        db_sess.commit()
        return RedirectResponse("/site", status_code=status.HTTP_303_SEE_OTHER, )
    else:
        return RedirectResponse("/register?msg=Данный+пользователь+уже+зарегестрирован",
                                status_code=status.HTTP_303_SEE_OTHER)


@app.post("/log_in")
def logging(email=Form(), password=Form()):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.email == email).first()
    if user and user.check_password(password):
        return RedirectResponse("/site", status_code=status.HTTP_303_SEE_OTHER)
    else:
        return RedirectResponse("/log_in?msg=Неправильный+логин+или+пароль", status_code=status.HTTP_303_SEE_OTHER)


if __name__ == '__main__':
    main()
