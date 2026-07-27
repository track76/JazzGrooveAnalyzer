# Scientific Geometry

## Purpose

Define the architectural components used to represent scientific geometric
coordinates inside the Jazz Groove Analyzer.

---

# Architecture

Observable Musical Fact
        ↓
Domain Object
        ↓
Scientific Quantity
        ↓
Scientific Coordinate
        ↓
Geometric Point
        ↓
Geometric Space

---

# Scientific Coordinate

A Scientific Coordinate is the architectural representation of exactly one
validated scientific quantity.

It does not perform measurements.

It stores the result of a scientific measurement.

---

# Geometric Point

A Geometric Point is an ordered collection of Scientific Coordinates.

It contains no musical logic.

---

# Geometric Space

A Geometric Space is a collection of Geometric Points generated from the
Representation Pipeline.

The space never modifies Domain objects.

