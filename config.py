"""Configuration settings for Timeloop Bus."""

import os

SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
SCALE = 3

MINUTES_PER_ACTION = 1
MAX_MINUTES = 10

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:7b")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
PREFERRED_LLM = os.environ.get("PREFERRED_LLM", "ollama")

DEBUG_MODE = True
LOG_PROMPTS = True

ENABLE_SOUND = True

COLORS = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "gray": (128, 128, 128),
    "dark_gray": (64, 64, 64),
    "light_gray": (192, 192, 192),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "bus_floor": (80, 60, 40),
    "bus_seat": (100, 80, 60),
    "window": (30, 30, 50),
    "driver": (40, 40, 40),
    "passenger_1": (200, 100, 100),
    "passenger_2": (100, 200, 100),
    "passenger_3": (100, 100, 200),
    "passenger_4": (200, 200, 100),
    "ui_bg": (20, 20, 30),
    "ui_text": (200, 200, 200),
    "ui_accent": (255, 200, 100),
}
