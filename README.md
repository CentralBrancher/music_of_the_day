# Music of the Day

**Music of the Day** is an end-to-end generative system that transforms the *semantic state of daily news* into an expressive ensemble composition.

Each day, the project ingests real-world events, analyzes their meaning and dynamics, and produces a unique piece of music that reflects how the world feels *today* while remembering how it felt *yesterday*.

> *A living musical diary of global semantics.*

---

## What It Does

On every run, the system:

1. Fetches daily news from configurable RSS sources  
2. Embeds and analyzes semantic meaning  
3. Tracks change, novelty, and narrative momentum over time  
4. Maps semantic features to musical intent  
5. Composes expressive music (MIDI)  
6. Renders high-quality audio (WAV)  
7. Writes a natural-language explanation of the result  

All in **one command**.

---

## Architecture Overview
```bash
News → Embeddings → Semantic Features → Musical Intent → MIDI → WAV
                  ↑
                  Temporal Memory
```

---

## Repository Structure
```bash
music-of-the-day/
├── assets/
│ └── soundfonts/ # SoundFont for WAV rendering
├── configs/
│ ├── sources.yaml # RSS feeds & ingestion config
├── outputs/
│ └── YYYY-MM-DD/
│ ├── music.mid
│ ├── music.wav
│ └── explanation.txt
├── scripts/
│ ├── run_daily.py # One-command daily runner
├── src/music_of_the_day/
│ ├── ingestion/ # News fetching & normalization
│ ├── semantics/ # Embeddings, features, memory
│ ├── mapping/ # Semantics → music
│ ├── music/ # MIDI + WAV generation
│ ├── explain/ # Textual explanation
│ └── pipeline.py # Orchestration
├── tests/ # Unit tests
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## Semantic Layer

### News Ingestion
- Pulls articles via RSS feeds (configured in `configs/sources.yaml`)
- Normalizes and cleans text
- Designed for extensibility (additional sources, APIs)

### Embeddings
- Uses transformer-based sentence embeddings (e.g. **All-mpnet-base-v2**)
- Produces per-article vectors
- Aggregates into a **daily semantic embedding**

### Semantic Features

The system extracts interpretable features such as:

- **Semantic shift** – how much today diverges from recent history  
- **Semantic novelty** – how unusual today’s topics are  
- **Topic structure**
  - Number of topics
  - Topic dominance
  - Topic entropy  
- **Intra-day dispersion** – diversity within today’s news  
- **Semantic velocity** – day-over-day movement  
- **Semantic acceleration** – change in velocity  
- **Narrative phase** – inferred global state  
  (`build_up`, `climax`, `aftermath`, `stasis`)

### Temporal Memory
- Daily embeddings are persisted
- Rolling averages supported
- Semantic velocity stored across days
- Enables continuity and long-form evolution

---

## Semantics → Music Mapping

Semantic features are translated into **musical intent**, expressed as high-level forces that guide composition rather than fixed musical facts:

- **Harmonic color** (bright / dark / ambiguous)
- **Base tempo** (global pacing anchor)
- **Dynamic intensity curve** (energy over time)
- **Tension curve** (harmonic and emotional pressure)
- **Texture density curve** (orchestration thickness)
- **Emotional vector** *(valence, arousal, tension)*
- **Motion profile** (`drift`, `rise`, `wave`, `collapse`)
- **Duration** (overall temporal scale)

Instead of prescribing notes or keys directly, this layer shapes how the music *behaves* over time—serving as the creative bridge between semantic meaning and audible form.

---

## Music Generation

### Composition

Music is generated from `MusicIntent` using **instrument-specific renderers** built on `pretty_midi`.  
Rather than a single solo instrument, the system produces a small **ensemble texture** driven by shared semantic curves.

- Intent-driven MIDI generation using `pretty_midi`
- Multi-instrument ensemble:
  - Piano
  - Strings
  - Bass
  - Percussion
- Time-discretized rendering over semantic frames
- Probabilistic note triggering based on texture density
- Expressive control derived from intent curves:
  - **Intensity curve** → velocity and energy
  - **Density curve** → note activation probability
  - **Tension curve** → harmonic and registral pressure
  - **Motion profile** → long-range musical behavior

Musical techniques include:
- Curve-shaped dynamics over time
- Density-weighted texture emergence
- Energy-driven harmonic tension
- Narrative-aware motion (`drift`, `rise`, `wave`, `collapse`)
- Stochastic variation for organic output

---

## Running the Project

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python scripts/run_daily.py
```

---

Ensure you have FluidSynth installed and accessible from PATH.

---

## Tests

Run the full test suite:

```bash
pytest
```

Includes tests for:

- Semantic feature extraction

- News ingestion (mocked)

- Music generation

---

## Automation

The project is designed to support:

- Daily scheduled runs (e.g. GitHub Actions)

- Artifact uploads (MIDI, WAV, explanations)

- Long-term semantic and musical continuity
  

