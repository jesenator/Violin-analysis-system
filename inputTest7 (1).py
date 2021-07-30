# inputTest6.1.py

# working on splitting channel input to two arrays  - completed
################################################# functions
def getData(itr):
    def writeFile(p, frames, channels, filename):
        print("writing " + filename)
	wf = wave.open(filename, 'wb')
	wf.setnchannels(channels)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()

    # print sound level and threshold to terminal
    def printSound(rms, THRESHOLD):
	bars = ""
	scale_factor = 6

	for i in range(int(rms/scale_factor)):
	    bars = bars + "|"
	
	for i in range (rms/scale_factor, THRESHOLD/scale_factor):
	    bars = bars + " "
	bars = bars + "-"
	print(bars)


    # define callback for pyaudio
    def callback(data, frame_count, time_info, status): 
	    
	    frame = np.fromstring(data, dtype=np.int16)
	    
	    hammerChannel = frame[HAMMERCHANNEL::CHANNELS]
	    micChannel = frame[MICCHANNEL::CHANNELS]
	    
	    hammerData = hammerChannel.tostring()
	    micData = micChannel.tostring()
	    
	    rms = audioop.rms(data, 2)
	    hammerRms = audioop.rms(hammerData, 2)
	    micRms = audioop.rms(micData,2)

	    if (recording != 2):
		    # printSound(rms, THRESHOLD)
	    
		    hammerFramesDe.append(hammerData)
		    micFramesDe.append(micData)
		    
		    framesDe.append(data)
		    rmsDe.append(rms)
		    hammerRmsDe.append(hammerRms)
		    micRmsDe.append(micRms)
		    
		    diff = datetime.now() - startTime
		    seconds = diff.total_seconds()
		    xDe.append(round(seconds, 2))
		    
		    # print(len(framesDe))
		    
	    
	    # while the sound threshold has not been surpassed, trim the buffers to a set length
	    if len(rmsDe) > RECORDING_FRAMES + BUFFER_FRAMES + 3:
		    rmsDe.popleft()
		    xDe.popleft()
		    hammerRmsDe.popleft()
		    micRmsDe.popleft()
		    
	    if len(framesDe) > BUFFER_FRAMES and recording == 0:
		    framesDe.popleft()
		    hammerFramesDe.popleft()
		    micFramesDe.popleft()
	
       
	    # start recording if sound threshold is surpassed
	    if (hammerRms > THRESHOLD and recording == 0):
		    global time
		    time = datetime.now()
		    # recording = True
		    startRecording() # this is a hack of a solution because 
						    # assigning the variable within the callback
						    # function caused issues.
		    print("*** recording")

	    # stop taking data from the audio stream and stop the plot
	    if recording == 1 and (datetime.now() - time > timedelta(seconds = RECORD_SECONDS)):
		    print("*** recording finished")
		    print("close plotter window")
		    endRecording()
		    animate(0)
		    ani.event_source.stop()

	    return (data, pyaudio.paContinue)


    def animate(i):	
	ax.clear()
	if recording == 0:
	    plt.title("listening")
	elif recording == 1:
	    plt.title("recording")
	elif recording == 2:
	    plt.title("recording finished - close plotter window")
		
	plt.xlabel("time")
	plt.ylabel("volume")
	x = xDe
	y = rmsDe
	y2 = hammerRmsDe
	y3 = micRmsDe
	
	ax.set_ylim(0, Y_LIMIT)
	ax1.set_ylim(0, Y_LIMIT)
	ax2.set_ylim(0, Y_LIMIT)
	ax3.set_ylim(0, Y_LIMIT)
	
	# ax.plot(x, y)
	ax1.plot(x, np.full(len(y), THRESHOLD), label="hammer threshold")
	ax2.plot(x, y2, label="hammer")
	ax3.plot(x, y3, label="mic")
	ax2.legend()
	
    def startRecording():
	global recording
	recording = 1

    def endRecording():
	global recording
	recording = 2

    def getSeconds():
	milliseconds = int(datetime.strftime(datetime.now(), '%f'))
	seconds = round(milliseconds/1000, 1)
	# print(seconds)
	print(milliseconds)
	return seconds
	
	
	
    def encode(line):
	temp = base64.b64encode(bytes(line, encoding))
	temp = temp.decode("Ascii") + "\n"
	encoded = bytes(temp, encoding)
	return encoded

    def serialWrite(p, filename, frames):
	ser.write(encode(filename))
	
	if ".txt" in filename:
	    f = open(filename, "r")
	    for line in f:
		encoded = encode(line)
		decoded = base64.b64decode(encoded)
		# print("sending: " + decoded.decode("Ascii"), end="")
		ser.write(encoded)
		
	elif ".wav" in filename:
	    for frame in frames:
		ser.write(encode(frame))
		
	
	ser.write(bytes("*\n", encoding))
	
    def upload(p, HAMMER_OUTPUT_FILE, MIC_OUTPUT_FILE, hammerFrames, micFrames):
	ser = serial.Serial(port='/dev/ttyUSB0',
			    baudrate=115200,
			    parity=serial.PARITY_NONE,
			    stopbits=serial.STOPBITS_ONE,
			    bytesize=serial.EIGHTBITS,
			    timeout=1)
	encoding = 'iso-8859-1'
	
	serialWrite(p, HAMMER_OUTPUT_FILE, hammerFrames)
	serialWrite(p, MIC_OUTPUT_FILE, MICFrames)

	
	
	
    ############################################ main
    import sys      
    import pyaudio
    import wave
    import sys
    import os
    import struct
    import numpy as np
    import audioop
    import matplotlib.pyplot as plt
    import matplotlib.animation as animation
    from datetime import timedelta
    from datetime import datetime
    import time
    import collections
    import serial

    print("running inputTest.py")
    p = pyaudio.PyAudio()

    # pyaudio stream characteristics
    CHUNK = int(1024*4)
    FORMAT = pyaudio.paInt16
    DEVICE_INDEX= 2
    CHANNELS = 2
    RATE = 44100

    RECORD_SECONDS = 1.5
    RECORDING_BUFFER_SECONDS = .2

    # THRESHOLD = 120
    # Y_LIMIT = THRESHOLD * 5
    THRESHOLD = 50
    Y_LIMIT = 1500
    # MIC_VISUAL_MULTIPLIER = 3

    startTime = datetime.now()

    # ouput file names
    OUTPUT_FILE = "output.wav"
    HAMMER_OUTPUT_FILE = "hammer_output" + str(itr) + ".wav"
    MIC_OUTPUT_FILE = "mic_output" + str(itr) + ".wav"

    # one channel is 0 and the other is 1. 
    MICCHANNEL = 1
    HAMMERCHANNEL = 0

    # this first measurment works when CHUNK 1024*3 but not for 1024*1
    FRAMES_PER_SECOND = RATE / CHUNK
    # FRAMES_PER_SECOND = 23

    BUFFER_FRAMES = FRAMES_PER_SECOND * RECORDING_BUFFER_SECONDS
    RECORDING_FRAMES = FRAMES_PER_SECOND * RECORD_SECONDS

    print("Input info: ", p.get_default_input_device_info())

    stream = p.open(format = FORMAT,
		    channels = CHANNELS,
		    rate = RATE,
		    input_device_index = DEVICE_INDEX,
		    input = True,
		    frames_per_buffer = CHUNK,
		    stream_callback = callback)

    frames, hammerFrames, MicFrames, x, y, = [], [], [], [], []
    cutoffLine = []
    global recording
    recording = 0

    framesDe = collections.deque()
    hammerFramesDe = collections.deque()
    micFramesDe = collections.deque()
    rmsDe = collections.deque()
    hammerRmsDe = collections.deque()
    micRmsDe = collections.deque()
    xDe = collections.deque()

    print("starting stream")
    stream.start_stream()

    fig = plt.figure()
    ax = plt.subplot()
    ax1 = plt.subplot()
    ax2 = plt.subplot()
    ax3 = plt.subplot()
    ani = animation.FuncAnimation(fig, animate, interval=25)
    plt.show()

    stream.stop_stream()
    stream.close()
    p.terminate()
	
    frames = framesDe
    hammerFrames = hammerFramesDe
    micFrames = micFramesDe

    # writeFile(p, frames, 1, OUTPUT_FILE)
    writeFile(p, hammerFrames, 1, HAMMER_OUTPUT_FILE)
    writeFile(p, micFrames, 1, MIC_OUTPUT_FILE)
    # upload(p, HAMMER_OUTPUT_FILE, MIC_OUTPUT_FILE, hammerFrames, micFrames)

    # os.system("aplay " + OUTPUT_FILE)
    # os.system("aplay " + HAMMER_OUTPUT_FILE)
    # os.system("aplay " + MIC_OUTPUT_FILE)



for i in range(50):
    try:
	os.remove("*_output*.wav")
    except:
	pass

POINTS = 4
for itr in range(POINTS):
    print("data point " + str(itr))
    getData(itr)
