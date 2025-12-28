from manim import *
import numpy as np
import random
CONFIG = {
    "bg_color": "#0a0a0a",       # Deep Void
    "primary": "#00f3ff",        # Cyber Cyan
    "secondary": "#ff00aa",      # Neon Pink
    "accent": "#ffd700",         # Gold
    "glass": "#1a1a1a",          # Semi-transparent background
    "font": "Monospace"
}
def get_random_noise(size=64):
    return np.random.randint(0, 255, (size, size, 4), dtype=np.uint8)
def get_pattern_image(size=64):
    arr = np.zeros((size, size, 4), dtype=np.uint8)
    for y in range(size):
        for x in range(size):
            r, g, b = 10, 0, 30
            if y > size//2 + (np.sin(x/5)*5): 
                r, g, b = 20, 20, 40 
                if x % 4 != 0 and y % 6 != 0 and random.random() > 0.8:
                    if random.random() > 0.5:
                        r, g, b = 0, 240, 255 
                    else:
                        r, g, b = 255, 0, 170 
            dx, dy = x - size*0.8, y - size*0.2
            if dx*dx + dy*dy < 20:
                r, g, b = 255, 100, 50
            arr[y, x] = [r, g, b, 255]
    return arr
def interpolate_images(noise_arr, final_arr, alpha):
    mixed = (noise_arr[:,:,:3] * (1-alpha) + final_arr[:,:,:3] * alpha).astype(np.uint8)
    alpha_channel = np.full((noise_arr.shape[0], noise_arr.shape[1], 1), 255, dtype=np.uint8)
    return np.concatenate([mixed, alpha_channel], axis=2)
