"""

THIS SCRIPT IS NOT TESTED!

This script needs ffmpeg

winget install Gyan.FFmpeg
(if u have winget installed)

choco install ffmpeg
(if u have choco installed)


"""

from pathlib import Path
import subprocess

AUDIO_DIR = Path("src/assets/sfx")
EXTENSIONS = {".wav", ".mp3", ".MP3"}

def convert_to_ogg(source: Path):
    target = source.with_suffix(".ogg")

    if target.exists():
        print(f"Skipping existing: {target}")
        return

    print(f"Converting: {source} -> {target}")

    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i", str(source),
            "-c:a", "libvorbis",
            "-q:a", "5",
            str(target),
        ],
        check=True,
    )

def main():
    files = [
        path for path in AUDIO_DIR.rglob("*")
        if path.is_file() and path.suffix in EXTENSIONS
    ]

    if not files:
        print("No audio files found.")
        return

    for file in files:
        convert_to_ogg(file)

    print(f"Done. Converted/skipped {len(files)} audio files.")

if __name__ == "__main__":
    main()