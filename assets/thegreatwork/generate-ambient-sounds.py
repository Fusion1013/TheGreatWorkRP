import subprocess
import yaml
from pathlib import Path

SOUNDS_DIR = Path("sounds")
OUTPUT_DIR = Path("ambient_sounds")
NAMESPACE = "thegreatwork"

OVERLAP_SECONDS = 3

OUTPUT_DIR.mkdir(exist_ok=True)


def get_duration(file_path: Path) -> float:
    """Get audio duration using ffprobe."""
    result = subprocess.run(
        [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(file_path)
        ],
        capture_output=True,
        text=True,
        check=True
    )
    return float(result.stdout.strip())


def build_internal_name(file_path: Path) -> str:
    # sounds/sfx/impact.ogg → sfx.impact
    relative = file_path.relative_to(SOUNDS_DIR).with_suffix("")
    return ".".join(relative.parts)


def build_key(internal_name: str) -> str:
    return f"{NAMESPACE}:{internal_name}"


def write_yaml(file_path: Path, data: dict):
    output_file = OUTPUT_DIR / f"{file_path.stem}.yml"

    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f, sort_keys=False)


def main():
    count = 0

    for file in SOUNDS_DIR.rglob("*.ogg"):
        internal_name = build_internal_name(file)
        key = build_key(internal_name)
        length = round(get_duration(file))

        data = {
            "internal_name": internal_name,
            "key": key,
            "length_seconds": length,
            "overlap_seconds": OVERLAP_SECONDS
        }

        write_yaml(file, data)
        count += 1

    print(f"Generated {count} YAML files in {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()