class AdvancedDiffusionViz(Scene):
    def construct(self):
        self.camera.background_color = CONFIG["bg_color"]
        prompt_text = "cyberpunk city, neon lights, 8k"
        input_panel = RoundedRectangle(width=6.5, height=1.2, corner_radius=0.2, 
                                     stroke_color=CONFIG["primary"], stroke_width=2,
                                     fill_color=CONFIG["glass"], fill_opacity=0.8).to_edge(UP, buff=1.0)
        cursor = Rectangle(width=0.05, height=0.5, color=CONFIG["primary"], fill_opacity=1)
        prompt_display = Text("", font=CONFIG["font"], font_size=24, color=WHITE).move_to(input_panel)
        label = Text("TEXT PROMPT", font=CONFIG["font"], font_size=16, color=GRAY).next_to(input_panel, UP, buff=0.15)
        self.play(FadeIn(input_panel), FadeIn(label))
        for i in range(len(prompt_text) + 1):
            txt = prompt_text[:i]
            prompt_display.become(Text(txt, font=CONFIG["font"], font_size=24, color=WHITE).move_to(input_panel))
            cursor.next_to(prompt_display, RIGHT, buff=0.05)
            self.add(prompt_display, cursor)
            self.wait(0.03) 
        self.wait(0.5)
        self.remove(cursor)
        words = prompt_text.split(", ")
        tokens = VGroup(*[
            VGroup(
                RoundedRectangle(width=1.5, height=0.6, color=CONFIG["secondary"], fill_opacity=0.3),
                Text(w, font_size=14, font=CONFIG["font"]).set_color(CONFIG["secondary"])
            ) for w in words
        ]).arrange(RIGHT, buff=0.2).move_to(input_panel)
        self.play(FadeOut(prompt_display), FadeIn(tokens))
        matrix_box = Rectangle(width=6, height=2, color=BLUE_E, fill_opacity=0.2).move_to(UP * 0.5)
        matrix_label = Text("CLIP EMBEDDINGS (Vectors)", font_size=18, color=BLUE).next_to(matrix_box, UP)
        self.play(
            input_panel.animate.set_opacity(0),
            label.animate.set_opacity(0),
            tokens.animate.move_to(matrix_box.get_center()),
            Create(matrix_box), Write(matrix_label)
        )
        vectors = VGroup()
        for t in tokens:
            nums = VGroup(*[
                DecimalNumber(random.random(), num_decimal_places=2, font_size=12, color=CONFIG["primary"])
                for _ in range(4)
            ]).arrange(DOWN, buff=0.15)
            nums.move_to(t)
            vectors.add(nums)
        self.play(Transform(tokens, vectors), run_time=1.5)
        self.wait(0.5)
        context_group = VGroup(matrix_box, matrix_label, tokens)
        self.play(context_group.animate.scale(0.4).to_corner(UL).set_opacity(0.8))
        noise_arr = get_random_noise(64)
        final_arr = get_pattern_image(64)
        image_mobj = ImageMobject(noise_arr)
        image_mobj.height = 3.5
        image_mobj.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"]) 
        image_mobj.move_to(UP * 1)
        noise_label = Text("LATENT NOISE x_T", font=CONFIG["font"], font_size=20, color=WHITE).next_to(image_mobj, UP)
        self.play(FadeIn(image_mobj), Write(noise_label))
        unet_group = VGroup()
        b1 = Square(0.5, color=CONFIG["secondary"], fill_opacity=0.5).move_to(DOWN * 1.5 + LEFT * 2)
        b2 = Square(0.5, color=CONFIG["secondary"], fill_opacity=0.5).move_to(DOWN * 2.5 + LEFT * 1)
        b3 = Square(0.5, color=CONFIG["accent"], fill_opacity=0.8).move_to(DOWN * 3)
        b4 = Square(0.5, color=CONFIG["secondary"], fill_opacity=0.5).move_to(DOWN * 2.5 + RIGHT * 1)
        b5 = Square(0.5, color=CONFIG["secondary"], fill_opacity=0.5).move_to(DOWN * 1.5 + RIGHT * 2)
        c1 = Arrow(b1.get_bottom(), b2.get_top(), buff=0, color=GRAY)
        c2 = Arrow(b2.get_bottom(), b3.get_left(), buff=0, color=GRAY)
        c3 = Arrow(b3.get_right(), b4.get_bottom(), buff=0, color=GRAY)
        c4 = Arrow(b4.get_top(), b5.get_bottom(), buff=0, color=GRAY)
        skip1 = DashedLine(b2.get_right(), b4.get_left(), color=CONFIG["secondary"], stroke_opacity=0.5)
        unet_group.add(b1, b2, b3, b4, b5, c1, c2, c3, c4, skip1)
        unet_label = Text("U-NET (Noise Predictor)", font_size=20, color=CONFIG["secondary"]).next_to(b3, DOWN)
        self.play(Create(unet_group), FadeIn(unet_label))
        attn_lines = VGroup()
        for block in [b1, b2, b4, b5]:
            l = Line(context_group.get_bottom(), block.get_top(), color=CONFIG["primary"], stroke_opacity=0.3)
            attn_lines.add(l)
        self.play(Create(attn_lines), run_time=1)
        step_counter = ValueTracker(50) 
        step_text = Text("TIMESTEP: 50", font=CONFIG["font"], font_size=24, color=CONFIG["accent"])
        step_text.move_to(image_mobj.get_right() + RIGHT * 1.5)
        step_text.add_updater(lambda m: m.become(
            Text(f"TIMESTEP: {int(step_counter.get_value())}", font=CONFIG["font"], font_size=24, color=CONFIG["accent"])
            .move_to(image_mobj.get_right() + RIGHT * 2)
        ))
        self.add(step_text)
        math_tex = MathTex(r"x_{t-1} \leftarrow x_t - \epsilon_\theta(x_t, \text{prompt})", font_size=24, color=WHITE)
        math_tex.next_to(unet_label, DOWN)
        self.play(Write(math_tex))
        total_time = 6
        frames = 60 * total_time
        for i in range(frames):
            alpha = i / frames 
            current_step = 50 - int(alpha * 50)
            step_counter.set_value(current_step)
            visual_alpha = smooth(alpha) 
            new_pixels = interpolate_images(noise_arr, final_arr, visual_alpha)
            image_mobj.pixel_array = new_pixels
            if i % 60 == 0:
                self.play(Indicate(attn_lines, color=CONFIG["primary"], scale_factor=1.1), run_time=0.2)
                self.play(Indicate(unet_group, color=WHITE, scale_factor=1.05), run_time=0.2)
            self.wait(1/60)
        self.play(
            FadeOut(unet_group), FadeOut(attn_lines), FadeOut(unet_label), 
            FadeOut(math_tex), FadeOut(step_text), FadeOut(context_group),
            noise_label.animate.become(Text("LATENT RESULT (64x64)", font_size=20, color=WHITE).next_to(image_mobj, UP))
        )
        vae_box = Rectangle(width=4, height=1.5, color=PURPLE).move_to(DOWN * 1)
        vae_txt = Text("VAE DECODER", font=CONFIG["font"], font_size=24, color=PURPLE).move_to(vae_box)
        flow_down = Arrow(image_mobj.get_bottom(), vae_box.get_top(), color=WHITE)
        self.play(Create(vae_box), Write(vae_txt), GrowArrow(flow_down))
        final_image = ImageMobject(final_arr)
        final_image.height = 6 
        final_image.move_to(ORIGIN)
        final_image.set_opacity(0)
        self.play(
            FadeOut(flow_down), FadeOut(vae_box), FadeOut(vae_txt), FadeOut(noise_label),
            image_mobj.animate.move_to(ORIGIN).scale(6/3.5), 
            run_time=1
        )
        flash_rect = SurroundingRectangle(image_mobj, color=WHITE, buff=0)
        self.play(
            FadeIn(final_image),
            FadeOut(image_mobj),
            Create(flash_rect),
            rate_func=there_and_back, run_time=0.5
        )
        self.remove(flash_rect)
        final_label = Text("GENERATED IMAGE", font=CONFIG["font"], font_size=32, weight=BOLD, color=CONFIG["primary"])
        final_label.next_to(final_image, DOWN, buff=0.5)
        scan_line = Line(final_image.get_corner(UL), final_image.get_corner(UR), color=CONFIG["secondary"])
        scan_line.width = final_image.width
        self.play(
            Write(final_label),
            scan_line.animate.move_to(final_image.get_bottom()),
            run_time=1.5
        )
        self.play(FadeOut(scan_line))
        
        self.wait(3)
if __name__ == "__main__":
    config.pixel_width = 1080
    config.pixel_height = 1920
    config.frame_rate = 60
    config.background_color = CONFIG["bg_color"]
    
    scene = AdvancedDiffusionViz()
    scene.render()
