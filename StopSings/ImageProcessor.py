#Author: Swapnil Acharya
#Since: 5/16/2020

import numpy
import matplotlib.pyplot as plt
from matplotlib import rcParams


def blendTwoImages(imageArray1,imageArray2, blendFactor):
	"""This function blends two images together into one image where bith imageArray have to be of the same size
		
		Args:
			imageArray1: 2D grey scale image array for image1
			imageArray2: 2D grey scale image array for image2
			blendFactor: determine which of the two images has more influence over the final image, musbet be between 0 < blendFactor < 1

		Returns:
			2D blended image array
	"""

	print("Started Blending Two Images")

	imageHeight, imageWidth = imageArray1.shape
	blendedPixel= numpy.zeros(imageArray1.shape,float)

	for i in range(0,imageHeight):
		for j in range(0,imageWidth):
			pixel1 = blendFactor * float(imageArray1[i,j])
			pixel2 = (1-blendFactor) * float(imageArray2[i,j])
			finalPixel = int(round(pixel1+pixel2))
			
			if(finalPixel < 0):
				blendedPixel[i,j] = 0
			elif(finalPixel > 255):
				blendedPixel[i,j] = 255
			else:
				blendedPixel[i,j] = finalPixel

	print("Completed Blending Two Images")
	return blendedPixel





def adjustBrightness(imageArray, adjustmentConstant):
	""" This function adjusts the brightness of the 2D array by a contant value

	Args:
		imageArray: the 2D greyscale image array whos brightness is to be adjusted
		
		adjustmentConstant: The constant that is to be used for brightness adjustment

	Returns:
		None
	"""

	print("Starting Brightness adjustment")

	imageHeight, imageWidth = imageArray.shape

	for i in range(0,imageHeight):
		for j in range(0,imageWidth):
			tempC =  imageArray[i,j] + adjustmentConstant
			if(tempC > 255):
				imageArray[i,j] = 255
			else:
				imageArray[i,j] = tempC
	print("Brightness adjustment complete")

	return imageArray #return brightness adjusted image array
	



def adjustContrastInAllPixels(imageArray, centerConstant, factor):
	""" This function adjusts the contrast of the 2D array given a correction factor 

	Args:
		imageArray: the 2D image array whose brightness is to be adjusted

		centerContant: the offset or centervalue from and to which pixel's intesity is to be moved or pull towards

		factor: The constant that is used to adjust brightness
				increase contrast, 1.05 < factor < 1.2
				decrease constrast 0.1 < factor < 1.0

	Returns:
		None
	"""

	print("Starting contrast adjustment")

	imageHeight, imageWidth = imageArray.shape
	for i in range(0,imageHeight):
		for j in range(0,imageWidth):
			tempC = int(imageArray[i,j])
			tempD = int(factor * (tempC - centerConstant) + centerConstant)
			if(tempD < 0):
				imageArray[i,j] = 0
			elif(tempD > 255):
				imageArray[i,j] = 255
			else:
				imageArray[i,j] = tempD
	print("Contrast Adjustment complete")

	return imageArray #return contrast adjusted imageArray




def applyHistogramEqualization(imageArray):
	""" This function perfrom histogram eqalization on a 2D grey scale image array

		Instead of manupulating contrast and brightness of an image manually, Histogram equalization
		attempts to detemined the best value for both brightness and contrast. It overall improves the 
		appearence of the image. This function increases brightnes over most of the image and decreases 
		brightness over some of the image. Overall, histogram equalization improves appearance of an image.

		Args:
			imageArray:
				The 2D greyscale image array

		Returns:
			histogram euqalized 2D image array, the height and width of return array is the same as input imageArray
	"""

	print("Starting Histogram Equalization")


	imageHeight, imageWidth = imageArray.shape #get height and widhth of 2D image array

	#build histogram
	histogram = numpy.zeros([256],int) #declare a histogram container of size 256 since, a pixel's intensity in a greyscale image can go from 0-255

	for i in range(0,imageHeight):
		for j in range(0,imageWidth):
			intensity = imageArray[i,j]
			histogram[intensity] = histogram[intensity] + 1

	#plt.hist(histogram,bins=256,color='g',edgecolor='w', alpha=1)
	#plt.show()

	#build cumulative histogram
	for i in range(1,256):
		histogram[i] = histogram[i-1] + histogram[i]


	#Build normalized histogram
	histogram = histogram * (255/(imageHeight*imageWidth))

	#display histogram

	#bins = number of elements
	#color = color of histogram
	#edgecolor = 'distinguish bins
	#fig, a = plt.subplots(1,2)
	#alpha = transpancy of data, 0 < alpha < 1
	#rcParams['figure.figsize'] = 10,10 #graph size
	
	#plt.hist(histogram,bins=256,color='g',edgecolor='w',alpha=1)
	#plt.grid(axis='y',alpha=0.2)
	#plt.show()


	#apply histogram equalization
	for i in range(0,imageHeight):
		for j in range(0,imageWidth):
			intensity = imageArray[i,j]
			newIntensity = histogram[intensity]
			if(newIntensity < 0):
				imageArray[i,j] = 0
			elif(newIntensity > 255):
				imageArray[i,j] =255
			else:
				imageArray[i,j] = newIntensity

	
	print("Completed Histogram Equalization")
	return imageArray





