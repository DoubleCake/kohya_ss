import gradio as gr
import os
import json

def echo(name, request: gr.Request):
    print("Request headers dictionary:", request.headers)
    print("IP address:", request.client.host)
    return name

def flip_text(request: gr.Request,x):
    print("Request headers dictionary:", request.headers)
    print("IP address:", request.client.host)
    return x[::-1]

def change_down_files(select_model_folders:gr.Dropdown):
    files=[]
    for selected in select_model_folders:
        folder= f"./dataset/remote_datasets/{selected}/models"
        for file in os.listdir(folder):
            ends=os.path.splitext(file)[-1]
            if ends in [".safetensors",".ckpt"]:
                files.append(os.path.join(folder,file))

    return files

class RemoteTab():

    def __init__(self) -> None:
        self.init_folder_path
        
    def init_folder_path():
        pass
    
def remoteUI():
    with gr.Blocks():
        with gr.Tab("Flip Text"):
            text_input = gr.Textbox()
            text_output = gr.Textbox()
            text_button = gr.Button("Flip")
        text_button.click(flip_text, inputs=text_input, outputs=text_output)

        with gr.Tab("远程访问模型下载"):
            with gr.Row():
                #update local foler jsonfile
                down_files=[]
                ## 创建 路径和数据表
                dict_folder=[]
                model_path_choice=[]
                model_path_list=[]
                str = "./dataset/remote_datasets"
                dict_folder.append(f"📂remote_datasets")

                idx=1
                for root,dirs,files in os.walk(str):
                    #这套数据集下训练的有模型
                    if "models" in dirs:
                        model_path_choice.append(os.path.split(root)[-1])
                    for dir in dirs:
                        dict_folder.append(f"{'  '*idx}📂{dir}")

                    idx+=1

                gr.TextArea("\n".join(dict_folder),max_lines=20,label="Remte Folder List ",interactive=False)

                with gr.Column():
                        #已经训练好的模型
                        choices=dir
                        model_dp= gr.Dropdown(model_path_choice,multiselect=True)
                    
                        model_dp= gr.Dropdown(model_path_choice,multiselect=True)
                        download_files=gr.Files(value=down_files)

                        model_dp.select(change_down_files,inputs=model_dp,outputs=download_files)

                        download_all=gr.button("全部下载")
    
            with gr.Row():
                dirt={}



if __name__ == "__main__":

    remoteU2I = RemoteTab()
    interface = gr.Blocks(
                 title='Kohya_ss GUI', theme=gr.themes.Default(),
            )
    with interface:
        remoteUI()

    interface.launch(server_name='localhost')
