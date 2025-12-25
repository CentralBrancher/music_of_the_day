import os
import sys
from datetime import date
from pathlib import Path

from music_of_the_day.ingestion.fetch_news import fetch_news
from music_of_the_day.ingestion.normalize import normalize_text
from music_of_the_day.pipeline import run_pipeline
from music_of_the_day.music.ensemble import render_ensemble
from music_of_the_day.music.render import render_midi_to_wav
from music_of_the_day.explain.explanation import generate_explanation
from music_of_the_day.semantics.storage.rolling import (
    save_embeddings,
    load_latest_embeddings,
    compute_rolling_average
)
from music_of_the_day.semantics.storage.velocity import (
    save_velocity,
    load_latest_velocity
)
from music_of_the_day.semantics.storage.emotion import (
    save_emotion,
    load_latest_emotion
)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    
    today = date.today().isoformat()

    # --- Step 1: Fetch news ---
    articles = fetch_news(limit=7)
    if not articles:
        print("No articles fetched. Exiting.")
        return

    # --- Step 2: Normalize text ---
    normalized_articles = [normalize_text(a) for a in articles]

    # --- Step 3: Load previous embeddings for continuity ---
    rolling_embeddings = compute_rolling_average(n=14)  # avg of last 14 days
    embedding_yesterday = load_latest_embeddings()
    velocity_yesterday = load_latest_velocity()
    emotion_yesterday = load_latest_emotion()

    # --- Step 4: Run pipeline (compute embeddings today internally) ---
    features, intent, daily_embedding = run_pipeline(
        articles=normalized_articles,
        rolling_embeddings=rolling_embeddings,
        embedding_yesterday=embedding_yesterday,
        velocity_yesterday=velocity_yesterday,
        emotion_yesterday=emotion_yesterday
    )

    # --- Step 5: Save today's embeddings for next day's continuity ---
    save_embeddings(daily_embedding)
    save_velocity(features.semantic_velocity)
    save_emotion(features.emotion)

    # --- Step 6: Prepare output directory ---
    out_dir = Path("outputs") / today
    out_dir.mkdir(parents=True, exist_ok=True)
    midi_path = out_dir / "music.mid"
    wav_path = out_dir / "music.wav"

    # --- Step 7: Generate MIDI ---
    render_ensemble(
        intent=intent,
        output_path=str(midi_path)
    )

    # --- Step 8: Render WAV ---
    render_midi_to_wav(
        midi_path=str(midi_path),
        wav_path=str(wav_path),
        soundfont_path="assets/soundfonts/FluidR3_GM.sf2"
    )

    # --- Step 9: Generate explanation ---
    explanation = generate_explanation(features, intent)
    (out_dir / "explanation.txt").write_text(explanation)

    print(f"- Music of the Day generated for {today}:")
    print(f"- MIDI: {midi_path}")
    print(f"- WAV: {wav_path}")
    print(f"- Explanation: {out_dir / 'explanation.txt'}")


if __name__ == "__main__":
    main()
