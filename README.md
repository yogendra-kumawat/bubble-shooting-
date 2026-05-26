# 🫧 Bubble Pop — Finger Detection Game

<div align="center">

**A real-time hand-tracking game built with pure OpenCV + MediaPipe — no mouse, no keyboard, just your finger!**

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)]()
[![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)]()
[![MediaPipe](https://img.shields.io/badge/MediaPipe-FF6D00?style=for-the-badge)]()
[![Pygame](https://img.shields.io/badge/Pygame-Audio-green?style=for-the-badge)]()

</div>

---

## 🎮 What Is This?

Bubbles fall from the top of the screen. Point your **index finger** at a bubble to pop it — your webcam sees your hand in real time using MediaPipe, and your fingertip is the cursor. Miss a bubble and you lose a life. Pop as many as you can before you run out!

```
┌─────────────────────────────────────┐
│  SCORE=12     LIVES=4     START     │  ← HUD bar
│                                     │
│        🫧          🫧               │
│   🫧                    🫧          │  ← Bubbles falling
│                                     │
│           ☝️  (your finger)         │  ← Tracked fingertip
│                                     │
└─────────────────────────────────────┘
```

---

## ✨ Features

- 🖐️ **No controller needed** — index fingertip tracked live via MediaPipe
- 🫧 **4 bubbles** falling simultaneously at random X positions
- 💥 **Pop sound** plays on every successful hit (`Pop Bubble Sound Effect 2022.mp3`)
- 🎵 **Background music** loops throughout (`Plants vs Zombies Soundtrack.mp3`)
- ❤️ **5 lives** — miss a bubble = lose a life
- 🏆 **Score counter** — increments on every pop
- ⚡ **Speed increases** progressively at score 100, 200, and 300
- 🖥️ **START button** — tap with your finger to begin (or restart)
- 🎨 **Pure OpenCV rendering** — no game engine, just `cv2` drawing calls

---

## 🕹️ How to Play

1. Run the script — the game window opens with a splash screen
2. **Point your index finger at the START button** (top-right of screen) to begin
3. **Bubbles fall from the top** — touch them with your fingertip to pop them
4. **Miss a bubble** (it reaches the bottom) = **−1 life**
5. **Game over** when all 5 lives are gone — point at START to restart

### Controls Summary

| Action | How |
|--------|-----|
| Start / Restart | Point index finger at **START** button (top-right) |
| Pop a bubble | Move index fingertip **onto the bubble** |
| Quit | Close the window |

---

## ⚙️ How It Works

### Full Pipeline Per Frame

```
Webcam frame
     │
     ▼
cv2.flip(f, 1)                    ← Mirror so left=left (natural)
     │
     ▼
Build game canvas (600×600 white) ← Draw 4 bubbles at current Y positions
     │
     ▼
cv2.bitwise_and(frame, canvas)    ← Blend webcam + bubble images
     │
     ▼
MediaPipe Hands.process()         ← Detect hand landmarks
     │
     ▼
Extract landmark[8] (x8, y8)     ← Index fingertip position
     │
     ├──► Collision check (finger inside bubble?) → pop + score + sound
     │
     ├──► Finger on START button? → reset game
     │
     ▼
Draw HUD (score, lives, START)
     │
     ▼
Advance bubble Y positions        ← co_1 += 7 (or faster at high score)
     │
     ▼
If bubble Y ≥ 485 → reset to top, lose a life (if game active)
     │
     ▼
cv2.imshow("fg", frame)
```

### Bubble Rendering

Bubbles are real images (`download.jpeg` = blue bubble, `OIP.jpeg` = rainbow bubble), resized to 100×100 and **blended with the webcam feed** using `cv2.bitwise_and` — so the bubbles appear to float over the live camera picture.

```python
imp = np.ones((600, 600, 3), dtype=np.uint8) * 255  # white canvas
imp[x1:y1, xx1:yy1] = bubble1   # place bubble 1 at its current position
# ... repeat for bubbles 2, 3, 4

f = cv2.bitwise_and(f, imp)      # white areas let webcam through,
                                  # black areas block it — bubbles show up
```

### Fingertip Tracking

MediaPipe provides 21 hand landmarks. Landmark **#8** is the **index fingertip**:

```python
x8 = int(l.landmark[8].x * w)   # normalised → pixel X
y8 = int(l.landmark[8].y * h)   # normalised → pixel Y
```

A green dot is drawn at `(x8, y8)` so the player can see exactly where their fingertip is.

### Collision Detection

A bubble occupies a 100×100 box. The hit check is a simple bounding-box test:

```python
if axis1-50 < x8 < axis1+50 and co_1 < y8 < co_1+100:
    co_1 = 0              # reset bubble to top
    s2.play()             # pop sound
    score += 1
    axis1 = np.random.randint(50, 450)  # new random X position
```

### Speed Progression

Bubbles fall 7 pixels per frame by default. As score climbs, extra pixels are added each frame:

| Score | Base speed | Bonus | Total fall/frame |
|-------|-----------|-------|-----------------|
| 0–99 | 7 px | +0 | **7 px/frame** |
| 100–199 | 7 px | +7 | **14 px/frame** |
| 200–299 | 7 px | +9 | **16 px/frame** |
| 300+ | 7 px | +11 | **18 px/frame** |

> The last 15 pixels before the bottom (`co > 470`) slow to +1 px/frame so the bubble lingers briefly — giving the player one last chance to pop it.

### Audio

| Sound | File | Trigger |
|-------|------|---------|
| Background music | `Plants vs Zombies Soundtrack. .mp3` | Loops from first frame (`s1.play(-1)`) |
| Pop effect | `Pop Bubble Sound Effect 2022.mp3` | Every successful bubble pop |

---

## 📁 Project Structure

```
bubble-pop/
├── run.py                           # Main game script
├── download.jpeg                    # Blue bubble image (100×100)
├── OIP.jpeg                         # Rainbow bubble image (100×100)
├── Pop Bubble Sound Effect 2022.mp3 # Pop SFX
├── Plants vs Zombies Soundtrack. .mp3  # Background music
└── README.md
```

---

## 🚀 Setup & Installation

### Requirements

- Python 3.x
- Webcam

### Install Dependencies

```bash
pip install opencv-python mediapipe pygame numpy
```

### Run

```bash
python run.py
```

Stand back so your full hand is visible in the webcam frame. Point your index finger at **START** to begin!

---
