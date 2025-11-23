from fastapi import FastAPI, HTTPException, Request
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
# -----------------------------
# CARREGAR DADOS
# -----------------------------
ratings = pd.read_csv('data/ratings.csv')
movies = pd.read_csv('data/movies.csv')

# Conjuntos auxiliares
known_users = set(ratings["userId"].unique())
known_movies = set(movies["movieId"].unique())

# Templates HTML
templates = Jinja2Templates(directory="templates")

# -----------------------------
# MODELOS Pydantic
# -----------------------------
class UserCreate(BaseModel):
    user_id: int

class MovieCreate(BaseModel):
    movieId: int
    title: str
    genres: str = "Unknown"

class RatingUpdate(BaseModel):
    user_id: int
    movie_id: int
    rating: float


# -----------------------------
# 1. Filmes mais bem avaliados
# -----------------------------
def best_seller_recommendations_ratings(ratings, movies, top_n=10):
    movie_stats = ratings.groupby('movieId').agg(
        avg_rating=('rating', 'mean'),
        num_ratings=('rating', 'count')
    ).reset_index()

    movie_stats = movie_stats[movie_stats['num_ratings'] >= 10]
    best_sellers = movie_stats.sort_values(
        by=['avg_rating', 'num_ratings'],
        ascending=[False, False]
    )

    best_sellers = best_sellers.merge(movies, on='movieId')
    return best_sellers.head(top_n).to_dict(orient='records')


# -----------------------------
# 2. Filmes mais vistos
# -----------------------------
def most_viewed_movies(ratings, movies, top_n=10):
    movie_views = ratings.groupby('movieId').agg(
        num_ratings=('rating', 'count')
    ).reset_index()

    most_viewed = movie_views.sort_values(by='num_ratings', ascending=False)
    most_viewed = most_viewed.merge(movies, on='movieId')

    return most_viewed.head(top_n).to_dict(orient='records')


# -----------------------------
# 3. Filmes similares (item-based)
# -----------------------------
def get_similar_movies(movie_id: int, ratings, movies, top_n=10):
    user_movie_matrix = ratings.pivot_table(
        index='userId', 
        columns='movieId', 
        values='rating'
    ).fillna(0)

    user_movie_matrix = user_movie_matrix.applymap(
        lambda x: 1 if x > 0 else 0
    )

    cosine_sim = cosine_similarity(user_movie_matrix.T)
    cosine_sim_df = pd.DataFrame(
        cosine_sim, 
        index=user_movie_matrix.columns, 
        columns=user_movie_matrix.columns
    )

    if movie_id not in cosine_sim_df.index:
        raise HTTPException(status_code=404, detail="Filme não encontrado")

    similar_movies = cosine_sim_df[movie_id].sort_values(ascending=False).drop(movie_id)
    similar_movies = similar_movies.reset_index().merge(movies, on='movieId')

    return similar_movies.head(top_n).to_dict(orient='records')


# -----------------------------
# 4. Recomendação por usuários similares (user-based)
# -----------------------------
def user_based_recommendations(user_id: int, ratings, movies, top_n=10):
    user_movie_matrix = ratings.pivot_table(
        index='userId', 
        columns='movieId', 
        values='rating'
    ).fillna(0)

    user_movie_matrix = user_movie_matrix.applymap(
        lambda x: 1 if x > 0 else 0
    )

    if user_id not in user_movie_matrix.index:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    user_similarity = cosine_similarity(user_movie_matrix)
    user_similarity_df = pd.DataFrame(
        user_similarity, 
        index=user_movie_matrix.index, 
        columns=user_movie_matrix.index
    )

    similar_users = user_similarity_df[user_id].sort_values(ascending=False).drop(user_id)
    user_rated_movies = set(ratings[ratings["userId"] == user_id]["movieId"])

    recommendations = ratings[
        (ratings["userId"].isin(similar_users.index)) &
        (~ratings["movieId"].isin(user_rated_movies))
    ]

    recommendations = recommendations.groupby('movieId').agg(
        avg_rating=('rating', 'mean'),
        num_ratings=('rating', 'count')
    ).reset_index()

    recommendations = recommendations[recommendations['num_ratings'] >= 5]
    recommendations = recommendations.sort_values(
        by=['num_ratings', 'avg_rating'], 
        ascending=[False, False]
    )

    recommendations = recommendations.merge(movies, on='movieId')
    return recommendations.head(top_n).to_dict(orient='records')


# -----------------------------
# ENDPOINTS FastAPI
# -----------------------------

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/best-seller/ratings/")
async def get_best_seller_ratings(top_n: int = 10):
    return best_seller_recommendations_ratings(ratings, movies, top_n)


@app.get("/best-seller/views/")
async def get_most_viewed_movies(top_n: int = 10):
    return most_viewed_movies(ratings, movies, top_n)


@app.get("/similarity/{movie_id}")
async def get_movie_similarity(movie_id: int, top_n: int = 10):
    return get_similar_movies(movie_id, ratings, movies, top_n)


@app.get("/user-based/{user_id}")
async def get_user_recommendations(user_id: int, top_n: int = 10):
    return user_based_recommendations(user_id, ratings, movies, top_n)

@app.get("/search/movie/{name}")
async def search_movie(name: str):
    name = name.lower()
    results = movies[movies["title"].str.lower().str.contains(name)]
    return results.to_dict(orient="records")

# -----------------------------
# ENDPOINTS EXIGIDOS NO TRABALHO
# -----------------------------

@app.post("/users/")
async def add_user(user: UserCreate):
    if user.user_id in known_users:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    known_users.add(user.user_id)

    return {"message": "Usuário criado com sucesso", "user_id": user.user_id}


@app.post("/movies/")
async def add_movie(movie: MovieCreate):
    global movies

    if movie.movieId in known_movies:
        raise HTTPException(status_code=400, detail="Filme já existe")

    known_movies.add(movie.movieId)

    new_row = {
        "movieId": movie.movieId,
        "title": movie.title,
        "genres": movie.genres
    }

    movies = pd.concat([movies, pd.DataFrame([new_row])], ignore_index=True)
    return {"message": "Filme cadastrado com sucesso", "movie": new_row}


@app.post("/ratings/")
async def update_rating(rating: RatingUpdate):
    global ratings

    if rating.movie_id not in known_movies:
        raise HTTPException(status_code=404, detail="Filme não encontrado")

    if rating.user_id not in known_users:
        known_users.add(rating.user_id)

    mask = (
        (ratings['userId'] == rating.user_id) &
        (ratings['movieId'] == rating.movie_id)
    )

    if mask.any():
        ratings.loc[mask, 'rating'] = rating.rating
        action = "alterado"
    else:
        new_row = {
            "userId": rating.user_id,
            "movieId": rating.movie_id,
            "rating": rating.rating,
            "timestamp": 0
        }
        ratings = pd.concat([ratings, pd.DataFrame([new_row])], ignore_index=True)
        action = "registrado"

    return {
        "message": f"Rating {action} com sucesso",
        "user_id": rating.user_id,
        "movie_id": rating.movie_id,
        "rating": rating.rating
    }


# -----------------------------
# EXECUÇÃO LOCAL
# -----------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8081)