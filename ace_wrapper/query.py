#!/usr/bin/env python3
import argparse
import logging
import sys
from pathlib import Path

from auggie_sdk.context import FileSystemContext

from . import __version__

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(message)s",
    datefmt="%H:%M:%S",
    stream=sys.stderr,
)
logger = logging.getLogger("ace")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="ace",
        description="Augment Context Engine (ACE) semantic codebase retrieval wrapper.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  timeout 120s ace "How is the authentication flow implemented?" -w /path/to/project/root
  timeout 120s ace "Find where uploaded files are validated and stored" -w /path/to/project/root
  timeout 120s ace "frontend sends requestId to backend and starts a processing job" -w /path/to/project/root

Exit codes:
  0: Success (results found)
  1: Error (config, network, or path issues)

Note:
  Use this tool for conceptual, behavioral, or intent-based code search when
  exact identifiers are unknown. Treat output as candidate files/sections, not
  proof. Read returned files and use exact search (grep/rg) to confirm
  identifiers, error strings, routes, events, tests, and call sites.

  Prefer one workflow or concept per query. Split unrelated questions into
  separate searches; multi-topic queries can miss weaker subtopics.

  Semantic search may take longer than literal search; use a timeout when
  calling from agents or scripts.
  See: https://docs.augmentcode.com/context-services/sdk/overview#filesystem-context
""",
    )
    parser.add_argument("query", help="Natural-language semantic search query")
    parser.add_argument(
        "-w",
        "--workspace",
        default=".",
        help="Project root directory to search (default: .)",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Show debug logs")
    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    workspace = Path(args.workspace).resolve()
    logger.debug("Query: %s | Workspace: %s", args.query, workspace)

    if not workspace.exists():
        logger.error("Path not found: %s", workspace)
        sys.exit(1)

    try:
        with FileSystemContext.create(str(workspace)) as context:
            if sys.stderr.isatty():
                sys.stderr.write("Searching...\r")

            result = context.search(args.query)

            if sys.stderr.isatty():
                sys.stderr.write("            \r")

            if not result or (isinstance(result, str) and not result.strip()):
                logger.warning("No results found.")
                sys.exit(0)

            print(result)

    except Exception as e:
        if args.verbose:
            logger.exception("Search failed: %s", e)
        else:
            logger.error("Search failed: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
