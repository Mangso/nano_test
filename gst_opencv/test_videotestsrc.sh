gst-launch-1.0 videotestsrc is-live=true ! video/x-raw,framerate=25/1 ! videoconvert ! x264enc ! h264parse ! rtph264pay pt=96 ! udpsink host=192.168.0.49 port=10000
