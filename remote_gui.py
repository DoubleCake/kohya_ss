import gradio as gr
import os
import json
from tageditor.block_load_dataset import  LoadDatasetUI

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
        self.view_local=False
        self.localFolder=True
        
    def init_folder_path():
        pass

    def view_local_remote(self,request:gr.Request):

            if(request.client.host !="127.0.0.1"):
                #打开隐藏的上传按钮，用户可选择将图片资源进行上传，然后
                print("远程访问用户，调用远程服务器设置")
                self.localFolder = False
            else:
                print("本地访问,调用本地服务器")
                #本地选择图像
                self.localFolder=True
            print(self.localFolder)
    
            # return {componet: gr.update(visible= self.localFolder) }
    

            # return {
                #隐藏检测框
                
                
                # #本地的检测框 和 文本栏
                # self.train_data_dir_folder: gr.update(visible= self.localFolder),
                # self.train_data_dir: gr.update(visible= self.localFolder),

                # #远程检测框 和 栏
                # self.train_data_dir_upload:gr.update(visible=  not self.localFolder) ,
                # self.tran_data_remote_name : gr.update(visible=not self.localFolder),
                            
            # }


    def remote_folder(self):
        view_data_local_or_remote = gr.Button( #用来查看当前属于远程访问还是本地访问
        '请点击初始化项目图像设置路径训练路径', 
            visible=self.localFolder
        )
        view_data_local_or_remote.click(
            self.view_local_remote
        )

        return view_data_local_or_remote






def get_img_paths(folder):
    files= os.listdir(folder)
    imgs=[]
    for file in files:
        end = os.path.splitext(file)[-1]
        if end.lower() in [".jpg",".png",".jpeg"]:
            imgs.append(os.path.join(folder,file))
    
    return imgs

def refersh_gallery(dropdown):
    # print(dropdown)
    img_path =os.path.join("./dataset/remote_datasets",dropdown+"/imgs")
    imgs_folder=os.path.join(img_path,os.listdir(img_path )[0])

    imgs_gallery= get_img_paths(imgs_folder)

    return imgs_gallery

def remote_tab():
    with gr.Blocks():
        with gr.Tab("(Train Image Browser) 仅显示远程训练图集"):
            with gr.Row():
                with gr.Column():
                    pro_choices=os.listdir("./dataset/remote_datasets")
                    dropdown= gr.Dropdown(label="选择项目仓库",choices=pro_choices,value=pro_choices[0])
                    imgpath_list=refersh_gallery(dropdown.value)
                    imgs_gallery= gr.Gallery(value=imgpath_list,columns=6)
                    
                    dropdown.change(
                        refersh_gallery,
                        inputs=dropdown,
                        outputs=imgs_gallery
                    )
                with gr.Row():
                    gr.Label("在线标注功能(更新ing)")


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
                        download_files=gr.Files(value=down_files)

                        model_dp.select(change_down_files,inputs=model_dp,outputs=download_files)

                        # download_all=gr.button("全部下载")
    
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
