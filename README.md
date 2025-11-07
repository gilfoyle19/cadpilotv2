# CADPilot

CADPilot is an AI-Agent that transforms natural language descriptions into precise parametric 3D extrusion based models using Large Language Models and CadQuery.

## Overview

The goal of this project is to create a powerful yet simple CAD gen AI agent without using any agentic libraries such as LangChain, CrewAI etc.

CADPilot enables engineers and designers to generate complex 3D models using natural language. Simply describe your part, and the system will:

1. Parse your description into a structured specification.
2. Generate parametric CadQuery code.
3. Validate and refine the model.
4. Export to industry-standard formats.

## Features

### Core Capabilities
- **Natural Language Processing**: Convert English descriptions to JSON specs
- **Parametric Modeling**: Generate CadQuery Python code
- **Real-time Validation**: Ensure model quality
- **Interactive Visualization**: 3D preview with PyVista
- **Multiple Export Formats**: STEP and STL support

### Supported Operations
- Basic solids (box, cylinder, sphere)
- Complex sketches (splines, arcs)
- Boolean operations (union, cut)
- Features (fillets, chamfers)
- Pattern-based operations
- Multi-workplane modeling