def convolve(imageArray,kernel):
	""" This function perfrom convolution between image array and given kernel.

		Zeros padding is done around the image array based on the dimenstion of kernel
		after that convolution is perfromed.

		Args:
			imageArray: the 2D greyscale image array

			kernel: the kernel/filter/mask to apply to the 2D image array

		Returns:
			convolved imageArray, the hieght and width of the convolved array is the same as
			the input imageArray
	"""

	imageHeight, imageWidth = imageArray.shape
	kernelHeight, kernelWidth = kernel.shape

	paddedImageArray = numpy.zeros([imageHeight+((kernelHeight-1)*2), imageWidth+((kernelWidth-1)*2)],float) #pad 4 zeroes in all direction since, gaussian kernel is 5x5
	paddedImageArray[(kernelHeight-1):imageHeight+(kernelHeight-1),(kernelWidth-1):imageWidth+(kernelHeight-1)] = numpy.array(imageArray,float).copy() #insert image array in the zero array to create zero padded array
	convolvedImageArray = numpy.zeros(paddedImageArray.shape,float)

	#start convolution
	for i in range(4,paddedImageArray.shape[0]-(kernelHeight-1)):
		for j in range(4,paddedImageArray.shape[1]-(kernelWidth-1)):
			outerSum = 0
			for m in range(0,kernel.shape[0]):
					innerSum = 0
					for n in range(0,kernel.shape[1]):
						innerSum += paddedImageArray[i-m,j-n] * kernel[m,n] 
					outerSum += innerSum
			convolvedImageArray[i,j] = outerSum
		
	#remove zero padding
	convolvedImageArray = convolvedImageArray[4:imageHeight+4, 4:imageWidth+4].copy() #remove zero padding

	#return convolved array
	return convolvedImageArray





def applyGaussianBlur(imageArray):
	""" This function smooths(blurrs) an image by apply guassian blur.

		Args:
			imageArray: the 2D image array of an greyscale image

		Returns:
			blurred 2D image array whose height and width are the same as the input 2D image Array
	"""

	print("Started Applying Gaussian Blur")
	#Define Gausian Kernel
		
	#              1,  4,  6,  4, 1
	#              4, 16, 26, 16, 4
	#   1/256 *    6, 24, 36, 24, 6
	#              4, 16, 24, 16, 4
	#              1, 4,   6,  4, 1


	kernel = numpy.array([[1,  4,  6,  4, 1],
						 [4, 16, 26, 16, 4],
						 [6, 24, 36, 24, 6],
						 [4, 16, 24, 16, 4],
						 [1, 4,   6,  4, 1]],float)

	kernel = kernel / 256 #scale kernel

	
	blurredArray = convolve(imageArray.copy(),kernel.copy()) #apply blurr via convolution

	print("Completed Applying Gaussian Blur")

	return blurredArray #return blurred array




