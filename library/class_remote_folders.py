import gradio as gr
from .common_gui import remove_doublequote

import time
import shared
import os,shutil

def reg_data_upload_remote(train_data_dir,reg_data_dir,reg_data_upload_folder):
    if reg_data_dir!="":#不为空，检查一下格式是否正确
        try:
            num,imgs_name= reg_data_dir.split("_")   
        except Exception:
            raise gr.Error("reg Folder Format is wrong ")
        
    proname,_= train_data_dir.split("_")  
    tmp_reg = os.path.join(shared.dataset_dir,f"{proname}/reg")
    for file in reg_data_upload_folder:
        name= os.path.split(file)[-1]
        shutil.move(file.name,os.path.join(tmp_reg,name))

class RemoteFolders:
    # 根据用户的ip地址，决定展示的box是上传文件box 还是本地运行的文件夹box
    
    def __init__(self, headless=False):
        self.headless = headless
        self.tmp_file_names=[]
        self.pre_pro_name=""
        self.localFolder=False
        self.viw_local=True


    def remoteFolderUI(self):
        with gr.Row():
            self.train_data_dir = gr.Textbox(
                label='train data name',
                placeholder='folder Name (ep:10_sks)',
            )
            self.train_data_dir_upload=gr.UploadButton(
                '📂', elem_id='open_folder_small',file_count='directory'
            )

            self.train_data_dir_upload.upload (
                self.get_folder_path_remote,
                self.train_data_dir_upload,
                # self.train_data_dir_upload,
                show_progress=True,

            )
            

            self.reg_data = gr.Textbox(
                label='Regularisation folder',
                placeholder='(Optional) Show where the regularization folders containing the images',
                interactive=False,
            )
            
            self.reg_data_upload_folder=gr.UploadButton(
                '📂', elem_id='open_folder_small',file_count='directory'
            )
            self.reg_data_upload_folder.upload (
                reg_data_upload_remote,
                inputs=[self.train_data_dir,self.reg_data,self.reg_data_upload_folder],
                show_progress=True,

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
               
        self.train_data_dir.blur(
            self.rename_train_folder,
            inputs=[self.train_data_dir],
            outputs=[self.train_data_dir_upload],
        )

        # self.reg_data_dir.blur(
        #     self.rename_reg_folder,
        #     inputs=[self.train_data_dir],
        #     outputs=[self.train_data_dir_upload],
        # )
        self.logging_dir=""
        # self.logging_dir.blur(
        #     remove_doublequote,
        #     inputs=[self.logging_dir],
        #     outputs=[self.logging_dir],
        # )


    

    def get_folder_path_remote(self,files): 
        print(f"local folder:{os.path.abspath ('.')}")
        remote_dtpath="./dataset/remote_datasets"
        #每次上传，都会检测当前文件夹内的名字，如果
        tmpFolder="tmptraindata"
        folders = os.listdir(remote_dtpath) 
        endnum=0
        for folder in folders:
            if tmpFolder in folder:
                endnum+=1

        tmpFolder= os.path.join(remote_dtpath,f"tmptraindata{endnum:0>4}")
        if(endnum !=0 ):
            #检测前一个临时文件夹是否为空，如果为空，就使用该文件夹，不为空则序号加+
            if len(os.listdir( os.path.join(remote_dtpath,f"tmptraindata{endnum-1:0>4}")))==0:

                tmpFolder=os.path.join(remote_dtpath,f"tmptraindata{endnum-1:0>4}")

        self.pre_pro_name=os.path.split(tmpFolder)[-1]
        if not os.path.exists(tmpFolder):
            #在文件夹中创建 imgs/models/loggings 文件夹
            imgs_path=os.path.join(tmpFolder,"imgs")
            os.makedirs(imgs_path)
            os.makedirs(os.path.join(tmpFolder,"models"))
            os.makedirs(os.path.join(tmpFolder,"loggings"))       

        for file in files:
            im_name= os.path.split(file.name)[-1]
            new_path=os.path.join(imgs_path,im_name)
            self.tmp_file_names.append(new_path)
            shutil.move(file.name,new_path)



    def rename_train_folder(self,train_data_dir):
        new_files=[]
        try:
            pro_name,num,imgs_name= train_data_dir.split("_")   
        except Exception:
            raise gr.Error("project Format is wron ")   
            
        if num.isnumeric():
            # old_dir=os.path.join("./dataset/remote_datasets",self.pre_pro_name)
            new_dir=os.path.join(shared.dataset_dir,pro_name)

            if os.path.exists(new_dir):
                raise gr.Warning("There is the same name train data name!\
                                 the new Images will not append")
            else: 
                os.mkdir(new_dir)
                imgs_dir= os.path.join(new_dir,f"imgs/{num}_{imgs_name}")
                models_dir= os.path.join(new_dir,"models")
                logging_dir = os.path.join(new_dir,"logs")

                os.makedirs(imgs_dir)
                os.makedirs(models_dir)
                os.makedirs(logging_dir)

            #move tmp folder img to new file
                for file in self.tmp_file_names:
                    name=os.path.split(file)[-1]
                    shutil.move(file, os.path.join(imgs_dir,name))
                    new_files.append(os.path.join(imgs_dir,name))

                self.tmp_file_names=new_files

            return train_data_dir
        else:
            return " "
        
    def rename_reg_folder(self,reg_data_dir):
        new_files=[]
        try:
            num,imgs_name= reg_data_dir.split("_")   
        except Exception:
            raise gr.Error("project Format is wron ")   
            
        if num.isnumeric():
            # old_dir=os.path.join("./dataset/remote_datasets",self.pre_pro_name)
            new_dir=os.path.join(shared.dataset_dir,pro_name)

            if os.path.exists(new_dir):
                raise gr.Warning("There is the same name train data name!\
                                 the new Images will not append")
            else: 
                os.mkdir(new_dir)
                imgs_dir= os.path.join(new_dir,f"imgs/{num}_{imgs_name}")
                models_dir= os.path.join(new_dir,"models")
                logging_dir = os.path.join(new_dir,"logs")

                os.makedirs(imgs_dir)
                os.makedirs(models_dir)
                os.makedirs(logging_dir)

            #move tmp folder img to new file
                for file in self.tmp_file_names:
                    name=os.path.split(file)[-1]
                    shutil.move(file, os.path.join(imgs_dir,name))
                    new_files.append(os.path.join(imgs_dir,name))

                self.tmp_file_names=new_files

            return train_data_dir
        else:
            return " "
        
