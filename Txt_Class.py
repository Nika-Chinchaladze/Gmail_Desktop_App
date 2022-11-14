class TxtDealer:
    def __init__(self):
        self.hello = "world"

    def read_txt(self):
        with open("./format/format.txt", "r") as fmt:
            old_content = fmt.readlines()
            new_content = [item.strip() for item in old_content]
            fmt.close()
        return new_content

    def return_default(self, name):
        with open(f"./letters/{name}.txt", "r") as dft:
            wanted_text = dft.read()
            dft.close()
        return wanted_text
