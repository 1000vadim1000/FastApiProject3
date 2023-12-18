from sqlalchemy import select

from models import UserModel, PostModel
from scheme import UserScheme, PostScheme
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from db_conf import get_session


class UserService:
    def __init__(
            self,
            session: AsyncSession = Depends(get_session)
    ):
        self.session = session

    async def get_user(
            self,
            user_data=UserScheme,
    ):
        query = select(UserModel).where(user_data == user_data)

        user = await self.session.execute(query)
        user = user.scalars().first()

        if user:
            return UserScheme(**user.__dict__)

    async def create_user(self,
                          user_data: UserScheme,
                          ):
        new_user = UserModel(name=user_data.name, email=user_data.email)
        self.session.add(new_user)
        await self.session.commit()
        return UserScheme(id=new_user.id, name=new_user.name, email=new_user.email)

    async def update_user(self,
                          id: int = None,
                          name: str = None,
                          email: str = None,
                          ):
        user = await self.session.execute(select(UserModel).where(UserModel.id == id))
        user = user.scalars().first()

        if name:
            user.name = name
        if email:
            user.email = email

        await self.session.commit()

        if user:
            return UserScheme(**user.__dict__)

    async def delete_user(self,
                          id: int = None
                          ):
        user = await self.session.execute(select(UserModel).where(UserModel.id == id))
        user = user.scalars().first()
        await self.session.execute(user)
        await self.session.commit()
        return UserScheme(**user.__dict__)


class PostService:
    def __init__(
            self,
            session: AsyncSession = Depends(get_session)
    ):
        self.session = session

    async def get_post(
            self,
            id: int = None,
    ):
        query = select(PostModel).where(PostModel.post_id == id)

        post = await self.session.execute(query)
        post = post.scalars().first()

        return PostScheme(**post.__dict__)

    async def create_post(
            self,
            post_data: PostScheme,
    ):
        new_post = PostModel(title=post_data.title, content=post_data.content, user_id=post_data)
        self.session.add(new_post)
        await self.session.commit()

        return PostScheme(post_id=new_post.post_id, title=new_post.title, content=new_post.content,
                          user_id=new_post.user_id)

    async def update_post(self,
                          post_id: int = None,
                          content: str = None,
                          title: str = None,
                          ):
        post = await self.session.execute(select(PostModel).where(PostModel.post_id == post_id))
        post = post.scalars().first()

        if content:
            post.content = content
        if title:
            post.title = title

        if post:
            return PostScheme(**post.__dict__)
