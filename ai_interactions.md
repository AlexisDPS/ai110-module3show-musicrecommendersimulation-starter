# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked the AI to help extend my music recommender by adding five new song attributes to the dataset and updating the recommender so it could use those new features when scoring songs.

**Prompts used:**

- Update my `data/songs.csv` dataset by adding the columns `popularity`, `release_decade`, `instrumentalness`, `vocal_intensity`, and `lyrical_complexity`. Keep all existing rows, assign realistic values, and return the complete CSV.
- Update `src/recommender.py` so `load_songs()` loads the new columns using the correct data types.
- Update `score_song()` so it includes `popularity`, `instrumentalness`, and `vocal_intensity` in the recommendation score while keeping the existing scoring logic.

**What did the agent generate or change?**

The AI expanded `songs.csv` by adding five new attributes and realistic values for all 20 songs. It updated the `load_songs()` function to load the new fields and convert them to the appropriate integer or float types. It also updated the `score_song()` function so the recommender could use popularity, instrumentalness, and vocal intensity when calculating recommendation scores and explanations.

**What did you verify or fix manually?**

I manually reviewed the updated CSV to make sure all songs included the new columns and that the values were realistic. I verified that `load_songs()` converted each new field to the correct data type and that the scoring logic still worked correctly after adding the new features. I also reviewed the code to make sure the new scoring logic matched the intended design before accepting the changes.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

I used the Strategy design pattern.

**How did AI help you brainstorm or implement it?**

The AI suggested using the Strategy design pattern because all of the scoring modes use the same scoring logic and only differ in their weights. Instead of adding multiple `if` statements, it recommended creating separate strategy classes so each scoring mode could define its own weights while reusing the same scoring function.

**How does the pattern appear in your final code?**

The project contains a `ScoringStrategy` base class along with `GenreFirstStrategy`, `MoodFirstStrategy`, and `EnergyFocusedStrategy`. The selected strategy is passed into `recommend_songs()`, allowing the user to switch between different scoring modes without changing the main recommendation algorithm.

---

## Diversity Penalty Challenge

**What task did you give the agent?**

I asked the AI to add a diversity penalty so the recommender would avoid recommending too many songs by the same artist.

**Prompts used:**

- Update `recommend_songs()` so that if an artist is already represented in the selected recommendations, another song by that same artist receives a 10-point penalty before being selected.
- Keep the existing scoring strategies working and preserve the `(song, score, explanation)` return structure.
- Add an explanation such as `"artist diversity penalty (-10)"` whenever the penalty is applied.

**What did the agent generate or change?**

The AI updated `recommend_songs()` to score all songs first, then select recommendations one at a time while tracking which artists had already been chosen. Songs by artists that had already been recommended received a 10-point penalty before being considered again. It also added an explanation to show when the diversity penalty affected a recommendation.

**What did you verify or fix manually?**

I tested the recommender to confirm that songs from the same artist received the penalty and that the recommendations became more diverse. I also verified that all three scoring modes continued to work correctly after the changes.
