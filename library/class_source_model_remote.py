import gradio as gr
from .common_gui import (
    get_any_file_path,
    get_folder_path,
    set_pretrained_model_name_or_path_input,
)
import os

folder_symbol = '\U0001f4c2'  # 📂
refresh_symbol = '\U0001f504'  # 🔄
save_style_symbol = '\U0001f4be'  # 💾
document_symbol = '\U0001F4C4'   # 📄


class SourceModelRemote:
    def __init__(
        self,
        save_model_as_choices=[
            'same as source model',
            'ckpt',
            'diffusers',
            'diffusers_safetensors',
            'safetensors',
        ],
        headless=False,
    ):
        self.headless = headless
        self.save_model_as_choices = save_model_as_choices
   
        with gr.Row():
            self.model_list = gr.Dropdown(
                label='Model Quick Pick',
                choices=[
                    'custom',
                    # 'stabilityai/stable-diffusion-xl-base-0.9',
                    # 'stabilityai/stable-diffusion-xl-refiner-0.9',
                    'stabilityai/stable-diffusion-2-1-base/blob/main/v2-1_512-ema-pruned',
                    'stabilityai/stable-diffusion-2-1-base',
                    'stabilityai/stable-diffusion-2-base',
                    'stabilityai/stable-diffusion-2-1/blob/main/v2-1_768-ema-pruned',
                    'stabilityai/stable-diffusion-2-1',
                    'stabilityai/stable-diffusion-2',
                    'runwayml/stable-diffusion-v1-5',
                    'CompVis/stable-diffusion-v1-4',
                ],
                value='runwayml/stable-diffusion-v1-5',
            )
            self.save_model_as = gr.Dropdown(
                label='Save trained model as',
                choices=save_model_as_choices,
                value='safetensors',
            )
        with gr.Row():
            self.pretrained_model_name_or_path = gr.Dropdown(
                label='Pretrained model name or path',
                choices= os.listdir("./sd-models"),
                value= None
            )

        with gr.Row():
            self.v2 = gr.Checkbox(label='v2', value=False, visible=False)
            self.v_parameterization = gr.Checkbox(
                label='v_parameterization', value=False, visible=False
            )
            self.sdxl_checkbox = gr.Checkbox(
                label='SDXL Model', value=False, visible=False
            )

        self.model_list.change(
            set_pretrained_model_name_or_path_input,
            inputs=[
                self.model_list,
                self.pretrained_model_name_or_path,

                self.v2,
                self.v_parameterization,
                self.sdxl_checkbox,
            ],
            outputs=[
                self.model_list,
                self.pretrained_model_name_or_path,

                self.v2,
                self.v_parameterization,
                self.sdxl_checkbox,
            ],
            show_progress=False,
        )
