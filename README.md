# 🖱️ Motion Data Generator

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows)
![Status](https://img.shields.io/badge/status-Development-yellow)

A Python module that generates **realistic, human-like mouse movement and interaction traces**. Built with techniques such as **Bezier curve pathing**, **dynamic timing patterns**, and **micro-corrections**.

> ⚠️ **Ethical & Legal Notice:** This repository is provided **only** for authorized, legitimate, and ethical purposes (UI/UX testing, accessibility research, academic study, and controlled defensive research). **Do not** use this code to attack, evade, or interfere with third-party services. Attempting to use it to bypass anti-bot protections or perform unauthorized testing may violate terms of service and applicable law.

---

## 📌 Purpose

This library demonstrates techniques for synthesizing human-like pointer motion traces for **legitimate** scenarios:

- Creating realistic pointer data for automated UI/UX tests  
- Simulating pointer control for accessibility research  
- Teaching motion modelling and behavior detection  
- Defensive research and experiments in authorized environments

It is **not** a bypass tool and should never be used to evade bot protection or challenge-response systems without explicit permission.

---

## 🚀 Features

- 🎯 Bezier curve-based path generation  
- ⌛ Realistic movement timing, hesitation, and delays  
- 🖱️ Click simulation: single, double, and hold  
- 🌐 Fake browser/system context generation  
- 🌀 Micro-corrections and jitter noise  
- ⚙️ Adjustable motion parameters (speed, randomness, hesitation)

---

## ⚠️ Limitations & Responsible Use

- ❌ **Not a CAPTCHA bypass** tool — this module alone does not and cannot break hCaptcha or similar services.
- ✅ Use for educational, simulation, and internal testing purposes only.
- 📜 You must **not** use this against third-party services without prior, written authorization.
- 🛡️ Always follow responsible disclosure and ethical research practices.

---

## 📦 Installation

**Requirements**

- Python 3.8+  
- [`numpy`](https://pypi.org/project/numpy/)  
- [`bezier`](https://pypi.org/project/bezier/)

**Install with pip:**

```bash
pip install numpy bezier
```

---

## 🧪 Quickstart (Local Use Only)

```python
from motion import MotionDataGenerator
import json

generator = MotionDataGenerator()
captcha_box = {"x": 100, "y": 200, "width": 400, "height": 300}

motion = generator._Final(captcha_box, challenge_images=[], selected_images=[])

with open("result.json", "w") as f:
    json.dump(motion, f, indent=2)

```
