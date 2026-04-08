from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 3) -> List[Song]:
        """
        Generates top-K song recommendations for a user.
        
        Args:
            user: UserProfile object with taste preferences
            k: Number of recommendations to return (default: 3)
        
        Returns:
            List of top-K Song objects ranked by score
        """
        # Convert UserProfile to dictionary format
        user_prefs = {
            'favorite_genre': user.favorite_genre,
            'favorite_mood': user.favorite_mood,
            'target_energy': user.target_energy
        }
        
        # Score all songs using functional implementation
        scored_songs = []
        for song in self.songs:
            # Convert Song dataclass to dict for scoring
            song_dict = {
                'id': song.id,
                'title': song.title,
                'artist': song.artist,
                'genre': song.genre,
                'mood': song.mood,
                'energy': song.energy,
                'tempo_bpm': song.tempo_bpm,
                'valence': song.valence,
                'danceability': song.danceability,
                'acousticness': song.acousticness
            }
            
            score, _ = score_song(user_prefs, song_dict)
            scored_songs.append((song, score))
        
        # Sort by score descending
        scored_songs.sort(key=lambda x: x[1], reverse=True)
        
        # Return top-K as Song objects
        return [song for song, score in scored_songs[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """
        Explains why a song was recommended to a user.
        
        Args:
            user: UserProfile object
            song: Song object to explain
        
        Returns:
            Detailed explanation of the scoring breakdown
        """
        # Convert to dict format for scoring
        user_prefs = {
            'favorite_genre': user.favorite_genre,
            'favorite_mood': user.favorite_mood,
            'target_energy': user.target_energy
        }
        
        song_dict = {
            'id': song.id,
            'title': song.title,
            'artist': song.artist,
            'genre': song.genre,
            'mood': song.mood,
            'energy': song.energy,
            'tempo_bpm': song.tempo_bpm,
            'valence': song.valence,
            'danceability': song.danceability,
            'acousticness': song.acousticness
        }
        
        score, explanation = score_song(user_prefs, song_dict)
        
        # Format the explanation with song info
        header = f"Recommendation: {song.title} by {song.artist}"
        separator = "=" * len(header)
        final_score = f"Final Score: {score:.1f} / 7.5 points"
        
        return f"{separator}\n{header}\n{separator}\n\n{explanation}\n\n{final_score}"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    songs = []
    
    try:
        with open(csv_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric fields to appropriate types
                song = {
                    'id': int(row['id']),
                    'title': row['title'],
                    'artist': row['artist'],
                    'genre': row['genre'],
                    'mood': row['mood'],
                    'energy': float(row['energy']),
                    'tempo_bpm': float(row['tempo_bpm']),
                    'valence': float(row['valence']),
                    'danceability': float(row['danceability']),
                    'acousticness': float(row['acousticness'])
                }
                songs.append(song)
        
        print(f"Successfully loaded {len(songs)} songs.")
        return songs
    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_path}")
        return []
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return []

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 3) -> List[Tuple[Dict, float, str]]:
    """
    Generates top-K song recommendations based on user preferences.
    
    Process:
    1. Score each song using score_song()
    2. Sort by score (descending)
    3. Return top K recommendations with scores and explanations
    
    Args:
        user_prefs: User preference dictionary with keys:
                   - favorite_genre
                   - favorite_mood
                   - target_energy
                   - preferred_valence (optional)
                   - preferred_acousticness (optional)
        songs: List of song dictionaries
        k: Number of recommendations to return (default: 3)
    
    Returns:
        List of tuples: (song_dict, score, explanation)
        Sorted by score in descending order
    """
    # Score all songs
    scored_songs = []
    
    for song in songs:
        score, explanation = score_song(user_prefs, song)
        scored_songs.append((song, score, explanation))
    
    # Sort by score descending
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    
    # Return top K
    return scored_songs[:k]

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """
    Scores a song based on user preferences using point-based system.
    
    Scoring Rules:
    - Genre match: +1.0 point Modified from original 2.0 to balance with other factors
    - Mood match: +1.0 point
    - Energy distance: 0-6.0 points based on proximity modified from original 0-5.0 to give more weight to energy matching
    - Valence match: +1.0 point (if applicable)
    - Acousticness match: +0.5 points (if applicable)
    
    Returns:
        Tuple of (total_score, explanation_string)
    """
    score = 0.0
    breakdown = []
    
    # 1. Genre Matching: +1.0
    if user_prefs['favorite_genre'] == song['genre']:
        score += 1.0
        breakdown.append(f"✓ Genre match ('{song['genre']}') +1.0")
    else:
        breakdown.append(f"✗ Genre mismatch (user: '{user_prefs['favorite_genre']}', song: '{song['genre']}')")
    
    # 2. Mood Matching: +1.0
    if user_prefs['favorite_mood'] == song['mood']:
        score += 1.0
        breakdown.append(f"✓ Mood match ('{song['mood']}') +1.0")
    else:
        breakdown.append(f"✗ Mood mismatch (user: '{user_prefs['favorite_mood']}', song: '{song['mood']}')")
    
    # 3. Energy Distance: 0-6.0 based on proximity to target
    energy_diff = abs(user_prefs['target_energy'] - song['energy'])
    
    if energy_diff <= 0.05:
        energy_points = 6.0
        energy_reason = "very close (±0.05)"
    elif energy_diff <= 0.15:
        energy_points = 4.0
        energy_reason = "close (±0.15)"
    elif energy_diff <= 0.30:
        energy_points = 2.0
        energy_reason = "acceptable (±0.30)"
    else:
        energy_points = 0.0
        energy_reason = "too different"
    
    score += energy_points
    breakdown.append(f"Energy: {song['energy']} vs target {user_prefs['target_energy']} "
                    f"(diff: {energy_diff:.2f}, {energy_reason}) +{energy_points}")
    
    # 4. Valence Preference (if specified)
    preferred_valence = user_prefs.get('preferred_valence', 'neutral')
    if preferred_valence != 'neutral':
        if preferred_valence == 'high' and song['valence'] >= 0.70:
            score += 1.0
            breakdown.append(f"✓ Valence preference (high brightness) +1.0")
        elif preferred_valence == 'low' and song['valence'] <= 0.40:
            score += 1.0
            breakdown.append(f"✓ Valence preference (dark mood) +1.0")
        else:
            breakdown.append(f"✗ Valence mismatch (user: {preferred_valence}, song: {song['valence']:.2f})")
    
    # 5. Acousticness Preference (if specified)
    preferred_acousticness = user_prefs.get('preferred_acousticness', 'mixed')
    if preferred_acousticness != 'mixed':
        if preferred_acousticness == 'acoustic' and song['acousticness'] >= 0.70:
            score += 0.5
            breakdown.append(f"✓ Acousticness preference (acoustic) +0.5")
        elif preferred_acousticness == 'electronic' and song['acousticness'] <= 0.30:
            score += 0.5
            breakdown.append(f"✓ Acousticness preference (electronic) +0.5")
        else:
            breakdown.append(f"✗ Acousticness mismatch (user: {preferred_acousticness}, song: {song['acousticness']:.2f})")
    
    # Create explanation string
    explanation = "\n".join(breakdown)
    
    return score, explanation

