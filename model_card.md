# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

MuRec 1.0

## 2. Intended Use  

**Purpose:** MuRec 1.0 generates personalized song recommendations from a fixed catalog of 18 songs ranked by relevance to a user's taste profile. It suggests exactly 3 songs per request.

**Who it's for:** This system is **for classroom exploration and learning only**, not for real users. It demonstrates how simple scoring rules turn user preferences into ranked recommendations, and helps students understand where bias and limitations arise in recommendation systems.

**Key assumptions about the user:**
- Users have a **stable, well-defined taste profile** (they know their favorite genre, mood, and target energy level)
- Users want **relevance over discovery**—the system prioritizes exact matches rather than introducing serendipity or broadening taste
- Users are willing to specify optional preferences for valence and acousticness
- Users don't change preferences mid-session and don't have context-dependent moods (e.g., "I want different music for the gym vs. sleep")

**Not designed for:**
- Cold-start (new users with no preference history)
- Real-time learning from listening behavior
- Group recommendations or collaborative filtering
- Large-scale catalogs beyond 18 songs

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

**The basic idea:** MuRec treats recommendation as a matching game. You describe what you're in the mood for, and the model scores every song by counting how many of your preferences it matches. Songs with the highest scores are recommended first.

**What we ask about you:**
- Your **favorite genre** (e.g., rock, pop, lofi, jazz)
- Your **favorite mood** (e.g., happy, chill, intense, relaxed)
- Your **target energy level** (0–1 scale, where 0 is very calm and 1 is frantic)
- Optional: Do you prefer **uplifting or dark-sounding** songs? (valence)
- Optional: Do you prefer **acoustic instruments or electronic** sounds? (acousticness)

**How we score each song using a points system:**

When we compare a song to your preferences, we award points:
- **Genre match** (+1.0 point): If the song's genre exactly matches your favorite
- **Mood match** (+1.0 point): If the song's mood exactly matches your favorite
- **Energy proximity** (+0–6.0 points): This is the most important factor. If a song's energy is very close to your target (within ±0.05), you get 6 points. Slightly off (±0.15)? You get 4 points. Acceptable range (±0.30)? You get 2 points. Too different? Zero points.
- **Valence match** (+1.0 point): If you prefer bright/uplifting music and the song is bright, or you prefer dark music and it's dark
- **Acousticness match** (+0.5 points): If you prefer acoustic and the song is acoustic, or you prefer electronic and it's electronic

**The maximum possible score is 8.5 points** (all preferences aligned perfectly).

**What changed from the original logic:**
I doubled the importance of energy matching (from 0–3.0 points to 0–6.0 points) because energy is the most objective, measurable signal of what you're in the mood for. I also halved the importance of genre matching (from 2.0 to 1.0 points) so the system doesn't get stuck recommending only one genre if the energy doesn't fit. This means if you ask for high-energy rock, you might get high-energy pop or electronic instead—energy became the dominant factor.

---

## 4. Data  

**Catalog size:** 18 songs total, all from the file `data/songs.csv`.

**Genres represented:** pop, rock, indie pop, lofi, jazz, hip-hop, electronic, country, reggae, soul, folk, ambient, synthwave, classical (14 distinct genres across 18 songs).

**Moods represented:** happy, chill, intense, relaxed, moody, focused, aggressive, romantic, melancholic, uplifting, energetic, dreamy (12 distinct moods).

**Did I add or remove data:** No. I used the original 18-song starter dataset without modification.

**Coverage and gaps in musical taste:**

The dataset captures basic diversity across genres and moods, but has notable blind spots:

- **Electronic/high-energy bias**: Electronic, synthwave, and energetic songs are overrepresented (5+ songs), while classical, country, and soul have only 1 song each. A classical music fan would have very few options.
  
- **Missing song features**: The dataset lacks songs for several real-world use cases:
  - No *workout/motivational* music (high energy + aggressive energy blend is limited)
  - No *party music* (danceability varies; some high-energy songs have low tempo)
  - Underrepresentation of *sad/cathartic* songs (only 2-3 melancholic moods)
  - No *background instrumental* beyond ambient and lofi
  
- **Missing user preferences**: The scoring system doesn't consider:
  - **Tempo** (songs range 60–152 BPM, but this is completely ignored in scoring)
  - **Danceability** (useful for party or workout contexts, but not scored)
  - **Artist diversity** (no preference for familiar or new artists)
  - **Lyrical content** or language (vocal vs. instrumental, sing-along potential)
  - **Recency or trends** (all songs treated equally regardless of release context)
  - **Time of day or context** (workout, sleep, study, social gathering)

**Whose taste does this reflect:** The dataset appears to reflect a young, digital-native, streaming-platform listener who enjoys electronic and indie music. It underrepresents classical musicians, country fans, and users with diverse cultural music preferences.

---

## 5. Strengths  

**User types for which MuRec performs well:**

1. **High-energy music seekers (target_energy > 0.80)**: The system excels here because the catalog has many high-energy songs (Gym Hero 0.93, Neon Pulse 0.96, Storm Runner 0.91) and energy is the dominant scoring factor (+0–6.0 points). Users asking for intense, energetic music get tight, accurate matches.

