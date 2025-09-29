import pandas as pd

# 전처리
def normalize_games(results):
    rows = []
    for g in results:
        # 장르 첫 항목
        genres = g.get("genres", []) or []
        first_genre = genres[0]["name"] if genres else None

        # 태그 첫 항목의 games_count
        tags = g.get("tags", []) or []
        first_games_count = tags[0].get("games_count") if tags else None

        rows.append({
            "game_id": g.get("id"),
            "name": g.get("name"),
            "playtime": g.get("playtime"),
            "rating": g.get("rating"),
            "genre": first_genre,
            "games_count": first_games_count,
        })

    # 데이터프레임으로 반환
    return pd.DataFrame(rows)
