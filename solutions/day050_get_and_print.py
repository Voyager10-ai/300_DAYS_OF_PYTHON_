# Day 50: Get and Print
#
# Problem:
#   Write a Python class which has two methods: get_String and print_String.
#   get_String accepts a string from the user and print_String prints the string in upper case.
#   Includes input validation, multiline support, text formatting/borders, stream redirection,
#   fluent chainable API, batch processing, mock IO testing, unit tests, and Java practice.

import sys
import io
import re
import unittest
from typing import List, Dict, Tuple, Set, Any, Optional, Union, Callable, TextIO


# ─── 1. Core StringProcessor Class ─────────────────────────────────────────────


class StringProcessor:
    """
    Core class to get a string from user input or stream and print it in uppercase or formatted style.
    """

    def __init__(self, initial_text: str = ""):
        """
        Initializes StringProcessor with optional initial text.

        Args:
            initial_text: Default or starting text content.
        """
        self._text: str = str(initial_text)

    @property
    def text(self) -> str:
        """Returns the current string text."""
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        """Sets the current string text."""
        self._text = str(value)

    def get_string(
        self,
        prompt: str = "Enter a string: ",
        input_func: Callable[[str], str] = input,
    ) -> str:
        """
        Accepts a string from the user using the specified input function.

        Args:
            prompt: Prompt string displayed to the user.
            input_func: Callable used to read input (defaults to built-in input()).

        Returns:
            The acquired string.
        """
        self._text = input_func(prompt)
        return self._text

    def print_string(
        self,
        uppercase: bool = True,
        output_stream: Optional[TextIO] = None,
    ) -> str:
        """
        Prints the current string to the output stream, converted to uppercase by default.

        Args:
            uppercase: If True, converts string to uppercase before printing.
            output_stream: Output stream (defaults to sys.stdout).

        Returns:
            The printed string representation.
        """
        if output_stream is None:
            output_stream = sys.stdout

        output = self._text.upper() if uppercase else self._text
        print(output, file=output_stream)
        return output


# ─── 2. Advanced Input Handlers & Validation ───────────────────────────────────


    def get_string_with_validation(
        self,
        prompt: str = "Enter a valid string: ",
        validator: Optional[Callable[[str], bool]] = None,
        max_retries: int = 3,
        default_value: str = "",
        input_func: Callable[[str], str] = input,
    ) -> str:
        """
        Gets a string from user input with optional validation function and retry count.

        Args:
            prompt: Display prompt.
            validator: Callable returning True for valid input.
            max_retries: Number of allowed retries before falling back to default.
            default_value: Default fallback value if validation fails after retries.
            input_func: Input provider function.

        Returns:
            Validated string input or default fallback.
        """
        if validator is None:
            validator = lambda s: len(s.strip()) > 0

        for _ in range(max_retries):
            candidate = input_func(prompt)
            if validator(candidate):
                self._text = candidate
                return self._text

        self._text = default_value
        return self._text

    def get_multiline_string(
        self,
        prompt: str = "Enter multiline text (type 'END' on a new line to finish):\n",
        stop_word: str = "END",
        input_func: Callable[[str], str] = input,
    ) -> str:
        """
        Gets multiline text from user input until stop_word is encountered on its own line.

        Args:
            prompt: Prompt message.
            stop_word: Line content signaling end of multiline input.
            input_func: Input function provider.

        Returns:
            Combined multiline string text.
        """
        print(prompt, end="")
        lines: List[str] = []
        while True:
            try:
                line = input_func("")
                if line.strip() == stop_word:
                    break
                lines.append(line)
            except EOFError:
                break
        self._text = "\n".join(lines)
        return self._text

