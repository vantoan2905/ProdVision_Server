import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

Gst.init(None)

def bus_call(bus, message, loop):
    t = message.type
    if t == Gst.MessageType.EOS:
        print("End-of-stream")
        loop.quit()
    elif t == Gst.MessageType.ERROR:
        err, debug = message.parse_error()
        print(f"Error: {err}, {debug}")
        loop.quit()
    return True

def main():
    # pipeline đọc video file và stream ra tcp port 5000
    pipeline_str = (
        "filesrc location=/mnt/d/pcb_defect/ProdVision_django/test_video.mkv ! decodebin ! videoconvert ! "
        "x264enc tune=zerolatency bitrate=500 speed-preset=superfast ! "
        "h264parse ! tcpserversink host=127.0.0.1 port=5000"
    )
    
    pipeline = Gst.parse_launch(pipeline_str)
    
    loop = GLib.MainLoop()
    bus = pipeline.get_bus()
    bus.add_signal_watch()
    bus.connect("message", bus_call, loop)
    
    pipeline.set_state(Gst.State.PLAYING)
    try:
        loop.run()
    except KeyboardInterrupt:
        pass
    pipeline.set_state(Gst.State.NULL)


if __name__ == "__main__":
    main()
