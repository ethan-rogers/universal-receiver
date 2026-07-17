top_left = [20,20]
height = 30
spacing = 3

media_buffer = 10

media_controls = ["SP_MediaPlay", 
                  "SP_MediaPause", 
                  "SP_MediaSeekBackward",
                  "SP_MediaSeekForward",
                  "SP_MediaSkipBackward",
                  "SP_MediaSkipForward",
                  "SP_MediaStop",
                  "mute.png", 
                  "volume-down.png",
                  "volume-up.png", 
                  "brightness-down.png",
                  "brightness-up.png"]

media_width = [height for i in range(len(media_controls))]

keys_row1 = ["esc", "na"]  + [f"F{i}" for i in range(1,13)] + ["del"]
width_row1 = [height, 15] + [height for i in range(13)]

keys_row2 = ['`'] + [str(i) for i in range(1, 10)] + ["0", "-", "+", "<-"]
width_row2 =  [height for i in range(13)] + [47]

keys_row3 = ["tab", "q","w","e","r","t","y","u","i","o","p", "[", "]", "\\"]
width_row3 = [47] + [height for i in range(13)]

keys_row4 = ["caps", "a", "s", "d", "f", "g", "h", "j", "k", "l", ";", "'", "enter"]
width_row4 = [52] + [height for i in range(11)] + [60]

keys_row5 = ["shift", "z", "x", "c", "v", "b", "n", "m", ",", ".", "/", "na", "^"]
width_row5 = [57] + [height for i in range(10)] + [25, 30]

keys_row6 = ["ctrl", "alt", "wdw", "___", "fn", "na", "<", " v ", ">"]
width_row6 = [35 for i in range(3)] + [197,35] + [height for i in range(4)]

rows = [[media_controls, media_width],
        [keys_row1, width_row1],
        [keys_row2, width_row2], 
        [keys_row3, width_row3],
        [keys_row4, width_row4],
        [keys_row5, width_row5],
        [keys_row6, width_row6]]
