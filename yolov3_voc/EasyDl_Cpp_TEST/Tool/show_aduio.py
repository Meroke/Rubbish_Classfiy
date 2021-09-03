with open("/proc/asound/pcm") as f:
    s = f.read()
    for line in s.split("\n"):
        if "playback 4" in line:
            number = line.split(":")[0].split("-")
            print(int(number[0]), int(number[1]))