def detectEdges(imageArray):
	""" This function perfrom edge detection in an greyscale 2D imageArray

		this function applyies vertical and horizational sobel masks to image array,
		before useing this function smotthing masks such as gaussian blur is recomended

		TODO: changed vertical to primary diagonal, changed horizontal to secondary diagonal, rename them,
			  changing weight 2 to 5 gives more prominent edges

		Args:
			imageArray: the 2D grey scale image array

		Returns:
			edge edetected image array
	"""

	print("Started Edge detection")

	# sobel vertical mask
	#	-1, 0,	1
	#	-2,	0,	2
	#	-1,	0,	1
	sobelVerticalMask = numpy.array([[0,1,5],
									[-1,0,1],
									[-5,-1,0]],float)


	#sobel horizontal mask
	#	-1,	-2, -1
	#	0,	0,	0
	#	1,	2,	1
	sobelHorizontalMask = numpy.array([[-5,-1,0],
										[-1,0,1],
										[0,1,5]],float)


	#apply vertical mask to 2D image array
	verticalEdges = numpy.array(convolve(imageArray,sobelVerticalMask),float)

	#apply horizontal mask to 2D image array
	horizontalEdges = numpy.array(convolve(imageArray,sobelHorizontalMask),float)

	#get gradient magnitude
	gradientMadnitude = numpy.hypot(horizontalEdges,verticalEdges)

	#get gradient direction
	gradientDirection = numpy.arctan2(verticalEdges,horizontalEdges)

	print("completed Edge detection")

	return gradientMadnitude, gradientDirection #return imageArray and imageAray direction




def applyNonMaximSupression(imageArray,imageGradient):
	""" THis function perfrom gradient based thinning of the 2D pixel data

		THe result of this operation is reflected on the 2D array.

		Args:
			imageArray: the 2D edge detected image array

			imageGradient: the gradient of 2D edge detect image

		Returns:
			2D imageArray with edges supressed
	"""


	print("Started Thinning Edges via non maxium supression.")
		
	#convert directions from radian to degrees
	gradientDirection = imageGradient.copy()
	pixelData = imageArray.copy()

	gradientDirection = gradientDirection * (180/numpy.pi) #convert from radian to degrees

	suppressCount = 0
	negcount = 0

	imageHeight, imageWidth = pixelData.shape

	for i in range(1,imageHeight-1):
		for j in range(1,imageWidth-1):

			#get the current edge's direction
			direction = gradientDirection[i,j]
			if(direction < 0):
				negcount += 1

			#define container for pixel at opposite edges
			opEdge1 = 0 
			opEdge2 = 0

			#if gradient direction is between  either to left or right of the current pixel
			if(( 0 <= direction < 22.5 ) or (157.5 <= direction <= 180)):
				opEdge1 = pixelData[i,j+1]
				opEdge2 = pixelData[i,j-1]

			#if gradient direction is at the 45 degree angle or 225 degree angle
			elif( 22.5 <= direction < 67.5):
				opEdge1 = pixelData[i+1,j-1]
				opEdge2 = pixelData[i-1,j+1]

			#if gradient direction is at the 90 degree angle or 270 degree angle
			elif( 67.5 <= direction < 122.5 ):
				opEdge1 = pixelData[i+1,j]
				opEdge2 = pixelData[i-1,j]

			#if gradient direction is at the 135 degree angle or 315 degree angle
			elif( 112.5 <= direction < 157.5 ):
				opEdge1 = pixelData[i-1,j-1]
				opEdge2 = pixelData[i+1,j+1]
				
			#check
			if((pixelData[i,j] >= opEdge1) and (pixelData[i,j] >= opEdge2)):
				pass
			else:
				pixelData[i,j] = 0
				suppressCount += 1

	print("Completed Thinning Edges via non maxium supression. SupressCount = %d Negcount = %d"%(suppressCount,negcount))

	return pixelData




