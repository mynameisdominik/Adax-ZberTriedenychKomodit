from __future__ import annotations

import argparse
import json

from .parser import parse_url


def main() -> None:
    parser = argparse.ArgumentParser(description="Parse an ADAX DOCX calendar")
    parser.add_argument("url", help="Public URL of the municipality DOCX calendar")
    args = parser.parse_args()
    print(
        json.dumps(
            [item.as_dict() for item in parse_url(args.url)],
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
