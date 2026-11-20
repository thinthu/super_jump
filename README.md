# Pixel Ascent: Tower of Trials 🎮

A fast-paced, neon-aesthetic 2D vertical jumping game built entirely in Python using **Pygame**. 

## 🚀 About the Game
Climb as high as you can! Bounce on platforms to ascend, collect coins for bonus points, and avoid the dangerous spiked platforms that appear as you get higher. The game gets faster the better you play.

## ✨ Features
*   **Character Selection:** Choose between three distinct characters (Demon, Popstar, or Straw Hat).
*   **Procedural Generation:** Platforms spawn dynamically, ensuring no two runs are the same, but always remain physically reachable.
*   **Dynamic Difficulty:** The scroll speed increases as your score rises, and danger blocks begin spawning after you reach 200 points.
*   **In-Game Controls:** Direct top-right UI buttons for Restart, Pause/Resume, Mute, and Quit.
*   **Synthesized Audio:** Jump, Coin, and Hit sounds are generated mathematically on the fly using Python's `array` and `math` modules—no external audio files needed for effects!
*   **Neon Aesthetic:** Smooth gradient background, particle effects, and vibrant UI.

## 🛠️ Requirements
*   Python 3.8+
*   Pygame (`pip install pygame`)

## 🎮 How to Play
1. Clone the repository or download the files.
2. Ensure you have a background music file named `bg_music.ogg` in the same folder (optional, but recommended).
3. Run the game:
   ```bash
   python super_jump.py