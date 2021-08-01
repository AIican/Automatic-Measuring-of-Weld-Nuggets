# Masterarbeit: Automatic Measuring of Weld Nuggets

Resistance spot welding is a widely applied manufacturing process used typically in automobile production in order to weld multiple metal sheets together by using the heat generated from an electric current. As the material melts, the sheets get fused together and at this fusing point a nugget is formed which acts as a joint when it solidifies. The size of the nugget determines the quality of the welding. To measure the size the metal sheets are separated with the help of torsion testing and the image of the nugget and the metal sheet is captured using a light microscope. The nugget in the resulting image can then be measured manually using a third party graphics software. However this manual measuring costs significant amount of time and energy especially as the volume of the data increases. This paper aims to automate the measuring process using deep learning techniques which will extract the nugget from the image and measure its size.
<p align="center">
  <img width="396" height="241" src="https://user-images.githubusercontent.com/74857138/127747452-dacf98ea-b8cc-4236-b1b5-1ce8c06e18cb.png">
</p>

The images in the image folder will be processed and fed into the neural network. The predictions of the network are written into a csv file, which can be imported into the [VGG Image Annotator](https://www.robots.ox.ac.uk/~vgg/software/via/) (via.html). Through the VGG Image Annotator user can verify or adjust the predictions of the neural network and the new coordinates of the nugget are exported. The new annotations are then fed into the "Annotations" input field and the neural network can be retrained with the new data. This human-in-the-loop system aims to optimize the AI system in order to prduce more reliable results.

## Online User Interface
balabsabvh