def doubleThresholdingandEdgeTracking(imageArray,lowerThreshold,upperThreshold, neighborCount):
	"""This function perfrom double thresholding and edge tracking to remove noise and thing edges from the 2D pixel data

		The result of this operation is reflected on 2D array

		Args:
			imageArray: the 2D greyscale image array
			lowerThreshold: pixel intensity below this threshold value will be set to zero
			upperThreshold: pixel intensoty above this threshold value will be set to 255
			Neighborcount: the number of surrounding pixels to be check for edge tracking

		Returns:
			thresholded  adn edge tracked imageArray
	"""

	print("Started Removing unrelated Edges via Double Thresholding and tracking related edge via edge tracking")
		
	pixelData = imageArray.copy()
	imageHeight, imageWidth = pixelData.shape

	for i in range(neighborCount,imageHeight-neighborCount):
		for j in range(neighborCount,imageWidth-neighborCount):

			#if this pixel's intensity is above upper threshoold then its an edge
			if(pixelData[i,j] > upperThreshold):
				pixelData[i,j] = 255

			#if the pixel's  intensity is below lower threshold the its not and edge
			elif(pixelData[i,j] < lowerThreshold):
				pixelData[i,j] = 0

			#if the pixel's intenshity is below uperthreshold and above lower threshold, check surrounding pixels
			else:
					
				#get horizontally right neigbors
				hrNeighbors = list(pixelData[i,j+1:neighborCount+1])
				hrCount = len([k for k in hrNeighbors if k > upperThreshold])

						
				#get horizontally left neighbors
				hlNeighbors = list(pixelData[i,j-1:j-neighborCount-1:-1])
				hlCount = len([k for k in hlNeighbors if k > upperThreshold])



				#get vertically down neighbors
				vdNeighbors = list(pixelData[i+1:neighborCount+1,j])
				vdCount = len([k for k in vdNeighbors if k > upperThreshold])


						   
				#get vertically up neighbors
				vuNeighbors = list(pixelData[i-1:i-neighborCount-1,j])
				vuCount = len([k for k in vuNeighbors if k > upperThreshold])

				#get primary diagonal right
				pdrNeighbors = []
				mthIndex = i + 1
				nthIndex= j + 1
				indexCount = 0
				while(indexCount < neighborCount):
					pdrNeighbors.append(pixelData[mthIndex,nthIndex])
					mthIndex += 1
					nthIndex += 1
					indexCount +=1
				pdrCount = len([k for k in pdrNeighbors if k > upperThreshold])



				#get primary diagonal left
				pdlNeighbors = []
				mthIndex = i - neighborCount
				nthIndex= j  - neighborCount
				indexCount = 0
				while(indexCount < neighborCount):
					pdlNeighbors.append(pixelData[mthIndex,nthIndex])
					mthIndex += 1
					nthIndex += 1
					indexCount += 1
				pdlCount = len([k for k in pdlNeighbors if k > upperThreshold])


				#get seconday diagonal left
				sdlNeighbors=[]
				mthIndex = i + 1
				nthIndex = j - 1
				indexCount = 0
				while(indexCount < neighborCount):
					sdlNeighbors.append(pixelData[mthIndex,nthIndex])
					mthIndex += 1
					nthIndex -= 1
					indexCount += 1
				sdlCount = len([k for k in sdlNeighbors if k > upperThreshold])


				#get secondary diagonal right
				sdrNeighbors=[]
				mthIndex = i - 1
				nthIndex = j + 1
				indexCount = 0
				while(indexCount < neighborCount):
					sdrNeighbors.append(pixelData[mthIndex,nthIndex])
					mthIndex -= 1
					nthIndex += 1
					indexCount += 1
				sdrCount = len([k for k in sdrNeighbors if k > upperThreshold])


				#descision to keep the pixel or not
				if(( hlCount >= neighborCount) or (hrCount >= neighborCount) or (vuCount >= neighborCount) or (vdCount >= neighborCount) or (pdrCount >= neighborCount) or (pdlCount >= neighborCount) or (sdrCount >= neighborCount) or (sdlCount >= neighborCount)):
					pixelData[i,j] = 255
				else:
					pixelData[i,j] = 0
		
	print("Completed Removing unrelated Edges via Double Thresholding and tracking related edge via edge tracking")

	return pixelData #return imageArray 




def houghTransfrom(imageArray, thetaStep):
	"""This function perfrom hough transfrom in the given imageArray
	
	Args:
		imageArray: the 2D greyscale image array
		thetaStep: the increment invervals between [0,180]

	Returns:
		hough accumulator
	""" 
	print("Started Hough Transfrom")

	imageHeight, imageWidth = imageArray.shape
	houghHeight = (numpy.sqrt(2) * max(imageHeight,imageWidth))/2
	accHeight = int(numpy.round(houghHeight * 2.0))
	accWidth = 180
	houghAccumulator  = numpy.zeros([accHeight,accWidth,3],float)

	centerX = imageWidth / 2
	centerY = imageWidth / 2


	for i in range(0,imageHeight):
		for j in range(0, imageWidth):
			if(imageArray[i,j] == 255):
				for theta in range(0,180,thetaStep):
					thetaRad = numpy.deg2rad(theta)
					rho = ((float(j) - centerX)*numpy.cos(thetaRad)) + ( (float(i)  - centerY) * numpy.sin(thetaRad))
					rho += houghHeight #shift negative values up
					if( rho > (accHeight - 0.5 )):
						rho = accHeight - 1
					iRho = int(numpy.round(rho))
					iTheta = theta
					houghAccumulator[iRho,iTheta,0] += 1
					houghAccumulator[iRho,iTheta,1] = rho
					houghAccumulator[iRho,iTheta,2] = theta

	#plt.figure("Hough Space",figsize=(100,100))
	#plt.imshow(houghAccumulator[:,:,0])
	#plt.set_cmap("gray")
	#plt.show()

	print("Hough Transform complete")

	return houghAccumulator #return the accumulator



