from atra.gradio_utils.ui import GLOBAL_CSS, GET_GLOBAL_HEADER, launch_args
from atra.image_utils.diffusion import generate_images
import gradio as gr


def build_diffusion_ui():
    ui = gr.Blocks(css=GLOBAL_CSS)
    with ui:
        GET_GLOBAL_HEADER()
        with gr.Row():
            with gr.Column():
                prompt = gr.Textbox(
                    label="Prompt", info="Prompt of what you want to see"
                )
                negatives = gr.Textbox(
                    label="Negative Prompt",
                    info="Prompt describing what you dont want to see, useful for refining image",
                )
                mode = gr.Dropdown(
                    choices=["prototyping", "high res"],
                    label="Mode",
                    value="prototyping",
                )
            with gr.Column():
                images = gr.Image()
                LOGS = gr.Textbox(max_lines=6)
        prompt.submit(
            generate_images,
            inputs=[prompt, negatives, mode],
            outputs=[images, LOGS],
        )
        negatives.submit(
            generate_images,
            inputs=[prompt, negatives, mode],
            outputs=[images, LOGS],
        )

        gr.Examples(
            [
                [
                    "A photo of A majestic lion jumping from a big stone at night",
                ],
                [
                    "Aerial photography of a winding river through autumn forests, with vibrant red and orange foliage",
                ],
                [
                    "interior design, open plan, kitchen and living room, modular furniture with cotton textiles, wooden floor, high ceiling, large steel windows viewing a city",
                ],
                [
                    "High nation-geographic symmetrical close-up portrait shoot in green jungle of an expressive lizard, anamorphic lens, ultra-realistic, hyper-detailed, green-core, jungle-core"
                ],
                ["photo of romantic couple walking on beach while sunset"],
                ["Glowing jellyfish floating through a foggy forest at twilight"],
                [
                    "Skeleton man going on an adventure in the foggy hills of Ireland wearing a cape"
                ],
                [
                    "Elegant lavender garnish cocktail idea, cocktail glass, realistic, sharp focus, 8k high definition"
                ],
            ],
            inputs=[prompt],
        )

    ui.queue(concurrency_count=1, api_open=False)
    ui.launch(server_port=7861, **launch_args)
