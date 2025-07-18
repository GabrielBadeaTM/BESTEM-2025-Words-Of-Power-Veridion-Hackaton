# 🧩 1. Pathfinder Grid Simulation

## 📝 Problem Overview

Given a 2D grid with walls, a start point (S), a target (T), and an empty space (E), the task is to move S to T by pushing it step by step. At each step, E must move to the next cell where S is supposed to go, allowing S to be pushed forward. There is a limit `K` on how many moves E is allowed to take in one step.

Multiple such scenarios are evaluated.

## ⚙️ Solution

This solution simulates the puzzle using BFS and DFS:

- First, it uses **BFS** to determine all shortest paths from S to T.
- Then, for each such path, it simulates how E can help push S along the path.
- For each push, we check whether E can move to the required position in ≤ K moves. If not, we simulate a "cheat" move, costing `K` time units.
- The solution calculates the total time taken for each path and returns the minimum.

Several utility functions manage grid allocation, bounds checking, and path tracing. The pathfinding logic is structured and robust, handling both accessible and blocked scenarios.

## ⚠️ Notes

- Memory is managed manually with dynamic allocation.
- The BFS used for both finding shortest paths and checking reachability.
- The code was written and tested as part of a technical screening challenge.

## 🧠 Additional Problem – Dynamic Programming Game

This second part of the challenge is a classic dynamic programming problem involving a two-player game.

# 🧊 2. Crystal - Dinamic Programing

Players Arin and Bion take turns subtracting either 2, 5, or 7 from a starting number `T`. The player who cannot make a move loses.

Given multiple values of `T`, determine whether Arin (who always starts) can win each game, assuming both players play optimally.

### 💡 Solution

I use a bottom-up dynamic programming approach:

- We compute for each `T` whether it is a winning (`true`) or losing (`false`) position.
- A position `T` is winning if there exists at least one move that puts the opponent in a losing position.
- We iterate from 0 to the target `T` and mark each accordingly based on the available moves.

The algorithm returns `"Arin"` if the starting position is a win for Arin, or `"Bion"` otherwise.

This is a simple, clean implementation of **Grundy Numbers** (or Nim-like) logic using `O(n)` time and space.