def houghTransfromWithImageGradient(imageArray, imageGradient):
	"""This function perfrom hough transfrom in the given imageArray
	
	Args:
		imageArray: the 2D greyscale image array
		imageGradient: the 2D image gradient array generated from edge detection

	Returns:
		hough accumulator
	""" 
	print("Started Hough Transfrom")

	imageHeight, imageWidth = imageArray.shape
	houghHeight = (numpy.sqrt(2) * max(imageHeight,imageWidth))/2
	accHeight = int(numpy.round(houghHeight * 2.0))
	accWidth = 180
	houghAccumulator  = numpy.zeros([accHeight,accWidth,3],float)

	centerX = imageWidth / 2
	centerY = imageWidth / 2


	for i in range(0,imageHeight):
		for j in range(0, imageWidth):
			if(imageArray[i,j] == 255):
				theta = imageGradient[i,j]
				thetaRad = numpy.deg2rad(theta)
				rho = ((float(j) - centerX)*numpy.cos(thetaRad)) + ( (float(i)  - centerY) * numpy.sin(thetaRad))
				rho += houghHeight #shift negative values up
				iRho = int(numpy.round(rho))
				iTheta = int(numpy.round(theta))
				houghAccumulator[iRho,iTheta,0] += 1
				houghAccumulator[iRho,iTheta,1] = rho
				houghAccumulator[iRho,iTheta,2] = theta

	#plt.figure("Hough Space",figsize=(100,100))
	#plt.imshow(houghAccumulator[:,:,0])
	#plt.set_cmap("gray")
	#plt.show()

	print("Hough Transform complete")

	return houghAccumulator #return the accumulator




def boundaryChecks(val,minBoundary,maxBoundary):

	if(val > (maxBoundary - 0.5)):
		val = maxBoundary-1
	elif(val < minBoundary):
		val = minBoundary
	else:
		val = numpy.round(val)

	return int(val)




def detectHoughPoints(houghAccumulator,thresholdPercentage, imageHeight, imageWidth):
	""" This function detects points from the hough accumulator array

		Args:
			houghAccumulator: the accumulator array containing hough points

		Returns:
			line coordinates list([x1,y1,x2,y2])
	"""

	print("Started detecting hough points")

	#TODO THreshold could be 50% of the largest value in accumualtor
	threshold = int( numpy.round(numpy.max(houghAccumulator[:,:,0]) * (thresholdPercentage/100)))
	accHeight, accWidth, dim = houghAccumulator.shape
	diagonal = int(numpy.round(numpy.hypot(imageHeight,imageWidth)))
	
	pointList =[]
	#get rho and theta values that are above threshold
	for i in range(0,accHeight):
		for j in range(0,accWidth):
			
			x1 = y1 = x2 = y2 = 0
			if(houghAccumulator[i,j,0] > threshold):
				rho = houghAccumulator[i,j,1]
				theta = houghAccumulator[i,j,2]
				thetaRad = numpy.deg2rad(theta)
				
				if(45 <= theta <= 135):
					#y = (r - x cos(t)) / sin(t)
					x1 = 0
					y1 = (float(rho-(accHeight/2)) - ((x1 - (imageWidth/2) ) * numpy.cos(thetaRad))) / numpy.sin(thetaRad) + (imageHeight / 2)
					x2 = imageWidth - 0
					y2 = (float(rho-(accHeight/2)) - ((x2 - (imageWidth/2) ) * numpy.cos(thetaRad))) / numpy.sin(thetaRad) + (imageHeight / 2)
				
				else:
					#x = (r - y sin(t)) / cos(t);
					y1 = 0
					x1 = (float(rho-(accHeight/2)) - ((y1 - (imageHeight/2) ) * numpy.sin(thetaRad))) / numpy.cos(thetaRad) + (imageWidth / 2)
					y2 = imageHeight - 0
					x2 = (float(rho-(accHeight/2)) - ((y2 - (imageHeight/2) ) * numpy.sin(thetaRad))) / numpy.cos(thetaRad) + (imageWidth / 2)
				
					
				x1 = boundaryChecks(x1,0,imageWidth)
				y1 = boundaryChecks(y1,0,imageHeight)

				x2 = boundaryChecks(x2,0,imageWidth)
				y2 = boundaryChecks(y2,0,imageHeight)

				pointList.append([x1,y1,x2,y2])
				#pointList.append([int(numpy.round(x1)),int(numpy.round(y1)),int(numpy.round(x2)),int(numpy.round(y2))])

	print("Completed detecting hough points. Total Points %d"%len(pointList))
	return pointList

	
	
	


