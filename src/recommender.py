import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

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

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": int(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
                "popularity": int(row["popularity"]),
                "release_decade": int(row["release_decade"]),
                "instrumentalness": float(row["instrumentalness"]),
                "vocal_intensity": float(row["vocal_intensity"]),
                "lyrical_complexity": float(row["lyrical_complexity"]),
            })
    return songs

# Default point values for each scoring factor. A scoring "mode" is just a
# different version of these weights, which is what makes the Strategy
# pattern below so simple: every mode reuses the exact same math in
# score_song(), just with bigger or smaller numbers plugged in.
DEFAULT_WEIGHTS: Dict[str, float] = {
    "genre": 30,
    "mood": 25,
    "energy": 15,
    "valence": 15,
    "tempo": 15,
    "popularity": 15,
    "instrumentalness": 15,
    "vocal_intensity": 15,
}

def score_song(user_prefs: Dict, song: Dict, weights: Optional[Dict[str, float]] = None) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    `weights` controls how many points each factor is worth. If you don't
    pass any, DEFAULT_WEIGHTS is used (this is what the ScoringStrategy
    classes below do, to implement different scoring modes).
    """
    if weights is None:
        weights = DEFAULT_WEIGHTS

    score = 0.0
    reasons = []

    genre_weight = weights.get("genre", 0)
    if song["genre"] == user_prefs["genre"]:
        score += genre_weight
        reasons.append(f"genre match (+{genre_weight:.1f})")

    mood_weight = weights.get("mood", 0)
    if song["mood"] == user_prefs["mood"]:
        score += mood_weight
        reasons.append(f"mood match (+{mood_weight:.1f})")

    energy_weight = weights.get("energy", 0)
    energy_points = energy_weight * (1 - abs(song["energy"] - user_prefs["energy"]))
    score += energy_points
    reasons.append(f"energy similarity (+{energy_points:.1f})")

    if "valence" in user_prefs:
        valence_weight = weights.get("valence", 0)
        valence_points = valence_weight * (1 - abs(song["valence"] - user_prefs["valence"]))
        score += valence_points
        reasons.append(f"valence similarity (+{valence_points:.1f})")

    if "tempo" in user_prefs:
        tempo_weight = weights.get("tempo", 0)
        tempo_points = tempo_weight * (1 - abs(song["tempo_bpm"] - user_prefs["tempo"]) / 100)
        tempo_points = max(0, tempo_points)
        score += tempo_points
        reasons.append(f"tempo similarity (+{tempo_points:.1f})")

    if "popularity" in user_prefs:
        popularity_weight = weights.get("popularity", 0)
        popularity_points = popularity_weight * (1 - abs(song["popularity"] - user_prefs["popularity"]) / 100)
        popularity_points = max(0, popularity_points)
        score += popularity_points
        reasons.append(f"popularity similarity (+{popularity_points:.1f})")

    if "instrumentalness" in user_prefs:
        instrumentalness_weight = weights.get("instrumentalness", 0)
        instrumentalness_points = instrumentalness_weight * (1 - abs(song["instrumentalness"] - user_prefs["instrumentalness"]))
        score += instrumentalness_points
        reasons.append(f"instrumentalness similarity (+{instrumentalness_points:.1f})")

    if "vocal_intensity" in user_prefs:
        vocal_intensity_weight = weights.get("vocal_intensity", 0)
        vocal_intensity_points = vocal_intensity_weight * (1 - abs(song["vocal_intensity"] - user_prefs["vocal_intensity"]))
        score += vocal_intensity_points
        reasons.append(f"vocal intensity similarity (+{vocal_intensity_points:.1f})")

    return score, reasons

class ScoringStrategy:
    """
    Base class for a scoring "mode".

    This is the Strategy pattern: each subclass below is an interchangeable
    algorithm (a different set of weights) that plugs into the same
    recommend_songs() function. main.py picks a strategy object and passes
    it in, without recommend_songs() needing to know which mode it is.

    We chose Strategy (over, say, if/elif branches in score_song) because
    every mode shares the *same* math -- only the weights change. That
    means adding a new mode later is just adding a new small class with its
    own weights dict, instead of editing scoring logic in multiple places.
    """
    name = "Default"
    weights = DEFAULT_WEIGHTS

    def score(self, user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
        return score_song(user_prefs, song, self.weights)

class GenreFirstStrategy(ScoringStrategy):
    """Cares most about matching the user's favorite genre."""
    name = "Genre-First"
    weights = {**DEFAULT_WEIGHTS, "genre": 50, "mood": 15, "energy": 10}

class MoodFirstStrategy(ScoringStrategy):
    """Cares most about matching the user's favorite mood."""
    name = "Mood-First"
    weights = {**DEFAULT_WEIGHTS, "genre": 15, "mood": 50, "energy": 10}

class EnergyFocusedStrategy(ScoringStrategy):
    """Cares most about matching the user's target energy level."""
    name = "Energy-Focused"
    weights = {**DEFAULT_WEIGHTS, "genre": 15, "mood": 15, "energy": 50}

# Lets main.py look up a strategy by name (e.g. from user input) instead of
# importing every strategy class individually.
SCORING_STRATEGIES: Dict[str, "ScoringStrategy"] = {
    "genre-first": GenreFirstStrategy(),
    "mood-first": MoodFirstStrategy(),
    "energy-focused": EnergyFocusedStrategy(),
}

def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    strategy: Optional[ScoringStrategy] = None,
) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    `strategy` picks the scoring mode (Genre-First, Mood-First,
    Energy-Focused, ...). If you don't pass one, the default weights are
    used, matching the previous behavior of this function.

    To keep the final list from being dominated by one artist, every time a
    song is picked we remember its artist. If a later song shares that
    artist, it loses 10 points for each recommendation already picked from
    them (an "artist diversity penalty") before it gets picked.
    """
    if strategy is None:
        strategy = ScoringStrategy()

    ARTIST_DIVERSITY_PENALTY = 10

    # Score every song once, up front, using the chosen strategy.
    candidates = []
    for song in songs:
        score, reasons = strategy.score(user_prefs, song)
        candidates.append((song, score, reasons))

    recommendations = []
    artist_pick_counts: Dict[str, int] = {}

    # Pick songs one at a time so the diversity penalty (which depends on
    # what's already been picked) can affect who gets picked next.
    for _ in range(min(k, len(candidates))):
        best_choice = None  # (index, adjusted_score, penalty)

        for i, (song, score, reasons) in enumerate(candidates):
            prior_picks = artist_pick_counts.get(song["artist"], 0)
            penalty = ARTIST_DIVERSITY_PENALTY * prior_picks
            adjusted_score = score - penalty

            if best_choice is None or adjusted_score > best_choice[1]:
                best_choice = (i, adjusted_score, penalty)

        best_index, adjusted_score, penalty = best_choice
        song, _, reasons = candidates.pop(best_index)

        final_reasons = list(reasons)
        if penalty > 0:
            final_reasons.append(f"artist diversity penalty (-{penalty})")
        explanation = ", ".join(final_reasons)

        recommendations.append((song, adjusted_score, explanation))
        artist_pick_counts[song["artist"]] = artist_pick_counts.get(song["artist"], 0) + 1

    return recommendations
