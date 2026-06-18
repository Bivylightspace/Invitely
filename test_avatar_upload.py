import argparse
import os
import sys


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Test the avatar upload service by generating a DiceBear avatar and uploading it to Supabase."
    )
    parser.add_argument(
        "-s",
        "--seed",
        default="testuser",
        help="Unique seed string used to generate the avatar.",
    )
    parser.add_argument(
        "-b",
        "--bucket",
        default=None,
        help="Optional Supabase avatar bucket name to override AVATAR_BUCKET_NAME.",
    )
    args = parser.parse_args()

    if args.bucket:
        os.environ["AVATAR_BUCKET_NAME"] = args.bucket

    # Import after environment variables are set so the config values are loaded correctly.
    from importlib import reload

    from api.utils import config
    from api.v1.services import avatar_service

    reload(config)
    reload(avatar_service)

    try:
        result = avatar_service.upload_default_avatar(args.seed)
    except Exception as exc:
        print("Avatar upload failed:", type(exc).__name__, str(exc), file=sys.stderr)
        return 1

    print("Avatar upload succeeded:")
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
