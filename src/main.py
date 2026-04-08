"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.8,
        "preferred_valence": "high",
        "preferred_acousticness": "mixed"
    }
    
    recommendations = recommend_songs(user_prefs, songs, k=3)

    print("\n" + "=" * 60)
    print("TOP MUSIC RECOMMENDATIONS")
    print("=" * 60)
    print(f"\nUser Preferences:")
    print(f"  • Genre: {user_prefs['favorite_genre']}")
    print(f"  • Mood: {user_prefs['favorite_mood']}")
    print(f"  • Target Energy: {user_prefs['target_energy']}")
    print(f"  • Valence: {user_prefs['preferred_valence']}")
    print(f"  • Acousticness: {user_prefs['preferred_acousticness']}")
    print("\n" + "-" * 60)
    
    for i, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        print(f"\n{i}. {song['title']} by {song['artist']}")
        print(f"   Genre: {song['genre']} | Mood: {song['mood']}")
        print(f"   Score: {score:.1f} / 7.5 points")
        print(f"\n   Why this recommendation:")
        for line in explanation.split("\n"):
            print(f"   {line}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
