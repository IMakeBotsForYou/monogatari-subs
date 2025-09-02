import os
import pysrt
import re

def print_long(string, length):
    total_length = length
    middle = f" {string} "
    side_length = (total_length - len(middle)) // 2

    # If the total is odd, you might need one more dash on the right
    print("ー" * side_length + middle + "ー" * (total_length - len(middle) - side_length))

HIGHLIGHT_BG = '\033[43m'  # Yellow background
RESET = '\033[0m'
def highlight(text, word):
    return text.replace(word, f"{HIGHLIGHT_BG}{word}{RESET}")

while 1:
    regex = input("Regex? Y/n")
    if regex != "Y":
        regex = False

    if regex:
        pattern = re.compile(rf"{input('Pattern to look for > ')}")
    else:
        pattern = input('Name to look for > ')

    count = 0
    for filename in os.listdir("./"):
        if filename.endswith("srt"):
            full_path = os.path.join("./", filename)

            subs = pysrt.open(full_path)

            # Create SRT files for each part
            file = pysrt.SubRipFile()

            current_part = 0
            for sub in subs:
                file.append(sub)


            # # Shift the timestamps of each part
            last = None
            for sub, next_sub in zip(file, file[1:]):
                if regex:
                    result = pattern.search(sub.text)
                    if result:
                        print_long(filename[:-4], 40)
                        if last:
                            print(str(last.start)[:-4], highlight(last.text, result.group()))
                        else:
                            print("[Start of file]")
                        print(str(sub.start)[:-4], highlight(sub.text, result.group()))
                        print(str(next_sub.start)[:-4], highlight(next_sub.text, result.group()))
                        print("ー" * 35)
                        count += 1
                else:
                    for length in range(len(pattern), 0, -1):
                        last_chars = pattern[-length:]
                        without = pattern[:-length]
                        if len(pattern) <= length:
                            continue
                        if sub.text.endswith(without) and next_sub.text.startswith(last_chars):
                            if last:
                                print(str(last.start)[:-4], last.text)  
                            else:
                                print("[Start of file]")
                            print(str(sub.start)[:-4], highlight(sub.text, without))
                            print(str(next_sub.start)[:-4], highlight(next_sub.text, last_chars))
                            print("ー" * 35)
                            count += 1 

                last = sub

    print(f"Encountered {count} {'times' if count > 1 else 'time'}")
    count = 0