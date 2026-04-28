.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.2.2 (2026-04-28)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- Add ``vislog.VisLog.on`` and ``vislog.VisLog.off`` methods for imperative logger enable/disable control.
- Add ``vislog.api`` module as an alternative import path.
- Include a Claude Code agent skill (``.claude/skills/vislog/SKILL.md``) with self-contained usage guide, so AI assistants can correctly use ``vislog`` in any project.

**Minor Improvements**

- Modernize type hints for Python 3.10+: replace ``typing.Optional[X]`` with ``X | None``, ``typing.List`` with ``list``, ``typing.Callable`` with ``collections.abc.Callable``. Remove ``import typing`` entirely.
- Replace deprecated ``datetime.utcnow()`` with ``datetime.now(tz=timezone.utc)``.
- Drop Python < 3.10 support (``requires-python = ">=3.10"``).
- Migrate project skeleton from ``setup.py`` to ``pyproject.toml`` + ``uv`` + ``mise``.
- Rewrite tests: split monolithic ``test()`` into 33 independent pytest test cases with proper assertions on return values. Add ``conftest.py`` with ``SHOW_LOG`` toggle for visual debugging.


0.1.1 (2024-06-16)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- First release
- Add the following public API:
    - ``vislog.AlignEnum``
    - ``vislog.VisLog``
    - ``vislog.VisLog.pipe``
    - ``vislog.VisLog.ruler``
    - ``vislog.VisLog.indent``
    - ``vislog.VisLog.nested``
    - ``vislog.VisLog.pretty_log``
    - ``vislog.VisLog.start_and_end``
    - ``vislog.VisLog.emoji_block``
    - ``vislog.VisLog.disabled``
