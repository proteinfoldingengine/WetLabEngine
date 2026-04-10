# UQCF-GEM Coherence-First Fractal Path Generator

**A Toy Model of Emergent Geometric Order**

This repository presents a **coherence-first path generator** inspired by UQCF-GEM principles.  
Instead of minimizing Euclidean distance (the classical TSP objective), it propagates a path by maximizing **local directional coherence** under density-modulated fractal scaling.

The resulting path forms a smooth, information-bearing backbone. The primary metric is **coherence flow** — not total length.

## Core Idea
Global order emerges from local coherence retention + fractal scaling.  
The path itself encodes the information, analogous to how a protein backbone encodes structure while folding.

## Key Findings
- Coherence-first models produce significantly higher coherence flow scores than distance-only or entropy-only baselines.
- Coherence flow tends to increase with system size n (slow logarithmic growth observed).
- Ensemble iteration yields high-quality backbones quickly.
- On protein alpha-carbon coordinates, results qualitatively align with aspects of natural structure (no biological priors).
- Runtime is practical on standard hardware.

## What This Is
- A toy model of geometric organization
- A coherence-first optimization primitive
- A reproducible experimental framework

## What This Is Not
- A shortest-path TSP solver
- A biological folding engine
- A proof of a physical theory

## What is actually demonstrated

This package demonstrates that local coherence retention, directional memory, and density-modulated fractal scaling can generate structured geometric backbones from disordered point clouds.

It does not demonstrate Euclidean optimality, biological folding accuracy, or proof of a physical theory.

## Files
- uqcf_gem_peer_review.py
- requirements.txt

## Quick Start

pip install -r requirements.txt
python uqcf_gem_peer_review.py
