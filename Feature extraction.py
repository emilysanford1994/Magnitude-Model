from PIL import Image
import numpy as np
from scipy.spatial import ConvexHull
from pathlib2 import Path
import csv
import os

#Directories
imageDirectory = '/Users/emilysanford/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Johns Hopkins/Research/Test Re-Test/Submission 2/Github materials/Stimuli/' # Change this to the path where the images are saved
fileName = "/Users/emilysanford/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Johns Hopkins/Research/Test Re-Test/Submission 2/Github materials/stimulus features.csv" # Name of file where feature information will be saved

# Define colors
background = (128,128,128) # gray
col1 = (255,255,0) # yellow 
col2 = (0,0,255) # blue


# Feature extraction functions

def countPix(pic):
    # Takes picture as input, converts the picture to RGB values, then counts pixels in target colors defined above
    # Also converts to matrix for convex hull algorithm (1 = group 1, 2 = group 2, 0 = background)
    pic_rgb = pic.convert('RGB')
    col1_pix = 0
    col2_pix = 0
    width, height = pic.size
    mat = np.zeros((width, height))
    for x in range(0, width):
        for y in range(0, height):
            color = pic_rgb.getpixel((x, y))
            if color[0] == col1[0] and color[1] == col1[1] and color[2] == col1[2]:
                col1_pix += 1
                mat[x,y] = 1
            elif color[0] == col2[0] and color[1] == col2[1] and color[2] == col2[2]:
                col2_pix += 1
                mat[x,y] = 2
            else:
                mat[x,y] = 0
    return(col1_pix, col2_pix, mat)            
    
def convexHull(matx):
    # Calculates convex hull around the pixels of each color
    #Color 1
    col1_obj = np.argwhere(matx == 1).tolist()
    col1_objPoints = np.asarray(col1_obj)
    col1_ch = ConvexHull(col1_objPoints)
    col1_chArea = col1_ch.volume
    #Color 2
    col2_obj = np.argwhere(matx == 2).tolist()
    col2_objPoints = np.asarray(col2_obj)
    col2_ch = ConvexHull(col2_objPoints)
    col2_chArea = col2_ch.volume
    return (col1_chArea, col2_chArea)

def imageAnalysis(pic):
    # Runs analysis code
    col1_tsa,col2_tsa, mat = countPix(pic)
    col1_ch,col2_ch = convexHull(mat)
    return (col1_tsa, col2_tsa, col1_ch, col2_ch)
    


# Set wd to image directory
os.chdir(imageDirectory)

# Collect list of image paths (strings)
images = []
pathlist = Path(imageDirectory).glob('**/*.png')
for path in pathlist:
    pathStr = str(path)
    images.append(pathStr)

# Extract features from all images in folder
rows = []
i = 1
for image in images: 
    # Get image name and numbers from image title (will have to be adjusted depending on your file structure)
    picName = image.split("/",13)[13] 
    col1_N = picName.split("_",3)[2] # yellow
    col2_N = picName.split("_",3)[3].split(".",1)[0] # blue
    print(i, picName) # Uncomment this line to be updated on how many images have been processed
    i +=1
    
    # Run analysis
    img = Image.open(image)  
    col1_tsa, col2_tsa, col1_ch, col2_ch = imageAnalysis(img)
    row = [picName] + [col1_N] +[col2_N]+ [col1_tsa] + [col2_tsa] + [col1_ch] + [col2_ch]
    rows.append(row)    
    
# Save feature data to csv
columnTitleRow = ["image"]+["col1_N"]+["col2_N"]+ ["col1_TSA"]+["col2_TSA"]+["col1_CH"]+["col2_CH"]
with open(fileName, 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(columnTitleRow)
    for i in range(0, len(rows)):
        writer.writerow(rows[i]) 
        
        
        
        
        
        