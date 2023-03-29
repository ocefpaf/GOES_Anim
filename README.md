# Create GOES animations with observations/instruments overlay

This animation is created using two notebooks:

- 00-Download-GOES-Images.ipynb: downloads the GOES-16 images from S3. One can define the follow in the notebook.
  - Path to save the images
  - Bounding box (bbox)
  - Time span
  - GOES version, domain and product time

  The notebook will save smaller subset netCDF files with just the bbox and the NaturalColor or TrueColor data.
  Once can remove the original netCDF files to save space or modify the loop to remove them when the subset is saved.


- 01-Hurricane-Fiona.ipynb: reads the saved Natural/TrueColor images, the argo, glider, and saildrone data, and saves PNGs for each time step with the data layers.

One can add extra data layers to the images. The animations are later rendered with ffmpeg. Change the Frames Per Second (FPS) variable for a slower (5) or faster (30) animation.

Ffmpeg is called twice later on to crop the extra white space.

The PNGs, uncropped, and final cropped video is kept on the disk. Clean them up if you want to run the notebook  again.


![](NaturalColor_fps15_cropped_10_min.gif)
