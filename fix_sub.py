import pysrt
import os
from concurrent.futures import ThreadPoolExecutor
import re
from names_per_file import NAMES 

def split_and_shift_srt(file_path, split_times):
    subs = pysrt.open(file_path)

    
     # Convert split_times from milliseconds to SubRipTime objects
    split_times = [pysrt.SubRipTime(milliseconds=t) for t in split_times]

    
    # Prepare containers for each split part
    parts = [pysrt.SubRipFile() for _ in range(len(split_times) + 1)]

    current_part = 0
    for sub in subs:
        while current_part < len(split_times) and sub.start >= split_times[current_part]:
            current_part += 1
        parts[current_part].append(sub)

      
    # Shift each part so its first subtitle starts at 0
    for i in range(1, len(parts)):
        if parts[i]:
            first_start = parts[i][0].start
            for sub in parts[i]:
                sub.shift(seconds=-first_start.ordinal / 1000.0)  
    # shift using built-in

    
    # Save split files
    for i, part in enumerate(parts):
        part.save(f'28 - 死物語　{i+1} 上 (白石 涼子).srt', encoding='utf-8')

# print(len(["苛虎", "蛞蝓豆腐", "障り猫", "蛇切縄", "臥煙遠江", "暴力陰陽師", "クチナワさん", "クチナワ", "影縫", "影縫余弦さん", "ヶ原", "ヶ原さん", "遠江", "遠江さん", "わたくし", "神原", "神原駿河", "神原駿河さん", "アセロラオリオン", "ハートアンダーブレード", "ハートアンダーブレードさん", "キスショット", "死屍累生死郎", "老倉", "千石ちゃん", "千石撫子", "斧乃木ちゃん", "斧乃木余接", "斧乃木さん", "ブラック羽川", "阿良々木火憐ちゃん", "阿良々木火憐さん", "阿良々木火憐", "阿良々木火憐さん", "阿良々木火憐ちゃん", "阿良々木月火", "あるじ様", "扇", "扇ちゃん", "扇さん", "扇くん", "忍野扇", "トロピカレスク", "ホームアヴェイヴ", "ドッグストリングス", "トロピカレスク・ホームアヴェイヴ・ドッグストリングス", "スーサイドマスター", "デストピア", "ヴィルトゥオーゾ", "ヴィルトゥオーゾ", "デストピア・ヴィルトゥオーゾ・スーサイドマスター", "エピソード", "ギロチンカッター", "ドラマツルギー", '貝木', '貝木くん', '貝木さん', '貝木のお兄ちゃん', '戦場ヶ原さん', '羽川先輩', '翼先輩', '羽川ちゃん', '阿良々木くん', '翼', '暦お兄ちゃん', '貝木泥舟', '阿良々木ちゃん', '吸血鬼さん', 'ひたぎ義姉さん', '洗人さん', '忍野さん', '真宵さん', '阿良々木', '羽川', '羽川翼ちゃん', 'ツンデレ', '戦場ヶ原先輩', '吸血鬼もどき', '阿良々木暦さん', '洗人', '鬼のお兄ちゃん', '臥煙伊豆湖', '阿良々木先輩', '忍野メメさん', '月火くん', '羽川翼', '余接さん', '忍野忍', '臥煙', '火憐さん', '委員長ちゃん', '臥煙伊豆湖さん', '月火', '阿良々木暦', '月火ちゃん', '貝木泥舟さん', '火憐ちゃん', '吸血鬼のお兄ちゃん', '八九寺', '臥煙さん', '余接', '阿良々木暦くん', '八九寺さん', '真宵ちゃん', 'ひたぎちゃん', '真宵', '忍野忍ちゃん', '委員長さん', 'ガハラさん', '八九寺ちゃん', '羽川さん', '暦さん', '戦場ヶ原ひたぎ先輩', '忍野お兄ちゃん', '忍野のお兄ちゃん', '忍野', '吸血鬼ちゃん', '委員長', '暦ちゃん', '羽川翼さん', '戦場ヶ原ちゃん', '洗人迂路子さん', '翼さん', '戦場ヶ原ひたぎさん', '臥煙先輩', '戦場ヶ原ひたぎ', '翼ちゃん', '阿良々木さん', '忍野くん', 'ひたぎさん', 'ツンデレちゃん', 'ガハラ', '鬼いちゃん', 'ひたぎ先輩', '忍野メメ', '怪異', '吸血鬼', '余接ちゃん', '暦くん', '月火のお兄ちゃん', '暦', 'ひたぎ', '火憐', '怪異もどき', '月火さん', '戦場ヶ原', '洗人迂路子', '忍野忍さん']))



