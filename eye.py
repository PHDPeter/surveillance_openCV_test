#!/home/peter/.virtualenvs/cv/bin/python /home/peter/eye.py
#echo $pyenv_python
import cv2

import sounddevice as sd
from scipy.io.wavfile import write
import soundfile as sf

import skvideo.io

# sudo ln -s /home/peter/Documents/gits/surveillance_openCV_test/eye.py /bin/eyes

def run_cam(cam_u=0):
    cam_used=0
    cam_list = []
    # try:
    #     vr= cv2.VideoCapture(0)
    # except:
    #     print("no cam to view") #shuld add a defult view here
    #cam_list.append(vr)
    for i in range(0,10):#just set to a hi number
        vr1 = cv2.VideoCapture(i)
        if vr1 is None or not vr1.isOpened():
            #print('Warning: unable to open video source: ', i)
            #print(i)
            break
        else:
            #print(i)
            cam_list.append(vr1)

    if len(cam_list)==0:
        print("Warning: unable to open any video source")
    else:
        print(str(len(cam_list))+" number of cam avalible")

    isFrame, frame =cam_list[cam_used].read()

    adio_on = False
    recod=False
    r_cout=0

    while isFrame:
        
        
        cv2.imshow("test_window",frame)

        key=cv2.waitKey(1)

        if key == ord('a'):
            if adio_on==True:
                adio_on=False
            else:
                adio_on = True

        if adio_on==True:
            #print("no")
            cv2.putText(frame, "audio on", (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                        0.5, (0, 0, 255), 2)
            audio()

        if key == ord('r'):
            if recod==True:
                recod=False
                out.close()
            else:
                recod = True
                r_cout=r_cout+1
                out = skvideo.io.FFmpegWriter("saved_rec_"+str(r_cout) + '.avi', outputdict={
                    '-vcodec': 'libx264',  # use the h.264 codec
                    '-crf': '0',  # set the constant rate factor to 0, which is lossless
                    '-preset': 'veryslow'  # the slower the better compression, in princple, try
                    # other options see https://trac.ffmpeg.org/wiki/Encode/H.264
                })

        if recod==True:
            out.writeFrame(frame[:, :, ::-1])
        
        if key == ord('q'):
            for cam in cam_list:
                cam.release()
            cv2.destroyAllWindows()

        if key == ord('n'):
            if cam_used<len(cam_list):
                cam_used=cam_used+1
            else:
                cam_used=0 #looping back to start
            
        else:
            isFrame, frame =cam_list[cam_used].read()
            
    cv2.destroyAllWindows()
    if recod==True:
        out.close()


def audio():

    fs = 44100  # Sample rate
    seconds = 0.01  # Duration of recording
    #print(sd.query_devices(kind='input'))
    #sd.default.device = 5#'Plantronics Blackwire C210'
    #myrecording = sd.playrec(myarray,fs, channels=2)

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait until recording is finished

    sd.play(myrecording, fs)
    #status = sd.wait()  # Wait until file is done playing

    #write('output.wav', fs, myrecording)  # Save as WAV file
    #print("finished recording")
    
run_cam()
#audio()