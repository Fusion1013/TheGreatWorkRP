import json
from pathlib import Path

BASE_DIR = Path("sounds")
NAMESPACE = "thegreatwork"

OUTPUT_FILE = Path("sounds.json")


def to_sound_event(file_path: Path):
    # sounds/sfx/impact.ogg → sfx.impact
    relative = file_path.relative_to(BASE_DIR).with_suffix("")
    key = ".".join(relative.parts)

    # sfx/impact → namespace:sfx/impact
    sound_name = f"{NAMESPACE}:{relative.as_posix()}"

    return key, {
        "sounds": [
            {
                "name": sound_name,
                "volume": 1.0,
                "stream": True
            }
        ]
    }


def main():
    sounds_json = {}

    for file in BASE_DIR.rglob("*.ogg"):
        key, entry = to_sound_event(file)
        sounds_json[key] = entry

    # pretty stable output (important for version control diffs)
    OUTPUT_FILE.write_text(json.dumps(sounds_json, indent=2, sort_keys=True))

    print(f"Generated {len(sounds_json)} sound events")


if __name__ == "__main__":
    main()