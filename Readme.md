# 🧠 AI Diffusion Visualization (Manim)

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Manim](https://img.shields.io/badge/Manim-Community-green?style=for-the-badge&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-purple?style=for-the-badge)

> A "First Principles" visualization of how Stable Diffusion generates images from noise, built with Python and Manim.

## 🎥 Preview

![Diffusion Process Demo](https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExMjJ4Ynd4Ynd4Ynd4/placeholder.gif)

## 🚀 Overview

This project deconstructs the **Stable Diffusion pipeline** into a visual, mathematical animation. It was designed to explain complex Generative AI concepts in a vertical video format (9:16) for social media education.

**Visualized Concepts:**
* **CLIP Encoding:** Tokenizing text prompts into vector embeddings.
* **Latent Space:** Initializing Gaussian noise tensors ($x_T$).
* **U-Net Architecture:** Visualizing the neural network structure and skip connections.
* **Reverse Diffusion:** The iterative denoising process ($x_t \rightarrow x_{t-1}$).
* **VAE Decoding:** Upscaling the latent representation to pixel space.

## 🛠️ Installation

1. **Clone the repo**
    ```bash
    git clone [https://github.com/manjusg/diffusion-viz.git](https://github.com/manjusg/diffusion-viz.git)
    cd diffusion-viz
    ```

2. **Install Dependencies**
    You will need [Manim Community](https://www.manim.community/) and NumPy.
    ```bash
    pip install manim numpy
    ```
    *(Note: Ensure you have FFmpeg and LaTeX installed on your system).*

## 🎬 Usage

Run the following command to render the video in high quality (60FPS):

```bash
manim -pqh main.py AdvancedDiffusionViz

Flags:

-p: Preview the file after rendering.

-qh: Render in High Quality (1080p).

-ql: Render in Low Quality (480p) - Use for quick testing.

📂 Project Structure
Plaintext

├── main.py            # The core animation logic
├── assets/            # (Optional) Custom textures
└── README.md          # Documentation
🤝 Connect
I post daily breakdowns of AI & Tech concepts.

Instagram: @manju.s.g_

Twitter: @manju_sg_

LinkedIn: Manjunath G

Built with 💙 by Manju.
