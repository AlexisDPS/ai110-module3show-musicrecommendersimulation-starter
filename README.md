# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.
My design is a simple content-based recommender. It compares the features of the songs to the preferences stored in a user's profile. Real world platforms might also use collaborative filtering and user behavior, but this system focuses on matching song attributes to what the user says they enjoy.
Some prompts to answer:

- What features does each `Song` use in your system
  Each `Song` stores information such as its genre, mood, energy, valence, and tempo in beats per minute.
- What information does your `UserProfile` store
  The `UserProfile` stores the user's preferred genre, mood, energy level, valence, and tempo.
- How does your `Recommender` compute a score for each song
  The `Recommender` computes a score for each song by checking how closely the song matches the user's preferences. Genre and mood can receive points when they match exactly. Numerical features such as energy, valence, and tempo receive higher scores when their values are closer to the user's preferred values. The individual feature scores are then combined into one overall score.
- How do you choose which songs to recommend
  After every song receives a score, the recommender sorts the songs from highest score to lowest score. The highest-scoring songs are considered the best matches and are selected as the recommendations.

- Algorithm Recipe
  My recommender compares each of the songs to the user's preferences. It gives 30 points for a matching genre and 25 points for a matching mood. It also gives up to 15 similarity points each for energy, valence, and tempo based on how close the song's values are to the user's preferred values. After calculating the total score for every song, the songs are sorted going from highest score to lowest score, and then the highest-scoring songs are recommended.

- Potential Biases
  This recommender might over prioritize genre and mood because exact matches receive a large part of the total score. It may also miss songs that are very similar but belong to a different genre or mood label. Since this is a content-based recommender, it does not learn from other users' listening habits or discover unexpected recommendations like collaborative filtering systems can.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

   ```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
Top recommendations:

1. Sunrise City (Score: 69.70)
   Because: genre match (+30), mood match (+25), energy similarity (+14.7)
----------------------------------------

2. Gym Hero (Score: 43.05)
   Because: genre match (+30), energy similarity (+13.1)
----------------------------------------

3. Rooftop Lights (Score: 39.40)
   Because: mood match (+25), energy similarity (+14.4)
----------------------------------------

4. Neon Sermon (Score: 15.00)
   Because: energy similarity (+15.0)
----------------------------------------

5. Night Drive Loop (Score: 14.25)
   Because: energy similarity (+14.2)
----------------------------------------
```

**Screenshot or video** _(optional)_: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this
