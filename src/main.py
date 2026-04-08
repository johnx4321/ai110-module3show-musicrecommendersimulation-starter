"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def print_recommendations(user_name: str, user_prefs: dict, songs: list, k: int = 3) -> None:
    """
    Helper function to print recommendations for a user profile.
    """
    recommendations = recommend_songs(user_prefs, songs, k=k)

    print("\n" + "=" * 70)
    print(f"🎵 {user_name.upper()}")
    print("=" * 70)
    print(f"\nUser Preferences:")
    print(f"  • Genre: {user_prefs['favorite_genre']}")
    print(f"  • Mood: {user_prefs['favorite_mood']}")
    print(f"  • Target Energy: {user_prefs['target_energy']}")
    print(f"  • Valence: {user_prefs.get('preferred_valence', 'neutral')}")
    print(f"  • Acousticness: {user_prefs.get('preferred_acousticness', 'mixed')}")
    print("\n" + "-" * 70)
    
    for i, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        print(f"\n{i}. {song['title']} by {song['artist']}")
        print(f"   Genre: {song['genre']} | Mood: {song['mood']} | Energy: {song['energy']}")
        print(f"   Score: {score:.1f} / 7.5 points")
        print(f"\n   Why this recommendation:")
        for line in explanation.split("\n"):
            print(f"   {line}")
    
    print("\n" + "=" * 70)


def main() -> None:
    # Load all songs once
    songs = load_songs("data/songs.csv")
    
    # Define three distinct user preference profiles
    users = {
        "High-Energy Pop": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.82,
            "preferred_valence": "high",
            "preferred_acousticness": "electronic"
        },
        "Chill Lofi": {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.40,
            "preferred_valence": "neutral",
            "preferred_acousticness": "acoustic"
        },
        "Deep Intense Rock": {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.91,
            "preferred_valence": "low",
            "preferred_acousticness": "electronic"
        }
    }
    
    # Print recommendations for each user profile
    for user_name, user_prefs in users.items():
        print_recommendations(user_name, user_prefs, songs, k=3)
    
    print("\n" + "=" * 70)
    print("✅ Recommendation simulation complete!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
