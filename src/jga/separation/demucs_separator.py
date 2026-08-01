"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    demucs_separator.py

Description:
    Optional Demucs based source separation adapter.

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna
All Rights Reserved.
=========================================================
"""

from jga.runtime.analysis_context import (
    AnalysisContext,
)

from .base_separator import BaseSeparator


class DemucsSeparator(BaseSeparator):
    """
    Optional source separation backend.

    The real Demucs dependency is intentionally loaded
    only during execution.
    """

    def process(
        self,
        context: AnalysisContext,
    ) -> AnalysisContext:

        try:
            import demucs  # type: ignore
        except ImportError as exc:
            raise RuntimeError(
                "Demucs backend is not installed."
            ) from exc

        raise NotImplementedError(
            "Demucs execution pipeline not implemented yet."
        )
