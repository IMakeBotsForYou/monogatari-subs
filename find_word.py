import os
import pysrt
import re
#from video_ids import video_ids

import pysrt

video_ids = {
    "01   化物語 上 神谷 浩史.srt": "SERSaWm60bE",
    "02   化物語 中 1 加藤 英美里.srt": "T70BPU0seTA",
    "02   化物語 中 2 加藤 英美里.srt": "lYDodasbU3w",
    "03   化物語 下 斎藤 千和.srt": "bCmiFTOVF8M",
    "04   傷物語 1 井上 麻里奈.srt": "r6X3i5B36E4",
    "04   傷物語 2 井上 麻里奈.srt": "H7CGgAggMys",
    "05   偽物語 上 櫻井 孝宏.srt": "ztn4u2Ymsbw",
    "06   偽物語 下 坂本 真綾.srt": "rkPT0vFpcDM",
    "07   猫物語 黒 加藤 英美里.srt": "mM781AhuvzQ",
    "08   猫物語 白 沢城 みゆき.srt": "8lO1ISyT9nM",
    "09   傾物語 井口 裕香.srt": "Ht5OXUAkLV4",
    "10   花物語 堀江 由衣.srt": "CBWSkgXxlyA",
    "11   囮物語 三木 眞一郎.srt": "3PGp53TISnQ",
    "12   鬼物語 喜多村 英梨.srt": "OZ3h8bfFLXc",
    "13   恋物語 ゆきの さつき.srt": "TLBTzR0ULug",
    "14   憑物語 白石 涼子.srt": "yCmHkMImQZ8",
    "15   暦物語 1 早見 沙織.srt": "WFduj5rY2Mo",
    "15   暦物語 2 早見 沙織.srt": "jce2NXJ8cU0",
    "16   終物語 上 第1話 水橋 かおり.srt": "mzjda8VxUcU",
    "16   終物語 上 第2話 水橋 かおり.srt": "yDIhe971VC0",
    "16   終物語 上 第3話 水橋 かおり.srt": "xQlYLJhl7HE",
    "17   終物語 中 斎藤 千和.srt": "z9bdKE8NAeQ",
    "18   終物語 下 1 加藤 英美里.srt": "5xm1d0VC-sY",
    "18   終物語 下 2 加藤 英美里.srt": "4r3qEpcZeQY",
    "19   続・終物語 井上 麻里奈.srt": "GcARWSvzA5E",
    "20   愚物語 櫻井 孝宏.srt": "7QaFZKrbLXw",
    "21   業物語 三木 眞一郎.srt": "CFlOEA43Xlo",
    "22   撫物語 ゆきの さつき.srt": "cXMntZaZBYI",
    "23   結物語 花澤 香菜.srt": "DKhqmtrE2ak",
    "24   忍物語 白石 涼子.srt": "eJASqnm4QlY",
    "25   宵物語 ゆきの さつき.srt": "oUm5xL6FcBw",
    "26   余物語 早見 沙織.srt": "Qoud12pThYI",
    "27   扇物語 堀江 由衣.srt": "vybLXHoiLwg",
    "28   死物語 上 白石 涼子.srt": "OXKP7zmml9M",
    "29   死物語 下 加藤 英美里.srt": "t5nFhGtRCr0",
    "30   戦物語 日笠 陽子.srt": "cJzc4dkRNjw"
}


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
            video_id = video_ids[filename]
            # print(f'"{filename}": "{video_id}",')
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
                        # print("Edit Subs:\t",fix_subs_link)
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

                        # print(str(sub.start)[:-4], highlight(sub.text, pattern))
                        # print(str(next_sub.start)[:-4], next_sub.text)

                        add_sentence +=  highlight(sub.text, pattern, anki=True) + "<br>"
                        add_sentence +=  highlight(next_sub.text, pattern, anki=True)

                        if len(sentences) < example_sentence_limit:
                            sentences.append(add_sentence)


                        print("Link to Video:\t",current_time)
                        # print("Edit Subs:\t",fix_subs_link)
                        print("ー" * 35)
                        count += 1 
                        continue

                    # If you want to find words that are cut off
                    for length in range(len(pattern)-1, 0, -1):
                        last_chars = pattern[-length:]
                        without = pattern[:-length]
                        if len(pattern) <= length:
                            continue
                        if sub.text.endswith(without) and next_sub.text.startswith(last_chars):
                            print(filename)
                            add_sentence = ""
                            if last:
                                print(str(last.start)[:-4], last.text)  
                                add_sentence +=  highlight(last.text, pattern, anki=True) + "<br>"
                                
                            else:
                                print("[Start of file]")
                            print(str(sub.start)[:-4], highlight(sub.text, without))
                            print(str(next_sub.start)[:-4], highlight(next_sub.text, last_chars))

                            add_sentence +=  highlight(sub.text, pattern, anki=True) + "<br>"
                            add_sentence +=  highlight(next_sub.text, pattern, anki=True)
                          
                            if len(sentences) < example_sentence_limit:
                                sentences.append(add_sentence)


                            print("Link to Video:\t",current_time)
                            # print("Edit Subs:\t",fix_subs_link)
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
