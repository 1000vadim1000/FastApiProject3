import uvicorn
from fastapi import Depends
from fastapi import FastAPI
from sqladmin import Admin

from db_conf import engine
from models import UserAdmin
from scheme import UserScheme, PostScheme
from service.user_service import UserService, PostService

app = FastAPI()
admin_panel = Admin(app, engine)

admin_panel.add_view(UserAdmin)


@app.get(
    path="/get_user",
)
async def get_user(
        user_data=UserScheme,
        service: UserService = Depends()
):
    user = await service.get_user(
        user_data=user_data
    )
    return user


@app.post(
    path="/create_user/",
    response_model=UserScheme
)
async def create_user(
                      user_data: UserScheme,
                      service: UserService = Depends()
):
    new_user = await service.create_user(user_data)
    return new_user


@app.put(
    path="/update_user/",
    response_model=UserScheme
)
async def update_user(
        id: int = None,
        name: str = None,
        email: str = None,
        service: UserService = Depends()
):
    user = await service.update_user(
        id=id,
        name=name,
        email=email,
    )
    return user


@app.delete(
    path="/delete_user/",
    response_model=UserScheme,
)
async def delete_user(
        id: int = None,
        service: UserService = Depends()
):
    user = await service.delete_user(
        id=id
    )
    return user


@app.post(
    path="/create_post/",
    response_model=PostScheme
)
async def create_post(
        post_data: PostScheme,
        post_service: PostService = Depends(),
):
    return await post_service.create_post(post_data)


@app.get(
    path="/get_post/",
    response_model=PostScheme
)
async def get_post(
        id: int = None,
        post_service: PostService = Depends()
):
    post = await post_service.get_post(
        id=id
    )
    return post


@app.put(
    path="/update_post/",
    response_model=PostScheme
)
async def update_post(
        post_id: int = None,
        content: str = None,
        title: str = None,
        service: PostService = Depends(),
):
    post = await service.update_post(
        post_id=post_id,
        content=content,
        title=title
    )

    return post

if __name__ == '__main__':
    uvicorn.run("main:app", host='localhost', port=8055, reload=True)