def createHoughLineImage(houghPoints,imageHeight,imageWidth):
	""" This function creates image using hough points
	
		Args:
			houghPoints: the x,y coordinates of hough points

		Returns:
			the 2D greyscale image array
	"""
	print("Started Hough Line Image")

	imageArray = numpy.zeros([imageHeight,imageWidth],int)
	
	missedPoints = 0
	for x1,y1,x2,y2 in houghPoints:
		#x1=points[0]
		#y1=points[1]
		#x2=points[2]
		#y2=points[3]
		#print(x1,y1,x2,y2)

		if(y1 == y2): #verical lines
			if(x1 < x2):
				for j in range(x1,x2+1):
					imageArray[y1,j] = 255
			elif(x1 > x2):
				for j in range(x2,x1+1):
					imageArray[y1,j] = 255

		elif(x1 == x2): #horizontal lines
			if(y1 < y2):
				for i in range(y1,y2+1):
					imageArray[i,x1] = 255
			elif(y1 > y2):
				for i in range(y2,y1+1):
					imageArray[y1,j] = 255


		elif((y1 < y2) and (x1 < x2) ): #primary diagonal
			index_Y = y1
			index_X = x1

			while((index_Y <= y2) and (index_X <= x2)):
				imageArray[index_Y,index_X] = 255
				index_Y += 1
				index_X += 1
			
			while((index_Y <= y2) and (index_X > x2)):
				imageArray[index_Y,index_X-1] = 255
				index_Y += 1

			while((index_Y > y2) and (index_X <= x2)):
				imageArray[index_Y-1,index_X] = 255
				index_X += 1

	
				
		elif((y1 > y2) and (x1 < x2) ): #secondary diagonal
			index_Y = y1
			index_X = x1

			while((index_Y >= y2) and (index_X <= x2)):
				imageArray[index_Y,index_X] = 255
				index_Y -= 1
				index_X += 1
			
			while((index_Y >= y2) and (index_X > x2)):
				imageArray[index_Y,index_X-1] = 255
				index_Y -= 1

			while((index_Y < y2) and (index_X <= x2)):
				imageArray[index_Y+1,index_X] = 255
				index_X += 1

		else:
			missedPoints += 1

	
	print("Completed Hough Line Image. Missed lines: %d"%missedPoints)
	return imageArray





def drawHoughLineImage(imageArray,lineImage,blendFactor):
	"""This function blends two images together into one image where bith imageArray have to be of the same size
		
		Args:
			imageArray1: 2D grey scale image array for image1
			imageArray2: 2D grey scale image array for image2
			blendFactor: determine which of the two images has more influence over the final image, musbet be between 0 < blendFactor < 1

		Returns:
			2D blended image array
	"""

	print("Started drawing hough line image")

	imageHeight, imageWidth = imageArray.shape
	blendedPixel= numpy.zeros(imageArray.shape,float)

	for i in range(0,imageHeight):
		for j in range(0,imageWidth):

			if(lineImage[i,j]==255):

				pixel1 = blendFactor * float(imageArray[i,j])
				pixel2 = (1-blendFactor) * float(lineImage[i,j])
				finalPixel = int(round(pixel1+pixel2))
				
				if(finalPixel < 0):
					blendedPixel[i,j] = 0
				elif(finalPixel > 255):
					blendedPixel[i,j] = 255
				else:
					blendedPixel[i,j] = finalPixel
			else:
				blendedPixel[i,j]=imageArray[i,j]

	print("Completed drawing hough line image")
	return blendedPixel


