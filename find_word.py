import os
import pysrt
import re
from video_ids import video_ids
import pysrt

# for HTML at the end
example_sentence_limit = 3

def print_long(string, length):
    total_length = length
    middle = f" {string} "
    side_length = (total_length - len(middle)) // 2

    # If the total is odd, you might need one more dash on the right
    print("ー" * side_length + middle + "ー" * (total_length - len(middle) - side_length))

HIGHLIGHT_BG = '\033[43m'  # Yellow background
RESET = '\033[0m'

def highlight(text, word, anki=False):
    if anki:
        return text.replace(word, f"<span style='color: #aa88aa'>{word}</span>")
    return text.replace(word, f"{HIGHLIGHT_BG}{word}{RESET}")

def get_time(sub):
    return ""


while 1:
    sentences = []
    regex = input("Regex? Y/n")
    if regex != "Y":
        regex = False

    if regex:
        pattern = re.compile(rf"{input('Pattern to look for > ')}")
    else:
        pattern = input('Name to look for > ')

    count = 0
    file_count = 0
    for filename in os.listdir("./"):
        if filename.endswith("srt"):
            full_path = os.path.join("./", filename)
            video_id = video_ids[file_count]
            fix_subs_link = f"https://studio.youtube.com/video/{video_id}/translations"
            subs = pysrt.open(full_path)

            # Create SRT files for each part
            file = pysrt.SubRipFile()

            current_part = 0
            for sub in subs:
                file.append(sub)


            # Shift the timestamps of each part
            last = None
            for sub, next_sub in zip(file, file[1:]):

                hours = sub.start.hours*3600
                minutes = sub.start.minutes*60
                seconds = sub.start.seconds
                seconds = seconds-1 if seconds > 0 else 0
                current_time = f"https://www.youtube.com/watch?v={video_id}&t={hours+minutes+seconds}"


                if regex:
                    result = pattern.search(sub.text)
                    if not result:
                        pattern.search(sub.text+"\n"+next_sub.text)
                    if result:
                        print_long(filename[:-4], 40)
                        add_sentence = ""
                        if last:
                            print(str(last.start)[:-4], highlight(last.text, result.group()))
                            add_sentence += highlight(last.text, result.group(), anki=True) + "<br>"
                        else:
                            print("[Start of file]")


                        print(str(sub.start)[:-4], highlight(sub.text, result.group()))
                        print(str(next_sub.start)[:-4], highlight(next_sub.text, result.group()))

                        add_sentence += highlight(sub.text, result.group(), anki=True) + "<br>"
                        add_sentence += highlight(next_sub.text, result.group(), anki=True)  

                        if len(sentences) <= example_sentence_limit:
                            sentences.append(add_sentence)

                        print("Link to Video:\t",current_time)
                        print("Edit Subs:\t",fix_subs_link)
                        print("ー" * 35)
                        count += 1
                else:
                    if pattern in sub.text:
                        print(filename)
                        add_sentence = ""
                        if last:
                            print(str(last.start)[:-4], last.text)  
                            add_sentence += highlight(last.text, pattern, anki=True) + "<br>"
                        else:
                            print("[Start of file]")

                        print(str(sub.start)[:-4], highlight(sub.text, pattern))
                        print(str(next_sub.start)[:-4], next_sub.text)

                        add_sentence +=  highlight(sub.text, pattern, anki=True) + "<br>"
                        add_sentence +=  highlight(next_sub.text, pattern, anki=True)

                        if len(sentences) < example_sentence_limit:
                            sentences.append(add_sentence)


                        print("Link to Video:\t",current_time)
                        print("Edit Subs:\t",fix_subs_link)
                        print("ー" * 35)
                        count += 1 
                        continue

                    # for length in range(len(pattern)-1, 0, -1):
                        last_chars = pattern[-length:]
                        without = pattern[:-length]
                        if len(pattern) <= length:
                            continue
                        if sub.text.endswith(without) and next_sub.text.startswith(last_chars):
                            print(filename)
                            if last:
                                print(str(last.start)[:-4], last.text)  
                            else:
                                print("[Start of file]")
                            print(str(sub.start)[:-4], highlight(sub.text, without))
                            print(str(next_sub.start)[:-4], highlight(next_sub.text, last_chars))
                            print("Link to Video:\t",current_time)
                            print("Edit Subs:\t",fix_subs_link)
                            print("ー" * 35)
                            count += 1 
                            continue

                last = sub
            file_count += 1

    print(f"Encountered {count} {'time' if count == 1 else 'times'}")
    if sentences:
        print("-"*30)
        print("<hr>".join(sentences))
    count = 0