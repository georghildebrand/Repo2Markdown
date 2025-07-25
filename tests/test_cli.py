"""
Tests for CLI functionality.
"""

import tempfile

from pathlib import Path
from unittest import TestCase
from unittest.mock import patch
import argparse

from repo2ai.cli import (
    create_parser,
    validate_arguments,
    process_ignore_patterns,
    main,
)
from repo2ai.core import RepoFile, ScanResult


class TestCLIParser(TestCase):
    """Test CLI argument parsing."""

    def setUp(self):
        """Set up test parser."""
        self.parser = create_parser()

    def test_basic_parsing(self):
        """Test basic argument parsing."""
        args = self.parser.parse_args(["."])
        self.assertEqual(args.path, ".")
        self.assertFalse(args.clipboard)
        self.assertFalse(args.stdout)
        self.assertIsNone(args.output)

    def test_output_options(self):
        """Test output option parsing."""
        args = self.parser.parse_args(["--output", "test.md", "--clipboard", "."])
        self.assertEqual(args.output, Path("test.md"))
        self.assertTrue(args.clipboard)
        self.assertFalse(args.stdout)

    def test_filtering_options(self):
        """Test filtering option parsing."""
        args = self.parser.parse_args(
            [
                "--ignore",
                "*.tmp",
                "--ignore",
                "*.log",
                "--exclude-meta-files",
                "--max-file-size",
                "500000",
                ".",
            ]
        )
        self.assertEqual(args.ignore, ["*.tmp", "*.log"])
        self.assertTrue(args.exclude_meta_files)
        self.assertEqual(args.max_file_size, 500000)

    def test_help_message(self):
        """Test that help message is properly formatted."""
        with self.assertRaises(SystemExit):
            self.parser.parse_args(["--help"])

    def test_verbose_flag(self):
        """Test verbose flag parsing."""
        args = self.parser.parse_args(["-v", "."])
        self.assertTrue(args.verbose)

        args = self.parser.parse_args(["--verbose", "."])
        self.assertTrue(args.verbose)

        args = self.parser.parse_args(["."])
        self.assertFalse(args.verbose)


