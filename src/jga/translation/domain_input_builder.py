"""
=========================================================
Jazz Groove Analyzer (JGA)

File:
    domain_input_builder.py
=========================================================
"""

from jga.interfaces.translation.domain_input_builder import (
    DomainInputBuilder,
)


class DefaultDomainInputBuilder(DomainInputBuilder):

    def build(self, context):
        raise NotImplementedError
