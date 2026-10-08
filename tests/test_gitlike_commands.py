#
# Copyright 2015-2026 Joe Block <jpb@unixorn.net>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import io
from unittest import mock

import pytest

import gitlike_commands
from gitlike_commands import (
    _stream_target,
    find_subcommand,
    is_program,
    subcommand_driver,
)


class TestIsProgram:
    """Tests for is_program."""

    def test_found(self):
        """A program on $PATH returns True."""
        with mock.patch.object(gitlike_commands, "which", return_value="/usr/bin/git"):
            assert is_program(name="git") is True

    def test_not_found(self):
        """A program absent from $PATH returns False."""
        with mock.patch.object(gitlike_commands, "which", return_value=None):
            assert is_program(name="definitely-not-a-real-program") is False


class TestFindSubcommand:
    """Tests for find_subcommand."""

    def test_matches_longest_command(self):
        """The longest matching command name wins, with no leftover args."""
        with mock.patch.object(gitlike_commands, "is_program", return_value=True):
            command, args = find_subcommand(args=["foo", "bar", "baz"])
        assert command == "foo-bar-baz"
        assert args == []

    def test_peels_args_until_match(self):
        """When the full name has no program, trailing args peel off until one matches."""

        def only_foo_bar(name):
            return name == "foo-bar"

        with mock.patch.object(
            gitlike_commands, "is_program", side_effect=only_foo_bar
        ):
            command, args = find_subcommand(args=["foo", "bar", "baz"])
        assert command == "foo-bar"
        assert args == ["baz"]

    def test_no_match_raises(self):
        """No executable subcommand raises RuntimeError."""
        with mock.patch.object(gitlike_commands, "is_program", return_value=False):
            with pytest.raises(RuntimeError):
                find_subcommand(args=["foo", "bar", "baz"])

    def test_single_element_never_matches(self):
        """A single-element arg list cannot match (driver would re-exec itself)."""
        with mock.patch.object(gitlike_commands, "is_program", return_value=True):
            with pytest.raises(RuntimeError):
                find_subcommand(args=["foo"])


class TestStreamTarget:
    """Tests for _stream_target."""

    def test_real_fd_passes_through(self):
        """A stream exposing a real fd is returned unchanged."""
        stream = mock.Mock()
        stream.fileno.return_value = 3
        assert _stream_target(stream=stream) is stream

    def test_fdless_stringio_returns_none(self):
        """A StringIO (no backing fd) falls back to None."""
        assert _stream_target(stream=io.StringIO()) is None

    @pytest.mark.parametrize("error", [AttributeError, OSError, ValueError])
    def test_fileno_errors_return_none(self, error):
        """Each error fileno() may raise falls back to None."""
        stream = mock.Mock()
        stream.fileno.side_effect = error
        assert _stream_target(stream=stream) is None


class TestSubcommandDriver:
    """Tests for subcommand_driver."""

    def test_runs_resolved_subcommand(self):
        """A resolved subcommand is run via check_call with routed streams."""
        with (
            mock.patch.object(
                gitlike_commands, "find_subcommand", return_value=("foo-bar", ["baz"])
            ),
            mock.patch.object(gitlike_commands.sys, "argv", ["foo", "bar", "baz"]),
            mock.patch.object(gitlike_commands.subprocess, "check_call") as check_call,
        ):
            subcommand_driver()

        check_call.assert_called_once()
        called_args, called_kwargs = check_call.call_args
        assert called_args[0] == ["foo-bar", "baz"]
        assert set(called_kwargs) == {"stdin", "stdout", "stderr"}

    def test_exits_when_only_driver_matches(self):
        """When the match is the driver script itself, exit 1 without running it."""
        with (
            mock.patch.object(
                gitlike_commands, "find_subcommand", return_value=("foo", [])
            ),
            mock.patch.object(gitlike_commands.sys, "argv", ["foo"]),
            mock.patch.object(gitlike_commands.subprocess, "check_call") as check_call,
        ):
            with pytest.raises(SystemExit) as excinfo:
                subcommand_driver()

        assert excinfo.value.code == 1
        check_call.assert_not_called()

    def test_exits_when_no_subcommand_found(self):
        """A find_subcommand failure exits 1 without running anything."""
        with (
            mock.patch.object(
                gitlike_commands, "find_subcommand", side_effect=RuntimeError("nope")
            ),
            mock.patch.object(gitlike_commands.sys, "argv", ["foo", "bar"]),
            mock.patch.object(gitlike_commands.subprocess, "check_call") as check_call,
        ):
            with pytest.raises(SystemExit) as excinfo:
                subcommand_driver()

        assert excinfo.value.code == 1
        check_call.assert_not_called()
