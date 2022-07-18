from tkinter import *
root = tk.Tk()
filez = fd.askopenfilenames(parent=root, title='Choose a file')




class RawFileTinker(Frame):
    def __init__(self):
        Frame.__init__(self)

        self._frame_width = 100

        self.master.title("RawFileExtractor")
        self.master.rowconfigure(5, weight=1)
        self.master.columnconfigure(5, weight=1)
        self.grid(sticky=W + E + N + S)

    def convert_file(self):
        INPUT_FILE = "PATH/TO/FILE"
        MOD_MAP = {
            '200.3XXX': '54.x',
            'X': 'Y'
        }

        lines = []
        with open(INPUT_FILE) as file:
            for line in file:
                for key, value in MOD_MAP.items():
                    lines.append(line.replace(value, key))

        with open(INPUT_FILE + ".saby", 'w') as file:
            file.write("".join(lines))


if __name__ == "__main__":
    RawFileTinker().mainloop()