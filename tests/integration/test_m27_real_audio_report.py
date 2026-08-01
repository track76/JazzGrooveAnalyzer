from jga.pipeline.default_analysis_pipeline import (
    AnalysisPipeline,
)


def test_m27_real_audio_report():

    context = AnalysisPipeline().analyze(
        "recordings/III_Chet Baker - I fall in love too easily.mp3"
    )

    print()
    print("DIAGNOSTIC CONTEXT:")
    print(
        "Diagnostic exists:",
        context.behaviour_diagnostic_result is not None,
    )

    print(
        "Analytics diagnostic exists:",
        context.behaviour_analytics_result.behaviour_diagnostic_result
        is not None,
    )

    print(
        "Evidence exists:",
        context.scientific_report.scientific_evidence
        is not None,
    )

    print()
    print("CHAIN CHECK:")
    print(
        "context diagnostic:",
        context.behaviour_diagnostic_result is not None
    )

    print(
        "analytics diagnostic:",
        (
            context.behaviour_analytics_result
            .behaviour_diagnostic_result is not None
        )
        if context.behaviour_analytics_result
        else False
    )

    print(
        "report evidence:",
        (
            context.scientific_report.scientific_evidence
            is not None
        )
        if context.scientific_report
        else False
    )

    print()
    print("==============================")
    print("ANALYTICS RESULT DEBUG")
    print("==============================")

    print(
        context.behaviour_analytics_result
    )

    print(
        "Diagnostic inside analytics:",
        context.behaviour_analytics_result.behaviour_diagnostic_result
    )

    print()
    print("==============================")
    print("M27 CHAIN CHECK")
    print("==============================")

    print(
        "1. Context diagnostic:",
        context.behaviour_diagnostic_result is not None
    )

    print(
        "2. Analytics result:",
        context.behaviour_analytics_result is not None
    )

    print(
        "3. Analytics diagnostic:",
        (
            context.behaviour_analytics_result
            .behaviour_diagnostic_result
            is not None
        )
        if context.behaviour_analytics_result
        else False
    )

    print(
        "4. Scientific report:",
        context.scientific_report is not None
    )

    print(
        "5. Report evidence:",
        (
            context.scientific_report
            .scientific_evidence
            is not None
        )
        if context.scientific_report
        else False
    )

    report = (
        context.scientific_report
    )

    assert report is not None

    print()
    print("==============================")
    print("M27 REAL AUDIO REPORT")
    print("==============================")

    print(
        "Descriptor count:",
        len(
            report.descriptor_set.descriptors
        )
    )

    print(
        "Analytical structure:",
        report.analytical_structure is not None,
    )

    print(
        "Scientific evidence:",
        report.scientific_evidence is not None,
    )