2. **Users with matching genre-mood pairs**: When a user's preferred genre and mood combination exists in the catalog, the system recommends it reliably. For example:
   - "lofi + chill" → Strong recommendations (Library Rain, Midnight Coding both score well)
   - "pop + happy" → Sunrise City gets 2.0 genre + 1.0 mood + energy bonus
   - "rock + intense" → Storm Runner dominates

3. **Users who specify clear secondary preferences**: When a user adds valence or acousticness preferences, the system adds +1.0–0.5 bonus points that break ties effectively and provide more nuanced recommendations.

4. **Transparent and explainable recommendations**: The points-based system is simple enough for users to understand why a song ranked first. The explain_recommendation() function shows the exact breakdown (✓ Genre match +1.0, ✓ Energy very close +6.0, etc.), which builds trust and aids debugging.

**Patterns the scoring captures correctly:**

- **Energy is a reliable proxy for mood context**: A user asking for "calm music" typically wants low-energy songs (0.28–0.40), and the system correctly prioritizes Spacewalk Thoughts (0.28), Library Rain (0.35), and Whispers in the Wind (0.35).

- **Exact genre/mood matching is intuitive**: When a user says "I want jazz," they most often do want jazz. The exact-match logic works because users are assumed to know their genre preferences.

- **Energy tolerance bands (±0.05, ±0.15, ±0.30) are reasonable**: These thresholds align with human perception—a song with energy 0.76 feels subjectively closer to 0.76 than to 0.88, and the scoring reflects this.

**Test cases where recommendations felt right:**

- **"Deep Intense Rock" user** (genre: rock, mood: intense, energy: 0.91, low valence, electronic): System recommends Storm Runner first (rock + intense + 0.91 energy match = solid score), which aligns perfectly with user intent.

- **"Chill Lofi" user** (genre: lofi, mood: chill, energy: 0.40, neutral valence, acoustic): System recommends Library Rain (lofi + chill + 0.40 match) and Midnight Coding (lofi + chill), which are genre-accurate and mood-aligned.

- **Energy override case**: When a user asks for electronic/energetic music with high energy (0.96), Neon Pulse ranks top despite not perfectly matching genre/mood because the energy match is so strong (6.0 points). This felt intuitive—energy dominates, which is the design goal.

---

## 6. Limitations and Bias 

**Critical features the system ignores:**

- **Tempo (60–152 BPM range)**: Two high-energy songs can have wildly different tempos. Concrete Dreams is 92 BPM (hiphop, aggressive) while Neon Pulse is 140 BPM (electronic, energetic). A user might perceive these as completely different experiences, but MuRec scores them identically if energy matches.

- **Danceability (0.15–0.92 range)**: Concrete Dreams has 0.92 danceability while Old Guitar Tales has 0.45, but danceability is never considered. A user saying "I want party music" could get non-danceable recommendations if mood/energy match.

- **Acousticness threshold bias**: Valence requires ≥0.70 or ≤0.40 (hard cliff). Acousticness requires ≥0.70 or ≤0.30 (hard cliff). A song with 0.69 acousticness gets 0 points; 0.70 gets +0.5. This arbitrary boundary doesn't reflect gradual user preference.

- **Lyrics, context, and recency**: The system treats a classical etude, a lofi hip-hop beat, and a folk ballad as equally scorable units. In reality, context matters (workout vs. sleep), lyrics matter (sing-along vs. instrumental), and user preferences evolve (trending artists).

**Underrepresented and disadvantaged genres/moods:**

| Genre / Mood | Count | Problem |
|---|---|---|
| Electronic | 3+ songs | Overrepresented; high-energy electronic users get many hits |
| Classical | 1 song | Underrepresented; classical fans get only Moonlight Sonata |
| Country | 1 song | Only Dusty Roads (melancholic); upbeat country ignored |
| Soul | 1 song | Only Midnight Groove (romantic); soul diversity missing |
| Melancholic mood | 3 songs | Underrepresented; sad/introspective users have limited options |
| Romantic mood | 2 songs | Only Midnight Groove + Moonlight Sonata; limited romantic palettes |

**Energy dominance causes genre override:**

Because energy is now 0–6.0 out of 8.5 maximum (71%), the system can recommend a song from a completely different genre if energy matches. Example test case:
- User profile: "classical, romantic, 0.22 energy, high valence, acoustic"
- Best match: Moonlight Sonata (classical, romantic, 0.22 energy, 0.68 valence, 0.95 acoustic) → ~7.5 points
- Problem: If Moonlight Sonata were removed, the system might recommend Spacewalk Thoughts (ambient, chill, 0.28 energy, acoustic) even though ambient ≠ classical. Energy override trumps genre fidelity.

**Hard thresholds create cliff effects:**

- **Valence cliff**: Prefer "high valence"? Songs with valence 0.70–0.84 get +1.0, but 0.69 gets 0. This discontinuity doesn't match how users experience songs.
- **Acousticness cliff**: Prefer "acoustic"? Songs 0.70–0.95 get +0.5, but 0.69 gets 0. Island Vibes (0.72 acoustic) barely scrapes by.
- **Energy boundaries**: Energy thresholds (0.05, 0.15, 0.30) are absolute. A song at 0.050 energy difference scores 6.0; at 0.051 it drops to 4.0. Real preference would be more continuous.

