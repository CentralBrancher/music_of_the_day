# 🎶 Music of the Day

**Music of the Day** is an end-to-end generative system that transforms the *semantic state of daily news* into an expressive solo piano composition.

Each day, the project ingests real-world events, analyzes their meaning and dynamics, and produces a unique piece of music that reflects how the world feels *today* — while remembering how it felt *yesterday*.

> *A living musical diary of global semantics.*

---

## ✨ What It Does

On every run, the system:

1. 📰 Fetches daily news from configurable RSS sources  
2. 🧠 Embeds and analyzes semantic meaning  
3. 📈 Tracks change, novelty, and narrative momentum over time  
4. 🎼 Maps semantic features to musical intent  
5. 🎹 Composes expressive solo piano music (MIDI)  
6. 🔊 Renders high-quality audio (WAV)  
7. 📝 Writes a natural-language explanation of the result  

All in **one command**.

---

## 🧠 Architecture Overview
```bash
News → Embeddings → Semantic Features → Musical Intent → MIDI → WAV
                  ↑
                  Temporal Memory
```

---

## 🗂️ Repository Structure
```bash
music-of-the-day/
├── assets/
│ └── soundfonts/ # SoundFont for WAV rendering
├── configs/
│ ├── sources.yaml # RSS feeds & ingestion config
│ ├── semantic.yaml # Semantic parameters
│ └── music.yaml # Musical defaults
├── notebooks/ # Exploration & research notebooks
├── outputs/
│ └── YYYY-MM-DD/
│ ├── music.mid
│ ├── music.wav
│ └── explanation.txt
├── scripts/
│ ├── run_daily.py # One-command daily runner
│ └── backfill.py # Historical regeneration
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

## 🧠 Semantic Layer

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

## 🎼 Semantics → Music Mapping

Semantic features are translated into **musical intent**, including:

- Key and mode (major / minor)
- Tempo
- Texture density
- Harmonic dissonance
- Register focus
- Motif variation
- **Energy** (overall intensity)
- **Narrative arc** (`rise`, `wave`, `fall`)

This layer acts as the creative bridge between meaning and sound.

---

## 🎹 Music Generation

### Composition
- Generates expressive solo piano MIDI using `pretty_midi`
- Two-hand writing:
  - Right hand: evolving melodic motifs
  - Left hand: weighted harmonic support
- Musical techniques include:
  - Dynamic register expansion
  - Phrase-shaped velocity curves
  - Motif inversion and stretching
  - Energy-driven harmonic tension
  - Narrative-aware development

### Rendering
- MIDI rendered to WAV using FluidSynth
- High-quality SoundFont (`FluidR3_GM.sf2`)
- Produces ready-to-listen audio

---

## ▶️ Running the Project

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

## 🧪 Tests

Run the full test suite:

```bash
pytest
```

Includes tests for:

- Semantic feature extraction

- News ingestion (mocked)

- Music generation

---

## 🔁 Automation

The project is designed to support:

- Daily scheduled runs (e.g. GitHub Actions)

- Artifact uploads (MIDI, WAV, explanations)

- Long-term semantic and musical continuity

---

## 🌱 Optional Enhancements

- Sustain pedal and rubato

- Multi-instrument orchestration

- Web frontend or daily feed

- Public API

- Long-horizon semantic memory

--- 

## 🎨 Philosophy

### Music of the Day is not about turning news headlines into literal sounds.

It’s about capturing the motion of meaning —
how ideas shift, collide, accelerate, and settle —
and letting that motion leave a trace in music.

Some days are calm. Some days are tense.
This system listens — and plays.

--- 

## 📜 License

MIT License.
Use freely, remix boldly, credit kindly.
