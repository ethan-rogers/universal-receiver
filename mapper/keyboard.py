top_left = [30,30]
height = 30
spacing = 3

keys_row1 = ["esc", "na"]  + [f"F{i}" for i in range(1,13)] + ["del"]
width_row1 = [height, 15] + [height for i in range(13)]

keys_row2 = ['`'] + [str(i) for i in range(1, 10)] + ["0", "-", "+", "<-"]
width_row2 = [20] + [30 for i in range(12)] + [55]



rows = [[keys_row1, width_row1], [keys_row2, width_row2]]