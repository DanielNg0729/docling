"""Guarded import of the optional ``pylatexenc`` dependency.

``pylatexenc`` is only installed by the ``format-latex`` extra, but
``DocumentConverter`` imports every backend eagerly, so importing it directly at
module load would break ``import docling`` on installs that omit the extra (the
slim packages in particular). We import it here behind a guard and re-export the
node classes used across the latex backend; the failure is surfaced with a clear
message only when a LaTeX document is actually parsed (see
``LatexDocumentBackend.__init__``), mirroring the email/markdown/opendocument/
xbrl backends.

See https://github.com/docling-project/docling/issues/3740.
"""

from __future__ import annotations

PYLATEXENC_AVAILABLE: bool = False
PYLATEXENC_IMPORT_ERROR: ImportError | None = None

_INSTALL_HINT = (
    "The 'pylatexenc' package is required to parse LaTeX (.tex) documents. "
    "Install it with `pip install 'docling[format-latex]'`."
)

try:  # pragma: no cover - import-time guard
    from pylatexenc.latexwalker import (
        LatexCharsNode,
        LatexEnvironmentNode,
        LatexGroupNode,
        LatexMacroNode,
        LatexMathNode,
        LatexWalker,
        LatexWalkerParseError,
    )

    PYLATEXENC_AVAILABLE = True
except ImportError as e:  # pragma: no cover - import-time guard
    PYLATEXENC_IMPORT_ERROR = e

    # Sentinels so the rest of the latex backend can be imported without
    # pylatexenc present. These are only ever dereferenced while parsing a
    # LaTeX document, which is gated by ``raise_if_unavailable()`` below.
    LatexCharsNode = None  # type: ignore[assignment,misc]
    LatexEnvironmentNode = None  # type: ignore[assignment,misc]
    LatexGroupNode = None  # type: ignore[assignment,misc]
    LatexMacroNode = None  # type: ignore[assignment,misc]
    LatexMathNode = None  # type: ignore[assignment,misc]
    LatexWalker = None  # type: ignore[assignment,misc]
    LatexWalkerParseError = None  # type: ignore[assignment,misc]


def raise_if_unavailable() -> None:
    """Raise a helpful ImportError if ``pylatexenc`` is not installed."""
    if not PYLATEXENC_AVAILABLE:
        raise ImportError(_INSTALL_HINT) from PYLATEXENC_IMPORT_ERROR


__all__ = [
    "PYLATEXENC_AVAILABLE",
    "LatexCharsNode",
    "LatexEnvironmentNode",
    "LatexGroupNode",
    "LatexMacroNode",
    "LatexMathNode",
    "LatexWalker",
    "LatexWalkerParseError",
    "raise_if_unavailable",
]
