import os
import pysrt
from video_ids import video_ids
MAX_HITS = 2


def load_all_srts(directory="./"):
    srts = []
    for filename in os.listdir(directory):
        if filename.endswith(".srt"):
            srts.append(pysrt.open(os.path.join(directory, filename)))
    return srts


def highlight(text, word):
    return text.replace(word, f"<span style='color: #aa88aa'>{word}</span>")


def find_sentences_for_pattern(args):
    pattern, srts = args
    hits = []
    cache = set()
    count = 0
    remove = len(pattern)
    print()
    print(pattern)

    while remove > len(pattern) - 2 and remove > len(pattern)//2:
        for video_count, subs in enumerate(srts):
            video_id = video_ids[video_count]
            fix_subs_link = f"https://studio.youtube.com/video/{video_id}/translations"
            last = None
            for sub, next_sub in zip(subs, subs[1:]):
                hours = sub.start.hours*3600
                minutes = sub.start.minutes*60
                seconds = sub.start.seconds
                seconds = seconds-1 if seconds > 0 else 0
                current_time = f"https://www.youtube.com/watch?v={video_id}&t={hours+minutes+seconds}"
                if pattern[:remove] in sub.text and sub.text not in cache:
                    text = ""
                    if last:
                        text += last.text + "<br>"

                    text += highlight(sub.text, pattern[:remove])
                    if pattern not in next_sub.text:
                        text += "<br>" + next_sub.text

                    cache.add(sub.text)
                    hits.append(text)
                    count += 1
                    print(text)
                    print(current_time)
                    print(fix_subs_link)
                    print("")
                    if count >= MAX_HITS:
                        # print(f"{remove}, {pattern[:remove]}/{pattern[remove:]}")
                        break
                last = sub
        remove -= 1
    print("_"*50)
    print(pattern)
    print("<hr>".join(hits))


# def main():
#     # Load patterns
#     # with open("current_monogatari.txt", encoding="utf-8") as f:
#     #     patterns = [line.strip() for line in f if line.strip()]

#     # # Load SRTs once
#     # srts = load_all_srts("./")

#     # sentences = {}
#     # for pattern in patterns:
#     #     sentences[pattern] = find_sentences_for_pattern((pattern, srts))[1]
    
#     # # Write output
#     # with open("with_sentences.txt", "w", encoding="utf-8") as f:
#     #     f.write("Word\tSentences\n")
#     #     for word, text in sentences.items():
#     #         f.write(f"{word}\t{text}\n")


if __name__ == "__main__":
    srts = load_all_srts("./")
    while True:
        find_sentences_for_pattern(((input("> ")), srts))