**Unfair advantage for some user types:**

1. **High-energy seekers win**: Many catalog songs cluster at 0.75–0.96 energy. A user asking for 0.91 energy gets multiple close matches and consistently high scores.

2. **Low-energy seekers lose**: Low-energy songs are sparse (0.22–0.40 range). A classical fan wanting calm music gets only 3–4 good options.

3. **Secondary preference bias**: Users who don't specify valence/acousticness preferences miss +1.5 bonus points, but they also avoid penalty cliffs. This creates an implicit paradox: being indifferent is safer than being specific about edges.

4. **Genre-mood mismatch penalty**: A user asking for "jazz + romantic" gets Jazz (1 song, Coffee Shop Stories). But if the system can't find jazz, there's no graceful degradation—it falls back to energy only. Real recommenders would suggest semantically similar genres (e.g., "soul" as jazz alternative).

**Representation bias in the dataset:**

The 18-song catalog skews toward young, streaming-platform listeners:
- High electronic/synthwave representation (5 songs)
- Most songs are < 60 years old (implied by moods: energetic, dreamy, synthwave = recent)
- Artist names suggest indie/electronic production culture (Neon Echo, Orbit Bloom, LoRoom)
- Underrepresents classical, jazz standards, country, world music, gospel

This means:
- A 60-year-old classical enthusiast gets 1 option.
- A country music fan gets 1 option.
- An electronic music fan gets 5+ options.

---

## 7. Evaluation  

**User profiles tested:**
- "High-Energy Pop" (pop, happy, 0.82 energy)
- "Chill Lofi" (lofi, chill, 0.40 energy)
- "Deep Intense Rock" (rock, intense, 0.91 energy)
- "Energy Boundary Walker" (exact energy matches like 0.82)
- "The Contradiction" (classical + aggressive mood mismatch)
- "Complete Nomad" (rare jazz + romantic combo)

**What I looked for:**
- Do top-3 recommendations match the user's stated preferences?
- Does energy dominance override genre appropriately?
- Do hard thresholds (valence ≥0.70, acousticness ≥0.70) cause unexpected drops?
- Are recommendations transparent and explainable?

**What surprised me:**
- Energy override was more aggressive than expected: A user asking for "rock" could receive "pop" or "electronic" if energy matched, which felt both useful (flexibility) and risky (genre abandonment).
- The 18-song catalog's electronic bias became obvious: high-energy seekers got 5+ good options while classical fans got only 1.
- Hard thresholds created abrupt score cliffs: A song with 0.69 acoustic gets 0 bonus; 0.70 gets +0.5. This arbitrary boundary doesn't feel fair.

**Simple tests run:**
- **Exact energy match test**: User with target_energy = 0.82 vs. Sunrise City (0.82) → confirmed 6.0 energy points awarded
- **Genre override test**: "rock + high energy (0.96)" → System recommended Neon Pulse (electronic) over Storm Runner (rock, 0.91 energy) because Neon Pulse's 0.96 energy was closer
- **Underrepresentation test**: Asked for "classical + romantic" → Only got Moonlight Sonata; no genre degradation fallback
- **Boundary test**: Valence 0.70 vs. 0.69 → Confirmed hard cliff, no gradual scoring

---

## 8. Future Work  

1. **Add tempo and danceability scoring**: Include BPM and danceability as optional preferences (e.g., "I like danceable" or "I prefer 90–120 BPM"). This would eliminate cases where party-seekers get non-danceable songs and workout users get inappropriate tempos.

2. **Replace hard thresholds with continuous scoring**: Instead of valence ≥0.70 or ≤0.40 getting +1.0, use a smooth curve where songs closer to the preference get more points. This removes cliff effects and feels fairer at boundaries.

3. **Expand and balance the catalog**: Add more classical, country, and soul songs so all genres have equivalent representation. This would fix the electronic bias and provide low-energy seekers with more diverse options.

---

## 9. Personal Reflection  

Building MuRec taught me that recommender systems are policy decisions encoded in math. The choice to double energy from 3.0 to 6.0 points isn't just a technical tweak—it fundamentally changes whose tastes the system serves (high-energy seekers win, low-energy seekers lose). Every weighting decision, threshold boundary, and ignored feature creates winners and losers in the user population.

I was surprised by how easy it is to accidentally disadvantage entire user groups. Simply underrepresenting genres in the dataset and setting hard thresholds meant classical fans and acoustic-preference users faced structural unfairness. In real systems used by millions, these biases feel like bugs but they're often features—the system is working exactly as designed, just not fairly.

This changed how I think about Spotify, YouTube Music, and Apple Music. Those systems feel "smart" but they're actually performing weighted trade-offs: they optimize for engagement, ad-insertion, artist promotion, or catalog diversity—not always for user satisfaction. The next time I see a "recommended for you" that feels off, I'll recognize it's not a mistake—it's the system's design priorities trumping my actual preferences.

---  
