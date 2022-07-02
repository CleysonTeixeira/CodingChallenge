from fastapi import FastAPI
from pydantic import BaseModel

import httpx
import asyncio

from models import orm, User, Movie, Comment

class CreateUserInput(BaseModel):
    name: str
    email: str
    password: str

class CreateMovieCommentInput(BaseModel):
    comment: str

app = FastAPI()

@app.get('/healthcheck')
def healthcheck():
    return 'Ok'

@app.post('/users')
async def create_user(input: CreateUserInput):
    with orm.db_session:
        User(name=input.name, email=input.email, password=input.password)
        orm.commit()
    return input

@app.get('/users')
async def get_all_users():
    with orm.db_session:
       users = User.select()
       result = [u.name for u in users]
    return result

@app.get('/movies')
async def get_movies(movie_name: str):
    async with httpx.AsyncClient() as client:
        response = await client.get('https://omdbapi.com/?s=' + movie_name + '&type=movie&apikey=b5b36164')
        return response.json()


@app.get('/movies/{imdb_id}')
async def get_movie(imdb_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get('https://omdbapi.com/?i=' + imdb_id + '&type=movie&apikey=b5b36164')
        responseJson = response.json()

        if 'Title' not in responseJson:
            return responseJson
        
        with orm.db_session:
            movie = Movie.get(imdb_id = imdb_id)
                
            if movie is None:
                    Movie(imdb_id=responseJson['imdbID'], title=responseJson['Title'], likes_count=0)
                    orm.commit()

        return responseJson

@app.get('/movies/{imdb_id}/likes')
async def get_movie_likes(imdb_id: str):
    getMovieResponse = await get_movie(imdb_id)

    if 'Title' not in getMovieResponse:
            return getMovieResponse

    with orm.db_session:
        movie = Movie.get(imdb_id = imdb_id)

        if movie is None:
            return 'Movie not found'

        return movie.likes_count

@app.post('/movies/{imdb_id}/like')
async def set_new_like(imdb_id: str):
    getMovieResponse = await get_movie(imdb_id)

    if 'Title' not in getMovieResponse:
            return getMovieResponse

    with orm.db_session:
        movie = Movie.get(imdb_id = imdb_id)

        if movie is None:
            return 'Movie not found'

        movie.likes_count = movie.likes_count + 1
    
        orm.commit()

        return movie.likes_count

@app.get('/movies/{imdb_id}/comments')
async def get_movie_comments(imdb_id: str):
    getMovieResponse = await get_movie(imdb_id)

    if 'Title' not in getMovieResponse:
            return getMovieResponse

    with orm.db_session:
        movie = Movie.get(imdb_id = imdb_id)

        if movie is None:
            return 'Movie not found'

        comments = Comment.select(movie_id=movie.id)

        if comments is None:
            return []

        result = [c.comment for c in comments]

        return result

@app.post('/movies/{imdb_id}/comment')
async def create_movie_comment(imdb_id: str, input: CreateMovieCommentInput):
    getMovieResponse = await get_movie(imdb_id)

    if 'Title' not in getMovieResponse:
            return getMovieResponse

    with orm.db_session:
        movie = Movie.get(imdb_id = imdb_id)

        if movie is None:
            return 'Movie not found'
            
        Comment(user_id=1, movie_id=movie.id, comment=input.comment)
        orm.commit()

    return input