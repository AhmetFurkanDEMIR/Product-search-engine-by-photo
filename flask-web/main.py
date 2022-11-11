
from flask import Flask,render_template, session, redirect, url_for, request
import os
from werkzeug.utils import secure_filename
import psycopg2

import torch
import torchvision.transforms as T
import os
from PIL import Image
from torch import nn
import torch
from torch.utils.data import Dataset
from tqdm import tqdm
import numpy as np
from sklearn.neighbors import NearestNeighbors
from matplotlib import pyplot as plt
import cv2

global pathh
pathh = "/home/demir/Desktop/Hepsiburada/ai/images/"

class ConvEncoder(nn.Module):
    """
    A simple Convolutional Encoder Model
    """

    def __init__(self):
        super().__init__()

        self.conv1 = nn.Conv2d(3, 16, (3, 3), padding=(1, 1))
        self.relu1 = nn.ReLU(inplace=True)
        self.maxpool1 = nn.MaxPool2d((2, 2))

        self.conv2 = nn.Conv2d(16, 32, (3, 3), padding=(1, 1))
        self.relu2 = nn.ReLU(inplace=True)
        self.maxpool2 = nn.MaxPool2d((2, 2))

        self.conv3 = nn.Conv2d(32, 64, (3, 3), padding=(1, 1))
        self.relu3 = nn.ReLU(inplace=True)
        self.maxpool3 = nn.MaxPool2d((2, 2))

        self.conv4 = nn.Conv2d(64, 128, (3, 3), padding=(1, 1))
        self.relu4 = nn.ReLU(inplace=True)
        self.maxpool4 = nn.MaxPool2d((2, 2))

        self.conv5 = nn.Conv2d(128, 256, (3, 3), padding=(1, 1))
        self.relu5 = nn.ReLU(inplace=True)
        self.maxpool5 = nn.MaxPool2d((2, 2))
        
        self.conv6 = nn.Conv2d(256, 512, (3, 3), padding=(1, 1))
        self.relu6 = nn.ReLU(inplace=True)
        self.maxpool6 = nn.MaxPool2d((2, 2))
        
        self.conv7 = nn.Conv2d(512, 1024, (3, 3), padding=(1, 1))
        self.relu7 = nn.ReLU(inplace=True)
        self.maxpool7 = nn.MaxPool2d((2, 2))
        
        self.conv8 = nn.Conv2d(1024, 1024, (3, 3), padding=(1, 1))
        self.relu8 = nn.ReLU(inplace=True)
        self.maxpool8 = nn.MaxPool2d((2, 2))

    def forward(self, x):
        # Downscale the image with conv maxpool etc.
        x = self.conv1(x)
        x = self.relu1(x)
        x = self.maxpool1(x)

        x = self.conv2(x)
        x = self.relu2(x)
        x = self.maxpool2(x)

        x = self.conv3(x)
        x = self.relu3(x)
        x = self.maxpool3(x)

        x = self.conv4(x)
        x = self.relu4(x)
        x = self.maxpool4(x)

        x = self.conv5(x)
        x = self.relu5(x)
        x = self.maxpool5(x)
        
        x = self.conv6(x)
        x = self.relu6(x)
        x = self.maxpool6(x)
        
        x = self.conv7(x)
        x = self.relu7(x)
        x = self.maxpool7(x)
        
        x = self.conv8(x)
        x = self.relu8(x)
        x = self.maxpool8(x)
        
        return x



device = "cpu"  # GPU device
encoder = ConvEncoder()
# Shift models to GPU
encoder.to(device)

encoder.load_state_dict(torch.load("/home/demir/Desktop/BitirmeProjesi/modelAI/old/encoder_model.pt",map_location=torch.device('cpu')))
encoder.eval()

def compute_similar_images(image, num_images, embedding, device):
    """
    Given an image and number of similar images to search.
    Returns the num_images closest neares images.
    Args:
    image: Image whose similar images are to be found.
    num_images: Number of similar images to find.
    embedding : A (num_images, embedding_dim) Embedding of images learnt from auto-encoder.
    device : "cuda" or "cpu" device.
    """
    
    image = Image.open(image).convert("RGB")
    image = image.resize((768, 768))
    
    image_tensor = T.ToTensor()(image)
    image_tensor = image_tensor.unsqueeze(0)
    
    with torch.no_grad():
        image_embedding = encoder(image_tensor).cpu().detach().numpy()
        
    flattened_embedding = image_embedding.reshape((image_embedding.shape[0], -1))

    knn = NearestNeighbors(n_neighbors=num_images, metric="cosine")
    knn.fit(embedding)

    a, indices = knn.kneighbors(flattened_embedding)
    indices_list = indices.tolist()
    return indices_list

device="cpu"
flattened_embedding = np.load("/home/demir/Desktop/BitirmeProjesi/modelAI/old/data_embedding.npy")


conn = psycopg2.connect(
    host="localhost",
    database="DB_Hepsiburada",
    port="5432",
    user="postgres",
    password="123456789Zz.")


cursor = conn.cursor()

app = Flask(__name__) 
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_PATH'] = 'static/uploads'

@app.route("/",methods = ["GET","POST"])
def main():

    return render_template("/index.html")

@app.route("/imageSearch",methods = ["GET","POST"])
def imageSearch():

    if request.method == "POST":

        file = request.files['imgg']
        fileName = secure_filename(file.filename)

        file.save(os.path.join(app.config['UPLOAD_PATH'], "{}.png".format("aaa")))
        imgList = compute_similar_images(os.path.join(app.config['UPLOAD_PATH'], "{}.png".format("aaa")),10,flattened_embedding, device)

        imgListFinal = []

        for i in imgList[0]:

            imgListFinal.append(os.listdir(pathh)[i-1].split(".png")[0])

        print(imgListFinal)

        imagessList = []
        pr_id = []

        for img in imgListFinal:

            cursor.execute(
                    'SELECT pr_id, img_url FROM TBL_ImageUrl WHERE img_id=%s', (img,))
            image = cursor.fetchall()

            flag = None

            for j in pr_id:

                if str(j)==str(image[0][0]):
                    
                    flag = False
                    break

            if flag==None:

                pr_id.append(image[0][0])
                imagessList.append([image[0][0], image[0][1]])

        if len(imagessList)!=0:

            for counter, i in enumerate(imagessList):


                cursor.execute(
                        'SELECT pr_name, pr_url from tbl_product WHERE pr_id=%s', (i[0],))
                prod = cursor.fetchall()

                imagessList[counter].append([prod[0][0], prod[0][1]])

  
        imgP = os.path.join(app.config['UPLOAD_PATH'], "{}.png".format("aaa"))
  
        print(imgP)
        imagessList.insert(0,[-99, str(imgP), ["Aranan Ürün", "#", -99]])

        return render_template("/view.html", imgList = imagessList)
    else:

        return render_template("/index.html")


if __name__ == "__main__": 
	app.run(host='0.0.0.0', port=5600, debug=True)
