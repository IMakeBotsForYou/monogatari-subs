import os
import pysrt
from re import compile

subfolder = "original"
def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Compute the Levenshtein distance between two strings.
    This is the minimum number of single-character edits
    (insertions, deletions, substitutions) required to
    change s1 into s2.
    """
    len_s1, len_s2 = len(s1), len(s2)
    
    # Create a matrix (len_s1+1) x (len_s2+1)
    dp = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]
    
    # Initialize the base cases
    for i in range(len_s1 + 1):
        dp[i][0] = i
    for j in range(len_s2 + 1):
        dp[0][j] = j
    
    # Fill the matrix
    for i in range(1, len_s1 + 1):
        for j in range(1, len_s2 + 1):
            cost = 0 if s1[i-1] == s2[j-1] else 1
            dp[i][j] = min(
                dp[i-1][j] + 1,    # Deletion
                dp[i][j-1] + 1,    # Insertion
                dp[i-1][j-1] + cost  # Substitution
            )
    
    return dp[len_s1][len_s2]

for filename in os.listdir("."):
    if filename.endswith(".srt") and os.path.isfile(filename):
        prefix = filename.split(" ")[0]

        # Find the matching subfolder file
        subfile = None
        for f in os.listdir(subfolder):
            if f.startswith(prefix) and f.endswith(".srt"):
                subfile = os.path.join(subfolder, f)
                break

        if not subfile:
            print(f"No matching subfolder file for {filename}")
            continue

        # Load SRT files
        main_srt = pysrt.open(filename, encoding="utf-8")
        sub_srt = pysrt.open(subfile, encoding="utf-8")

        # Get last subtitle text of main file
        # last_text = main_srt[-1].text.strip()

        # Find the index in sub_srt starting from the end (skip ~30-40 lines)
        start_search = 0
        match_index = None
        original_lines = []
        # ([^─\d…○！？×まつい])\1$
        # found  = re.search(r"、[^と]$", sub.text)
        pattern = compile(r"、[^と。！？」]$")

        for i in range(0, len(main_srt)):
            if pattern.search(main_srt[i].text):
                # print(filename)
                # print(main_srt[i].text)
                original_lines.append((main_srt[i].text, i))

            # if jaccard_similarity(main_srt[i].text.strip(), last_text) > 0.9:
            #     match_index = i
            #     break

        # Append remaining subtitles from sub_srt to main_srt
        search_lines = [] 
        for original_line in original_lines:
            search_lines.append((original_line[0], original_line[1], [x for x in range(original_line[1]-10, original_line[1]+10)]))

        for original_line_text, original_line_number, search_range in search_lines:
            for line in search_range:
                if levenshtein_distance(main_srt[original_line_number].text, sub_srt[line].text) < 3 and main_srt[original_line_number].text != sub_srt[line].text:
                    print(filename)
                    print(main_srt[original_line_number-1].text)
                    print(main_srt[original_line_number].text)
                    print(main_srt[original_line_number+1].text)
                    print()
                    print(sub_srt[line].text)
                    print(sub_srt[line+1].text)
                    print()
                    print()
                    inp = input("Remove or add last char? Add: 1, Save: 2, Remove: else  >  ")
                    if inp == "1":
                        main_srt[original_line_number+1].text = main_srt[original_line_number].text[-1] + main_srt[original_line_number+1].text
                        main_srt[original_line_number].text = main_srt[original_line_number].text[:-1]
                    elif inp == "2":
                        ...
                    else:
                        main_srt[original_line_number].text = main_srt[original_line_number].text[:-1]
                    
                    print(main_srt[original_line_number].text)
                    print(main_srt[original_line_number+1].text)
                    print()
                    print()

        
        # # Save main file
        main_srt.save(filename, encoding="utf-8")
        # print(f"Appended {len(sub_srt) - match_index - 1} subtitles from {subfile} to {filename}")
