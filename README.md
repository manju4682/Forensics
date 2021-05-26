# Real-time face detection and capture and vehicle registration number detection at the scene of crime

## Motivation for the project
We all know that, a lot of crimes happen at ATMs, banks and other places. And CCTV evidence plays a very important role to nab the culprits. So, the idea was to automate this process to capture details at the scene of crime when the alarm goes off. 

## Features
At most places CCTV surveillance is common to capture any untoward incident or for personal security and many other reasons. This application builds on this idea. Taking CCTV streaming as input(used webcam as prototype), whenever the alarm goes off, the application captures details present at the scene of action. The details include faces of people present at the site and identifies vehicles based on registration numbers. This application can be connected to mugshot database of criminals and it becomes easy to find out the culprits within seconds. And the vehicle numbers extracted from the scene can be used to identify the owners by connecting it to the vehicles registration database. 

## Implementation and Tools used 
• OpenCV is used to capture the frame. And to detect faces present in the frame. And several OpenCV operations are used to isolate the number plate from the image.
• pytessseract is a ocr (optical character recognition) tool. And it used in the application to extract characters from the isolated probable numberplate. 
• EasyOcr is also a ocr tool. And even this was used to extract characters from the numberplate. Along with probable characters present, it also provides a factor to decide to what extent are the characters identified match the real characters on the plate. 
• And several other python packages to handle various functions.

## Conclusion and takeaways
The world is quickly adopting to visual technology, be it in the field of entertainment or automated driving or even forensics. And digital forensics data plays a very important role to make advancements to crack any case. Since we already have CCTVs to monitor crucial places all time around, it makes sense to automate the process of looking at the CCTV data to find who might be the probable culprits. And this project is a prototype of one such automation tool that might be possible.
