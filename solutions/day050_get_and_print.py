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


# ─── 3. Text Formatting Styles, Borders & Alignment ────────────────────────────


    def format_string(
        self,
        case_mode: str = "upper",
        prefix: str = "",
        suffix: str = "",
    ) -> str:
        """
        Formats current text according to specified case mode, prefix, and suffix.

        Args:
            case_mode: 'upper', 'lower', 'title', 'swapcase', 'reverse', or 'raw'.
            prefix: Optional prefix string.
            suffix: Optional suffix string.

        Returns:
            Formatted string content.
        """
        text = self._text
        if case_mode == "upper":
            text = text.upper()
        elif case_mode == "lower":
            text = text.lower()
        elif case_mode == "title":
            text = text.title()
        elif case_mode == "swapcase":
            text = text.swapcase()
        elif case_mode == "reverse":
            text = text[::-1]

        return f"{prefix}{text}{suffix}"

    def print_boxed(
        self,
        border_char: str = "*",
        padding: int = 2,
        output_stream: Optional[TextIO] = None,
    ) -> str:
        """
        Prints the text centered inside a decorative ASCII border box.

        Args:
            border_char: Character for the box border.
            padding: Space padding inside border.
            output_stream: Target stream.

        Returns:
            Boxed string content.
        """
        if output_stream is None:
            output_stream = sys.stdout

        text = self._text.upper()
        line_width = len(text) + (padding * 2)
        top_bottom = border_char * (line_width + 2)
        pad_spaces = " " * padding
        content_line = f"{border_char}{pad_spaces}{text}{pad_spaces}{border_char}"

        boxed_result = f"{top_bottom}\n{content_line}\n{top_bottom}"
        print(boxed_result, file=output_stream)
        return boxed_result

    def print_aligned(
        self,
        width: int = 60,
        align: str = "center",
        output_stream: Optional[TextIO] = None,
    ) -> str:
        """
        Prints text aligned within a fixed column width.

        Args:
            width: Column width integer.
            align: 'left', 'center', or 'right'.
            output_stream: Target stream.

        Returns:
            Aligned string.
        """
        if output_stream is None:
            output_stream = sys.stdout

        text = self._text.upper()
        if align == "center":
            aligned = text.center(width)
        elif align == "right":
            aligned = text.rjust(width)
        else:
            aligned = text.ljust(width)

        print(aligned, file=output_stream)
        return aligned


# ─── 4. Stream Redirection & File Logging Output ───────────────────────────────


    def print_to_string_io(self, uppercase: bool = True) -> str:
        """
        Prints current string into an in-memory io.StringIO buffer and returns the captured output.

        Args:
            uppercase: If True, converts text to uppercase.

        Returns:
            Captured buffer content string.
        """
        buffer = io.StringIO()
        self.print_string(uppercase=uppercase, output_stream=buffer)
        return buffer.getvalue()

    def log_string_to_file(
        self,
        file_path: Union[str, Path],
        mode: str = "a",
        encoding: str = "utf-8",
        uppercase: bool = True,
    ) -> str:
        """
        Appends or writes the formatted text to a target file.

        Args:
            file_path: Path to target file.
            mode: File mode ('a' for append, 'w' for overwrite).
            encoding: Text file encoding.
            uppercase: If True, writes in uppercase.

        Returns:
            Written string payload.
        """
        output = self._text.upper() if uppercase else self._text
        with open(file_path, mode, encoding=encoding) as f:
            f.write(output + "\n")
        return output


# ─── 5. Fluent Chainable API Interface ─────────────────────────────────────────


class StringProcessorChain:
    """
    Fluent builder interface enabling chained calls like:
    StringProcessorChain().set_text('hello').upper().reverse().print()
    """

    def __init__(self, initial_text: str = ""):
        self._text = str(initial_text)

    def set_text(self, text: str) -> "StringProcessorChain":
        self._text = str(text)
        return self

    def get_string(self, prompt: str = "Enter string: ", input_func: Callable[[str], str] = input) -> "StringProcessorChain":
        self._text = input_func(prompt)
        return self

    def upper(self) -> "StringProcessorChain":
        self._text = self._text.upper()
        return self

    def lower(self) -> "StringProcessorChain":
        self._text = self._text.lower()
        return self

    def title(self) -> "StringProcessorChain":
        self._text = self._text.title()
        return self

    def reverse(self) -> "StringProcessorChain":
        self._text = self._text[::-1]
        return self

    def strip(self) -> "StringProcessorChain":
        self._text = self._text.strip()
        return self

    def replace(self, old: str, new: str) -> "StringProcessorChain":
        self._text = self._text.replace(old, new)
        return self

    def print(self, output_stream: Optional[TextIO] = None) -> "StringProcessorChain":
        if output_stream is None:
            output_stream = sys.stdout
        print(self._text, file=output_stream)
        return self

    def to_string(self) -> str:
        return self._text


