# Automatic Measuring of Weld Nuggets
<p align="left">
  <img width="240" height="134" src="https://user-images.githubusercontent.com/74857138/127784568-8d7de918-0336-442b-9917-42915c18f5e7.png">
  <img width="294" height="80" src="https://user-images.githubusercontent.com/74857138/127784575-92a47599-181b-48dd-95c0-86f3daa21e4a.png">
</p>

Resistance spot welding is a widely applied manufacturing process used typically in automobile production in order to weld multiple metal sheets together by using the heat generated from an electric current. As the material melts, the sheets get fused together and at this fusing point a nugget is formed which acts as a joint when it solidifies. The size of the nugget determines the quality of the welding. To measure the size the metal sheets are separated with the help of torsion testing and the image of the nugget and the metal sheet is captured using a light microscope. The nugget in the resulting image can then be measured manually using a third party graphics software. However this manual measuring costs significant amount of time and energy especially as the volume of the data increases. This paper aims to automate the measuring process using deep learning techniques which will extract the nugget from the image and measure its size.
<p align="center">
  <img width="396" height="241" src="https://user-images.githubusercontent.com/74857138/128606206-48b749a5-2a78-4c90-9246-dea0a0b14c92.png">
</p>

The images in the image folder will be processed and fed into the neural network. The predictions of the network are written into a csv file, which can be imported into the [VGG Image Annotator](https://www.robots.ox.ac.uk/~vgg/software/via/) (via.html). Through the VGG Image Annotator user can verify or adjust the predictions of the neural network and the new coordinates of the nugget are exported. The new annotations are then fed into the "Annotations" input field, through which corresponding masks are created and the neural network can be retrained with the new data. This human-in-the-loop system aims to optimize the AI system in order to produce more reliable results.

## Online User Interface
In order to visualize the prediction of the neural network an online user interface is designed. Seperate from the rest of the code, the jupyter notebook "online_UI.ipynb" can be executed and with a temporary link the software can be tested online. Example images are in the images folder.
<p align="center">
  <img width="768" height="496" src="https://user-images.githubusercontent.com/74857138/127778694-0f9b9ab2-2970-4158-848a-17fd661e02c9.png">
</p>
