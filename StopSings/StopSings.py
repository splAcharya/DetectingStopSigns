import BitMapProcessor as BMP
import ImageProcessor as IMP 
import numpy
import time


def main():
    startTime = time.time()
    
    path = "D:\Repo\Personal\DetectingStopSigns\StopSings\inputImages\image_15.bmp"
    pathToSave = "D:\Repo\Personal\DetectingStopSigns\StopSings\outputImages\oi_"
    header, imgAr, imgH, imgW = BMP.readBitMapImage(path)
    imgAr2 = imgAr.copy()


    imgAr = IMP.applyHistogramEqualization(imgAr) #improve appearence of the image
    imgAr = IMP.applyGaussianBlur(imgAr) #smooth the image with low pass filter
    imgAr, imgGr = IMP.detectEdges(imgAr) #apply sobel edge detection
    imgAr = IMP.applyNonMaximSupression(imgAr,imgGr) #thin edges
    imgAr = IMP.doubleThresholdingandEdgeTracking(imgAr,70,150,5)


    ##TODO: Segement images, fro instance 3 by 3 window which allows more compettion and better lines, look julstroms notes
    houghAcc = IMP.houghTransfrom(imgAr,thetaStep = 5)
    #houghAcc = IMP.houghTransfromWithImageGradient(imgAr,imgGr)
    houghPoints = IMP.detectHoughPoints(houghAcc,50,imgH,imgW)
    lineImageAr = IMP.createHoughLineImage(houghPoints,imgH,imgW)
    imgAr = IMP.drawHoughLineImage(imgAr,lineImageAr,0.5)
    imgAr2 = IMP.drawHoughLineImage(imgAr2,lineImageAr,0.5)


    #TODO: to see hough lines, maybe try plotting all the points from one point to another and adding them together using nump.eye
    BMP.writeBitMapImage(header,imgAr,"image_15",pathToSave)
    BMP.writeBitMapImage(header,imgAr2,"image_15ob",pathToSave)
    #TODO: learn about FFT and write your won FFT algorithm
    #TODO: use only one threshold(lower threshold) and track anything above the lower threshold


    endTime = time.time()
    print("Elapsed Time: %0.3f seconds"%(endTime-startTime))



if __name__ == "__main__":
    main()
