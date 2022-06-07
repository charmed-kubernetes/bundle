#!/usr/bin/env python3


import argparse
import logging
import re
from contextlib import contextmanager
from pathlib import Path
from typing import List, Optional

log = logging.getLogger(__name__)
CONTAINER_IMAGE_TXT = Path(__file__).parent / "container-images.txt"


class LineNotFound(Exception):
    pass


class LineAlreadyExists(Exception):
    pass


class LineId:
    """Type to check user input is a valid line-id."""

    def __init__(self, user_input: str) -> None:
        line_id_re = re.compile(r"^v(?:\d+\.{0,1})+-(?:static|upstream)")
        valid = user_input == "ci-static" or line_id_re.match(user_input)
        if not valid:
            raise ValueError(f"{user_input} is an invalid line-id")
        self._user_input = user_input

    def __str__(self) -> str:
        return self._user_input


class Line:
    """Represents the line in the file to adjust."""

    def __init__(self, line_txt: str, line_no: int) -> None:
        self.line_no = line_no
        self.id, remainder = line_txt.split(":", 1)
        self.images = list(remainder.strip().split())
        self.new_line: Optional["Line"] = None

    @property
    def text(self):
        """Returns the value of the line as a string."""
        return f"{self.id}: {' '.join(self.images)}"

    @property
    def image_set(self):
        """Unique list of images on the line."""
        return set(self.images)

    def __add__(self, others: List[str]):
        """Add a list of images to the line.

        Eliminates dupilicates and preserves order
        """
        dedupe = self.image_set & set(others)
        additions = set(others) - dedupe
        self.images += sorted(additions)

    def __sub__(self, others: List[str]):
        """Remove a list of images from the line, while preserving order."""
        for image in others:
            try:
                self.images.remove(image)
            except ValueError:
                log.info(
                    f"Can't remove {image} from {self.id} as it doesn't exist"
                )

    def copy(self, line_id: str):
        with _at_line(line_id) as line:
            if line.line_no > 0:
                raise LineAlreadyExists(
                    f"Cannot copy-to line because {line_id} already exists"
                )
        text = f"{line_id}: {' '.join(self.images)}"
        self.new_line = Line(text, -1)


def _arguments():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("line_id", type=LineId, help="Name of line to adjust")
    parser.add_argument(
        "operation",
        type=str,
        choices=["create", "add-to", "delete-from", "copy-from"],
        help="Operation to perform on this line\n\n"
        "create: generates a new line with all the images\n"
        "add-to: updates line to include the images without removing others\n"
        "delete-from: updates line to remove only the listed images\n"
        "copy-from: duplicates line_id to new line with new_line_id\n",
    )
    parser.add_argument(
        "--new_line_id", type=LineId, help="Name of copied line"
    )
    parser.add_argument(
        "--images",
        type=str,
        nargs="+",
        help="List of images to apply in this action",
    )
    return parser.parse_args()


@contextmanager
def _at_line(line_id):
    all_lines = CONTAINER_IMAGE_TXT.read_text().splitlines()
    matches = []
    for line_no, line_text in enumerate(all_lines):
        if line_text.startswith(f"{line_id}: "):
            matches.append((line_no, line_text))

    if len(matches) == 0:
        line_no, line_text = -1, f"{line_id}: "
    elif len(matches) == 1:
        line_no, line_text = matches[0]
    else:
        raise ValueError(f"File Error, more than one line with {line_id}")

    line = Line(line_text, line_no)
    yield line

    if line.line_no >= 0:
        all_lines[line_no] = line.text
    else:
        all_lines.append(line.text)

    if line.new_line:
        all_lines.append(line.new_line.text)

    CONTAINER_IMAGE_TXT.write_text("\n".join(all_lines))


def create(args):
    """Generates a new line."""
    with _at_line(args.line_id) as line:
        if line.line_no >= 0:
            raise LineAlreadyExists(
                f"Cannot create line because {args.line_id} already exists"
            )
        line += args.images


def add_to(args):
    """Adds images to existing line."""
    with _at_line(args.line_id) as line:
        if line.line_no < 0:
            raise LineNotFound(
                f"Cannot alter line because {args.line_id} doesn't exist"
            )
        line += args.images


def delete_from(args):
    """Removes images from existing line."""
    with _at_line(args.line_id) as line:
        if line.line_no < 0:
            raise LineNotFound(
                f"Cannot alter line because {args.line_id} doesn't exist"
            )
        line -= args.images


def copy_from(args):
    """Copies existing line to new line."""
    with _at_line(args.line_id) as line:
        if line.line_no < 0:
            raise LineNotFound(
                f"Cannot copy line because {args.line_id} doesn't exist"
            )
        line.copy(args.new_line_id)


def main():
    """Handles key operations."""
    args = _arguments()
    if args.operation == "create":
        create(args)
    elif args.operation == "add-to":
        add_to(args)
    elif args.operation == "delete-from":
        delete_from(args)
    elif args.operation == "copy-from":
        copy_from(args)


if __name__ == "__main__":
    main()
