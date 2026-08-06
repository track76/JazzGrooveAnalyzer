# JGA Plate Rendering Specification

Author:
    Angelo Tracanna

Copyright © 2026 Angelo Tracanna

---

# Purpose

This document specifies the graphical language of the
JGA Scientific Plate.

It defines visual rules.

It does not define analytical algorithms.

All rendering technologies shall comply with this specification.

---

# Design Philosophy

The Scientific Plate is a scientific document.

Every graphical element shall communicate analytical information.

No graphical element shall be purely decorative.

Visual simplicity has priority over visual complexity.

---

# Visual Hierarchy

The Plate is organized into the following levels.

Level 0
Title

Level 1
Metadata

Level 2
Sections

Level 3
Measure Grid

Level 4
Beat Grid

Level 5
Metric Events

Level 6
Relationships

Level 7
Annotations

Level 8
Legend

---

# Typography

Title

Large
Bold
Centered

Metadata

Small
Left aligned

Measure numbers

Medium
Bold

Beat numbers

Small

Annotations

Small

Legend

Small

---

# Measure Grid

Measures are delimited by solid vertical lines.

Beat divisions use thin dashed lines.

Grid lines shall remain visually subordinate to metric events.

---

# Instrument Lanes

Each instrument occupies one horizontal lane.

Lane order shall remain deterministic.

Rhythm section ordering shall remain stable.

---

# Metric Events

Metric Events are represented by symbols.

Different event types may use different symbols.

Graphical symbols must remain readable when printed
in grayscale.

---

# Offsets

Offsets are expressed in milliseconds.

Zero offsets may be omitted to reduce visual clutter.

Positive and negative offsets shall remain visually
distinguishable.

---

# Sections

Musical sections are displayed above the measure grid.

Sections describe musical form.

Sections never modify analytical results.

---

# Time Representation

Absolute time is displayed along the bottom axis.

Metric position is displayed above the musical staff.

Both representations coexist.

---

# Scientific Consistency

Rendering shall never introduce analytical information.

Every visible element must originate from the
Scientific Plate model.

---

# Rendering Independence

This specification applies equally to

- Matplotlib

- SVG

- PDF

- HTML

- Future renderers

Graphical technology shall never affect
scientific meaning.

---

# Evolution

Future versions may extend this specification while
preserving backward compatibility of the visual language.

