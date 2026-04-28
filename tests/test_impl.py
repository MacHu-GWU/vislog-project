# -*- coding: utf-8 -*-

import pytest
from vislog.impl import (
    format_line,
    format_ruler,
    AlignEnum,
)
from conftest import logger, SHOW_LOG


@pytest.fixture(autouse=True)
def _toggle_vislog(request):
    if "no_toggle" in request.keywords:
        yield
    else:
        if SHOW_LOG:
            print("")
        with logger.disabled(disable=not SHOW_LOG):
            yield


class TestFormatLine:
    def test_basic(self):
        assert format_line("hello") == "| hello"

    def test_nesting(self):
        assert format_line("hello", nest=1) == "| | hello"
        assert format_line("hello", nest=1, _pipes=["| ", "# "]) == "| # hello"

    def test_indent(self):
        assert format_line("hello", indent=1) == "|   hello"

    def test_indent_and_nesting(self):
        assert format_line("hello", indent=1, nest=1) == "| |   hello"
        assert (
            format_line("hello", indent=1, nest=1, _pipes=["| ", "# "])
            == "| #   hello"
        )

    def test_pipes_length_mismatch(self):
        with pytest.raises(ValueError):
            format_line("hello", indent=1, nest=1, _pipes=["| "])


class TestFormatRuler:
    def test_basic(self):
        assert format_ruler("Hello", length=40) == (
            "---------------- Hello -----------------"
        )

    def test_short_length(self):
        assert format_ruler("Hello", length=20) == "------ Hello -------"

    def test_custom_char(self):
        assert format_ruler("Hello", char="=", length=40) == (
            "================ Hello ================="
        )

    def test_corner(self):
        assert format_ruler("Hello", corner="+", length=40) == (
            "+--------------- Hello ----------------+"
        )

    def test_align_left(self):
        assert format_ruler("Hello", align=AlignEnum.left, length=40) == (
            "----- Hello ----------------------------"
        )

    def test_align_right(self):
        assert format_ruler("Hello", align=AlignEnum.right, length=40) == (
            "---------------------------- Hello -----"
        )

    def test_left_padding(self):
        assert format_ruler(
            "Hello", left_padding=3, align=AlignEnum.left, length=40
        ) == ("--- Hello ------------------------------")

    def test_right_padding(self):
        assert format_ruler(
            "Hello", right_padding=3, align=AlignEnum.right, length=40
        ) == ("------------------------------ Hello ---")

    def test_nesting(self):
        assert format_ruler(
            "Hello", right_padding=3, align=AlignEnum.right, length=40, nest=1
        ) == ("| ---------------------------- Hello ---")
        assert format_ruler(
            "Hello", right_padding=3, align=AlignEnum.right, length=40, nest=2
        ) == ("| | -------------------------- Hello ---")

    def test_pipes_length_mismatch(self):
        with pytest.raises(ValueError):
            format_ruler("Hello", _pipes=["|"])


class TestVisLogNested:
    def test_nested_context_manager(self):
        output = logger.ruler("section 1")
        assert "section 1" in output

        output = logger.info("hello 1")
        assert output == "| hello 1"

        with logger.nested():
            output = logger.ruler("section 1.1")
            assert "section 1.1" in output

            output = logger.info("hello 1.1")
            assert output == "| | hello 1.1"

            with logger.nested():
                output = logger.info("hello 1.1.1")
                assert output == "| | | hello 1.1.1"

    def test_nested_pipe_custom(self):
        with logger.nested(pipe="# "):
            output = logger.info("test")
            assert output == "| # test"


@pytest.mark.no_toggle
class TestVisLogDisabled:
    def test_disabled_suppresses_output(self, capfd):
        logger.info("before")
        captured = capfd.readouterr()
        assert "before" in captured.out

        with logger.disabled(disable=True):
            logger.info("hidden")
            captured = capfd.readouterr()
            assert captured.out == ""

        logger.info("after")
        captured = capfd.readouterr()
        assert "after" in captured.out

    def test_disabled_false_does_not_suppress(self, capfd):
        with logger.disabled(disable=False):
            logger.info("visible")
            captured = capfd.readouterr()
            assert "visible" in captured.out


class TestVisLogIndent:
    def test_basic_indent(self):
        output = logger.info("a")
        assert output == "| a"

        with logger.indent():
            output = logger.info("b")
            assert output == "|   b"

            with logger.indent():
                output = logger.info("c")
                assert output == "|     c"

            output = logger.info("d")
            assert output == "|   d"

        output = logger.info("e")
        assert output == "| e"

    def test_indent_level(self):
        with logger.indent(2):
            output = logger.info("y")
            assert output == "|     y"

    def test_indent_param_in_info(self):
        output = logger.info("z", indent=2)
        assert output == "|     z"


class TestVisLogPipe:
    def test_pipe_context_manager(self):
        output = logger.info("a")
        assert output == "| a"

        with logger.pipe("*"):
            output = logger.info("b")
            assert output == "* b"

        output = logger.info("c")
        assert output == "| c"


class TestVisLogRuler:
    def test_ruler_returns_formatted_string(self):
        output = logger.ruler("test")
        assert "test" in output
        assert output.startswith("+")
        assert output.endswith("+")

    def test_ruler_with_nesting(self):
        with logger.nested():
            output = logger.ruler("nested ruler")
            assert "| +" in output
            assert "nested ruler" in output


class TestPrettyLog:
    def test_pretty_log_success(self):
        results = []

        @logger.pretty_log()
        def my_func():
            results.append(logger.info("inside"))

        my_func()
        assert results[0] == "| inside"

    def test_pretty_log_exception(self):
        @logger.pretty_log()
        def failing_func():
            raise ValueError("boom")

        with pytest.raises(ValueError, match="boom"):
            failing_func()

    def test_pretty_log_with_pipe(self):
        results = []

        @logger.pretty_log(pipe="# ")
        def piped_func():
            results.append(logger.info("inside"))

        piped_func()
        assert results[0] == "# inside"

    def test_pretty_log_nested_exception(self):
        @logger.pretty_log()
        def inner():
            logger.info("inner")
            raise Exception("inner error")

        @logger.pretty_log()
        def outer():
            logger.info("outer")
            with logger.nested():
                inner()

        with pytest.raises(Exception, match="inner error"):
            outer()


class TestStartAndEnd:
    def test_start_and_end_success(self):
        results = []

        @logger.start_and_end(msg="My Func", pipe="# ")
        def my_func(name: str):
            results.append(logger.info(f"{name} working"))

        my_func(name="alice")
        assert results[0] == "# alice working"

    def test_start_and_end_exception(self):
        @logger.start_and_end(msg="Bad Func", pipe="# ")
        def bad_func(name: str):
            raise ValueError("fail")

        with pytest.raises(ValueError, match="fail"):
            bad_func(name="bob")


class TestEmojiBlock:
    def test_emoji_block(self):
        results = []

        @logger.emoji_block(msg="Deploy {app_name}", emoji="\U0001f680")
        def deploy(app_name: str):
            results.append(logger.info("working"))
            results.append(logger.info("done"))

        deploy(app_name="my_app")
        assert results[0] == "\U0001f680 working"
        assert results[1] == "\U0001f680 done"


if __name__ == "__main__":
    from vislog.tests import run_cov_test

    run_cov_test(
        __file__,
        "vislog.impl",
        preview=False,
    )