# ─── 6. Batch String Collector & Bulk Processor ────────────────────────────────


class BatchStringProcessor:
    """
    Manages a collection of strings and processes/prints them in bulk.
    """

    def __init__(self, initial_list: Optional[List[str]] = None):
        self.strings: List[str] = list(initial_list) if initial_list else []

    def add_string(self, text: str) -> None:
        self.strings.append(str(text))

    def add_strings(self, texts: List[str]) -> None:
        self.strings.extend([str(t) for t in texts])

    def print_all_uppercase(self, output_stream: Optional[TextIO] = None) -> List[str]:
        if output_stream is None:
            output_stream = sys.stdout

        upper_list = [s.upper() for s in self.strings]
        for s in upper_list:
            print(s, file=output_stream)
        return upper_list

    def get_processed_list(self, case_mode: str = "upper") -> List[str]:
        if case_mode == "upper":
            return [s.upper() for s in self.strings]
        elif case_mode == "lower":
            return [s.lower() for s in self.strings]
        elif case_mode == "title":
            return [s.title() for s in self.strings]
        elif case_mode == "reverse":
            return [s[::-1] for s in self.strings]
        return list(self.strings)


# ─── 7. Mock IO Testing Helper ─────────────────────────────────────────────────


class MockIO:
    """
    Simulates input stream injection and output capture for unit testing StringProcessor.
    """

    def __init__(self, inputs: Optional[List[str]] = None):
        self.inputs: List[str] = list(inputs) if inputs else []
        self.output_buffer: io.StringIO = io.StringIO()
        self._index = 0

    def input_func(self, prompt: str = "") -> str:
        if self._index >= len(self.inputs):
            raise EOFError("No more mock inputs available")
        val = self.inputs[self._index]
        self._index += 1
        return val

    @property
    def output_stream(self) -> io.StringIO:
        return self.output_buffer

    def get_printed_output(self) -> str:
        return self.output_buffer.getvalue()


# ─── 8. Comprehensive Unit Test Suite ─────────────────────────────────────────


class TestGetAndPrintOperations(unittest.TestCase):
    def test_get_string_and_print_uppercase(self):
        sp = StringProcessor()
        mock = MockIO(["hello python"])
        sp.get_string(input_func=mock.input_func)
        self.assertEqual(sp.text, "hello python")

        printed = sp.print_string(uppercase=True, output_stream=mock.output_stream)
        self.assertEqual(printed, "HELLO PYTHON")
        self.assertIn("HELLO PYTHON", mock.get_printed_output())

    def test_validated_input(self):
        sp = StringProcessor()
        # First 2 fail validator (len < 5), 3rd passes
        mock = MockIO(["abc", "123", "valid_length"])
        res = sp.get_string_with_validation(
            validator=lambda s: len(s) >= 5,
            input_func=mock.input_func,
        )
        self.assertEqual(res, "valid_length")

    def test_multiline_string_input(self):
        sp = StringProcessor()
        mock = MockIO(["Line 1", "Line 2", "END"])
        res = sp.get_multiline_string(stop_word="END", input_func=mock.input_func)
        self.assertEqual(res, "Line 1\nLine 2")

    def test_format_string(self):
        sp = StringProcessor("hello world")
        self.assertEqual(sp.format_string(case_mode="upper"), "HELLO WORLD")
        self.assertEqual(sp.format_string(case_mode="title"), "Hello World")
        self.assertEqual(sp.format_string(case_mode="reverse"), "dlrow olleh")

    def test_print_boxed_and_aligned(self):
        sp = StringProcessor("test")
        mock = MockIO()
        boxed = sp.print_boxed(border_char="#", output_stream=mock.output_stream)
        self.assertIn("TEST", boxed)

        aligned = sp.print_aligned(width=20, align="center", output_stream=mock.output_stream)
        self.assertEqual(len(aligned), 20)

    def test_string_io_and_file_logging(self):
        sp = StringProcessor("logged message")
        output = sp.print_to_string_io(uppercase=True)
        self.assertEqual(output.strip(), "LOGGED MESSAGE")

    def test_fluent_chaining(self):
        res = (
            StringProcessorChain()
            .set_text("python")
            .upper()
            .replace("ON", "ON 300")
            .to_string()
        )
        self.assertEqual(res, "PYTH ON 300")

    def test_batch_processing(self):
        batch = BatchStringProcessor(["apple", "banana"])
        processed = batch.get_processed_list("upper")
        self.assertEqual(processed, ["APPLE", "BANANA"])