class TestArgumentValidation(TestCase):
    """Test argument validation."""

    def setUp(self):
        """Set up test directory."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_path = Path(self.temp_dir)

    def tearDown(self):
        """Clean up test directory."""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_valid_directory(self):
        """Test validation of valid directory."""
        args = argparse.Namespace(
            path=str(self.test_path),
            max_file_size=1024,
            output=None,
            prompt=None,
            open_chat=None,
            chat_all=False,
            clipboard=False,
        )

        # Should not raise exception
        validate_arguments(args)

    def test_nonexistent_directory(self):
        """Test validation of non-existent directory."""
        args = argparse.Namespace(
            path="/nonexistent/path",
            max_file_size=1024,
            output=None,
            prompt=None,
            open_chat=None,
            chat_all=False,
            clipboard=False,
        )

        with self.assertRaises(SystemExit):
            validate_arguments(args)

    def test_file_instead_of_directory(self):
        """Test validation when path is file instead of directory."""
        test_file = self.test_path / "test.txt"
        test_file.write_text("test")

        args = argparse.Namespace(
            path=str(test_file),
            max_file_size=1024,
            output=None,
            prompt=None,
            open_chat=None,
            chat_all=False,
            clipboard=False,
        )

        with self.assertRaises(SystemExit):
            validate_arguments(args)

    def test_invalid_max_file_size(self):
        """Test validation of invalid max file size."""
        args = argparse.Namespace(
            path=str(self.test_path),
            max_file_size=0,
            output=None,
            prompt=None,
            open_chat=None,
            chat_all=False,
            clipboard=False,
        )

        with self.assertRaises(SystemExit):
            validate_arguments(args)


class TestIgnorePatterns(TestCase):
    """Test ignore pattern processing."""

    def test_process_ignore_patterns(self):
        """Test processing ignore patterns."""
        args = argparse.Namespace(
            ignore=["*.tmp", "*.log"],
            exclude_meta=["README.md"],
            include_meta=None,
            exclude_meta_files=False,
        )

        patterns = process_ignore_patterns(args)
        expected = ["*.tmp", "*.log", "README.md"]
        self.assertEqual(patterns, expected)

    def test_no_ignore_patterns(self):
        """Test when no ignore patterns are specified."""
        args = argparse.Namespace(
            ignore=None, exclude_meta=None, include_meta=None, exclude_meta_files=False
        )

        patterns = process_ignore_patterns(args)
        self.assertEqual(patterns, [])


class TestCLIIntegration(TestCase):
    """Test CLI integration."""

    def setUp(self):
        """Set up test repository."""
        self.temp_dir = tempfile.mkdtemp()
        self.repo_path = Path(self.temp_dir)

        # Create test files
        (self.repo_path / "test.py").write_text('print("Hello")')
        (self.repo_path / "README.md").write_text("# Test Repository")

    def tearDown(self):
        """Clean up test repository."""
        import shutil

        shutil.rmtree(self.temp_dir)

    @patch("repo2ai.cli.scan_repository")
    @patch("repo2ai.cli.generate_markdown")
    @patch("repo2ai.cli.handle_output")
    def test_main_function(self, mock_output, mock_generate, mock_scan):
        """Test main function execution."""
        from repo2ai.cli import main
        from repo2ai.core import ScanResult, RepoFile

        # Mock scan result
        mock_file = RepoFile(
            path=self.repo_path / "test.py",
            content='print("Hello")',
            size=15,
            language="python",
        )
        mock_scan_result = ScanResult(
            files=[mock_file],
            repo_root=self.repo_path,
            total_size=15,
            ignored_files=[],
            included_files=[],
        )

        mock_scan.return_value = mock_scan_result
        mock_generate.return_value = "# Test Markdown"

        # Test with mocked arguments
        test_args = ["repo2ai", str(self.repo_path), "--stdout"]

        with patch("sys.argv", test_args):
            main()

        # Verify mocks were called
        mock_scan.assert_called_once()
        mock_generate.assert_called_once_with(mock_scan_result)
        mock_output.assert_called_once()

    @patch("repo2ai.cli.handle_output")
    @patch("repo2ai.cli.generate_markdown")
    @patch("repo2ai.cli.scan_repository")
    def test_verbose_integration(self, mock_scan, mock_generate, mock_output):
        """Test CLI with verbose flag captures stderr output."""
        from io import StringIO

        # Create mock result with verbose data
        mock_file = RepoFile(
            path=self.repo_path / "test.py",
            content='print("Hello")',
            size=15,
            language="python",
        )
        ignored_file = self.repo_path / "ignored.log"
        included_file = self.repo_path / "test.py"

        mock_scan_result = ScanResult(
            files=[mock_file],
            repo_root=self.repo_path,
            total_size=15,
            ignored_files=[ignored_file],
            included_files=[included_file],
        )

        mock_scan.return_value = mock_scan_result
        mock_generate.return_value = "# Test Markdown"

        # Test with verbose flag
        test_args = ["repo2ai", str(self.repo_path), "--verbose", "--stdout"]

        with patch("sys.argv", test_args):
            with patch("sys.stderr", new_callable=StringIO) as mock_stderr:
                main()

        # Verify verbose output appears in stderr
        stderr_output = mock_stderr.getvalue()
        self.assertIn("=== Verbose File Report ===", stderr_output)
        self.assertIn("Included files:", stderr_output)
        self.assertIn("Ignored files:", stderr_output)
        self.assertIn(str(included_file), stderr_output)
        self.assertIn(str(ignored_file), stderr_output)

        # Verify scan was called with verbose=True
        mock_scan.assert_called_once()
        call_kwargs = mock_scan.call_args[1]
        self.assertTrue(call_kwargs["verbose"])


if __name__ == "__main__":
    import unittest

    unittest.main()