def fix_subs(file_name):
    subs = pysrt.open(file_name)
    fixed_subs = pysrt.SubRipFile()

    for sub, next_sub in zip(subs, subs[1:]):

        if not next_sub.text.strip():
            sub.end = next_sub.end
            next_sub.start = next_sub.end


        # found  = re.search(r"^[」。、]", next_sub.text)
        # found1 = re.search(rf"[^。、]$", sub.text)
        if found: # and len(next_sub.text) > 10 and found1:
            print("-"*30)
            print(file_name)
            print(sub.start)
            print(sub.text)
            print(next_sub.text) 
            print(f"|{found.group()}|")
            print("-"*30)
            print("\n")             
            
            # move back 

            sub.text = sub.text + next_sub.text[:found.span()[1]] 
            next_sub.text = next_sub.text[found.span()[1]:] 

            # move to next 
            # next_sub.text = sub.text[found.span()[0]:] + next_sub.text 
            # sub.text = sub.text[:found.span()[0]] 

            sub.end -= 200
            next_sub.start -= 200

            print(sub.text)
            print(next_sub.text) 
            print("\n") 
            print("\n")

        # for full_name in NAMES[file_name]
        #     for length in range(len(full_name), -1, -1):

        #         last = full_name[-length:]
        #         without = full_name[:-length]
                
        #         if len(full_name) <= length:
        #             continue

        #         particles = r"(も|じゃ(のう?|な|よ)?|よね?な?|・|まで|から?(したら|に?は)?|に(とって)?(対して)?は?|は|の((よう(な|に)?)|こと[をが]?)?|が|を|と(?!し)は?|への|で(?!きる)(さえ|も|)?|や(もしれない|りも?)?)"
        #         particles_and_or_symbol = rf"(({particles})?[、。！？!?ー─―」』…・）]+|{particles})"
                
        #         if length == 0 and sub.text.endswith(full_name):
                    
        #             found = re.search(fr"^{particles_and_or_symbol}", next_sub.text)
        #             if not found:
        #                 continue
        #             if not found.group():
        #                 continue
        #             print("Particles")
        #             print(file_name)
        #             print(sub.text)
        #             print(next_sub.text) 
        #             print(length, last, without)
        #             print(found.group())
        #             print("\n") 
        #             sub.text = sub.text + next_sub.text[:found.span()[1]] 
        #             next_sub.text = next_sub.text[found.span()[1]:] 
        #             print(sub.text)
        #             print(next_sub.text) 
        #             print(length, last, without)
        #             print("\n") 
        #             print("\n")

        #         elif sub.text.endswith(without) and next_sub.text.startswith(last) and length != 0:
        #             print("Name broken")
        #             if length == 0 and next_sub.text.startswith(full_name):
        #                 continue
        #             found = re.search(fr"^{last}({particles_and_or_symbol})?", next_sub.text)
        #             if not found:
        #                 print(next_sub.text)
        #                 print(fr"^{last}{particles_and_or_symbol}")
        #                 raise IndexError
        #             print(file_name)
        #             print(sub.text)
        #             print(next_sub.text) 
        #             print(length, last, without)
        #             print("\n") 
        #             sub.text = sub.text + next_sub.text[:found.span()[1]] 
        #             next_sub.text = next_sub.text[found.span()[1]:] 
        #             print(sub.text)
        #             print(next_sub.text) 
        #             print(length, last, without)
        #             print("\n") 
        #             print("\n")
                   



        
        if not next_sub.text.strip():
            sub.end = next_sub.end
            next_sub.start = next_sub.end
        fixed_subs.append(sub)
        if next_sub == subs[-1]:
            fixed_subs.append(next_sub)


    # Fix overlaps
    for prev, nxt in zip(fixed_subs, fixed_subs[1:]):
        if nxt.start < prev.end:
            print(f"Fixed overlap of {(prev.end.ordinal - nxt.start.ordinal)}ms ({prev.start})")
            nxt.start = prev.end

    fixed_subs.save(file_name, encoding='utf-8')


def shift_subs(file_name, time_str, offset_ms):
    """
    Shift all subtitles after `time_str` by `offset_ms` milliseconds.
    Example: time_str = "00:01:05"
    """
    subs = pysrt.open(file_name)
    shift_point = pysrt.SubRipTime.from_string(time_str)

    for sub in subs:
        if sub.start > shift_point:
            ...
            sub.start += offset_ms
            sub.end += offset_ms
            # sub.shift(milliseconds=offset_ms)
             
    # Fix overlaps
    for prev, nxt in zip(subs, subs[1:]):
        if nxt.start < prev.end:
            print(f"Fixed overlap of {(prev.end.ordinal - nxt.start.ordinal)}ms ({prev.start})")
            nxt.start = prev.end

    subs.save(file_name, encoding='utf-8')


def process_file(filename):
    full_path = os.path.join("./", filename)
    if os.path.isfile(full_path):
        # print(full_path)
        fix_subs(full_path)



if __name__ == "__main__":
    file_path = '29 - 死物語 下 加藤 英美里.srt'
    HOUR = 3_600_000
    MINUTE = 60_000
    SECOND = 1000
    first = 4 * HOUR + 0 * MINUTE + 19 * SECOND
    # subs = pysrt.open(file_path)
    # s = subs[2954]

    # print(s.index)
    # s.start = pysrt.SubRipTime.from_string("02:33:11,000")
    # s.end = pysrt.SubRipTime.from_string("02:33:12,880")
    # s.text = "００７"
    # subs.insert(2956, s)
        # for i in range(2955, len(subs)):
        # subs[i].index += 1
    # subs.save(file_path, encoding='utf-8')

    # shift_subs(file_path, "00:00:00,000", -1*MINUTE+14*SECOND)

    # split_and_shift_srt(file_path, [first])

    # srt_files = [f for f in os.listdir("./") if f.endswith(".srt")]

    # with ThreadPoolExecutor() as executor:
        # executor.map(process_file, srt_files)
    # 06 - 偽物語 下 坂本 真綾.srt
    # files = [x for x in os.listdir("./") if x.endswith(".srt")]
    # file_amount = len(files)
    # for i, filename in enumerate(files):
    #     if filename.endswith(".srt"): 
    #         full_path = os.path.join("./", filename)
    #         if os.path.isfile(full_path): 
    #             # a = re.search(r"\d\d - (.+?(?: [下中上])?) ", full_path)
    #             # if a:
    #             #     print(f"\"{a.groups(1)[0]}\"", end=", ")
    #             fix_subs(full_path)
    #             print(f"Finished [{round(100*(i+1)/file_amount, 2)}%]")