# The Anatomy of a Hit Song: 50 Years of Billboard Data

## What this project does
Analyzes the #1 Billboard song of each year from 1958–2021, enriched with 
Spotify audio features (tempo, energy, valence, danceability), to explore 
how the "sound" of a hit song has changed across decades.

## Data sources
- Billboard Hot 100 chart data (1958-2021) — Kaggle: dhruvildave/billboard-the-hot-100-songs
- Spotify audio features — Kaggle: thedevastator/billboard-hot-100-audio-features 
  (pre-enriched dataset, used instead of live Spotify API due to Spotify's 
  Feb 2026 policy change requiring Premium accounts for API access)

## Process so far

### 1. Data cleaning (01_eda.ipynb)
- Loaded 280,000+ row Billboard chart dataset
- Converted date strings to datetime, extracted year and decade
- Filtered to the #1 song of each year (64 songs total, ranked by weeks at #1)

### 2. Enrichment (02_spotify_enrichment.ipynb)
- Merged the 64 top songs with a pre-enriched Spotify audio features dataset
- Matched on cleaned song + artist name
- Result: 59/67 rows matched successfully (~88%)
- Removed duplicate matches (same song had multiple album entries)
- 8 songs could not be matched due to title formatting differences 
  (movie-soundtrack suffixes, punctuation, slash-combined titles) — 
  excluded from feature analysis

## What I learned
- How to clean and reshape a real-world messy dataset
- Feature engineering (decade extraction)
- Merging/joining datasets on fuzzy text keys
- Handling missing data and documenting data quality tradeoffs
- Real APIs have real-world constraints (Spotify's policy change) — 
  had to adapt the project plan mid-way

  ### 3. Analysis (03_analysis.ipynb)
- Computed decade-level averages for all 6 audio features
- Found major trends: acousticness dropped ~5x (1950s→2020s), 
  valence peaked in 1970s then declined, tempo rose steadily and 
  peaked in the 2010s
- Flagged and investigated a 2020s danceability anomaly, which led to 
  discovering and fixing a Christmas song data artifact (see "Data quality" 
  section below) and a small sample size limitation (see "Limitations" 
  section below)
  
### Data quality: Christmas song artifact
Initial "#1 song per year" logic picked "All I Want For Christmas Is You" 
for both 2020 and 2021, since Mariah Carey's song returns to #1 every 
December due to seasonal streaming, distorting decade averages. 
Fixed by counting weeks-at-#1 within each specific year (not lifetime 
total), correctly surfacing "The Box" (2020) and "Butter" (2021) as 
that year's true chart-topping hits.

### Data quality: unmatched songs (9 of 64)
9 songs could not be matched to Spotify audio features. Investigation 
revealed two distinct causes:

**Title/formatting mismatches (7 songs):**
- Combined/extended titles: "Aquarius/Let The Sunshine In (The Flesh 
  Failures)", "End Of The Road (From 'Boomerang')", "Candle In The Wind 
  1997/Something About The Way You Look Tonight"
- Remix suffix: "Macarena (Bayside Boys Mix)"
- Special characters/stylization: "TiK ToK" (Ke$ha)
- Possibly absent or differently catalogued: "The Ballad Of The Green 
  Berets" (1966), "We Are The World" (1985)

**Confirmed dataset coverage gap (1 song):**
- "Butter" by BTS (2021) — verified by searching all 22 BTS entries in 
  the enriched dataset; the song is genuinely not present, likely because 
  the dataset was compiled before this song's release or update cycle.

This distinction matters: formatting mismatches could theoretically be 
fixed with better text-matching logic, while coverage gaps cannot be 
fixed without a more recent or complete data source.

### Limitation: small sample per decade
Each decade average is based on only ~10 songs (one #1 song per year). 
This makes some features (energy, valence, speechiness) noisy and 
sensitive to individual outlier songs, while stronger trends 
(acousticness) are more robust because the shift is large and consistent 
across multiple decades. A larger sample (e.g. top 10 songs per year) 
would produce more statistically reliable decade averages.

## Key findings

1. **Acousticness collapsed over 50 years** — from 0.83 average in the 1950s 
   to 0.10 by the 2000s, staying low since. This is the strongest, most 
   reliable trend in the dataset.

2. **Acousticness is the central "hub" feature** — it's negatively correlated 
   with energy (-0.58), danceability (-0.62), and valence (-0.39). As hit 
   songs moved away from acoustic instruments, they became more energetic, 
   happier, and more danceable — three shifts that appear to be linked to 
   one underlying change in production style.

3. **Energy and valence are strongly linked** (correlation: 0.69) — 
   high-energy hit songs also tend to sound more positive/happy.

4. **Valence (happiness) peaked in the 1970s** and has generally declined 
   since, though the pattern is noisy due to small sample size per decade.

5. **Speechiness rose sharply in the 2000s-2010s**, likely reflecting 
   hip-hop and rap's growing influence on the pop charts during that period.