# AD-016

## Title

Behaviour Analytics Operator Contract

## Status

LOCKED

## Context

Behaviour Analytics introduces mathematical operators acting on
DescriptorRelation objects.

To preserve composability and mathematical consistency, all
operators shall follow a unique contract.

## Decision

Every Descriptor Operator:

- accepts DescriptorRelation* as input;
- returns DescriptorRelation* as output;
- never modifies existing DescriptorRelation objects;
- preserves provenance;
- performs exactly one mathematical transformation.

Only AnalyticalStructureBuilder may construct an
AnalyticalStructure.

## Consequences

Operators become fully composable.

Behaviour Analytics becomes a mathematical transformation
pipeline rather than a collection of isolated algorithms.

