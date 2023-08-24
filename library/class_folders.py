import gradio as gr
from .common_gui import remove_doublequote, get_folder_path,get_folder_path_remote

    

class Folders:
    # 根据用户的ip地址，决定展示的box是上传文件box 还是本地运行的文件夹box
    
    def __init__(self, headless=False):
        self.headless = headless

        with gr.Row():

            self.train_data_dir = gr.Textbox(
                label='Image folder',
                placeholder='Folder where the training folders containing the images are located',
            )

            self.train_data_dir_folder = gr.Button(
                '📂', elem_id='open_folder_small', 
            )
            

            self.train_data_dir_folder.click(
                get_folder_path,
                outputs=self.train_data_dir,
                show_progress=False,
            )

            self.reg_data_dir = gr.Textbox(
                label='Regularisation folder',
                placeholder='(Optional) Folder where where the regularization folders containing the images are located',
            )

            self.reg_data_dir_folder = gr.Button(
                '📂', elem_id='open_folder_small', visible=(not self.headless)
            )


            self.reg_data_dir_folder.click(
                get_folder_path,
                outputs=self.reg_data_dir,
                show_progress=False,
            )
        with gr.Row():
            self.output_dir = gr.Textbox(
                label='Output folder',
                placeholder='Folder to output trained model',
            )
            self.output_dir_folder = gr.Button(
                '📂', elem_id='open_folder_small', visible=(not self.headless)
            )
            self.output_dir_folder.click(
                get_folder_path,
                outputs=self.output_dir,
                show_progress=False,
            )
            self.logging_dir = gr.Textbox(
                label='Logging folder',
                placeholder='Optional: enable logging and output TensorBoard log to this folder',
            )
            self.logging_dir_folder = gr.Button(
                '📂', elem_id='open_folder_small', visible=(not self.headless)
            )
            self.logging_dir_folder.click(
                get_folder_path,
                outputs=self.logging_dir,
                show_progress=False,
            )
    
        with gr.Row():
            self.output_name = gr.Textbox(
                label='Model output name',
                placeholder='(Name of the model to output)',
                value='last',
                interactive=True,
            )
            self.training_comment = gr.Textbox(
                label='Training comment',
                placeholder='(Optional) Add training comment to be included in metadata',
                interactive=True,
            )
        self.train_data_dir.blur(
            remove_doublequote,
            inputs=[self.train_data_dir],
            outputs=[self.train_data_dir],
        )
        self.reg_data_dir.blur(
            remove_doublequote,
            inputs=[self.reg_data_dir],
            outputs=[self.reg_data_dir],
        )
        self.output_dir.blur(
            remove_doublequote,
            inputs=[self.output_dir],
            outputs=[self.output_dir],
        )
        self.logging_dir.blur(
            remove_doublequote,
            inputs=[self.logging_dir],
            outputs=[self.logging_dir],
        )

    # def view_local_remote(self,request:gr.Request):

        # if(request.client.host !="127.0.0.1"):
        #     #打开隐藏的上传按钮，用户可选择将图片资源进行上传，然后
        #     print("远程访问用户，调用远程服务器设置")
        #     self.localFolder = False
        # else:
        #     print("本地访问,调用本地服务器")
        #     #本地选择图像
        #     self.localFolder=True

        # return {
        #     #隐藏检测框
        #     self.view_data_local_or_remote: gr.update(visible= False) ,
            
        #     #本地的检测框 和 文本栏
        #     self.train_data_dir_folder: gr.update(visible= self.localFolder),
        #     self.train_data_dir: gr.update(visible= self.localFolder),

        #     #远程检测框 和 栏
        #     self.train_data_dir_upload:gr.update(visible=  not self.localFolder) ,
        #     self.tran_data_remote_name : gr.update(visible=not self.localFolder),
                        
        # }