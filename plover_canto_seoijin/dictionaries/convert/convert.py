import json
import re
import sys


def add_v(chord):
    last_chord = chord.split("/")[-1]
    last_chord = re.sub(r"([AOEU-]+)", r"\1V", last_chord)
    chord = "/".join([*chord.split("/")[:-1]]+[last_chord])
    return chord


in_file = sys.argv[1]

with open("j2s.json", "r") as f:
    j2s = json.load(f)

with open(in_file, "r") as f:
    data = json.load(f)

out_dict = []

# For each homophone set
for jp, hz in data.items():
    chord = "/".join([j2s[syl] for syl in jp.split()])
    # For each honzi variant
    for i, word in enumerate(hz.split()):
        #print(f"{i} {jp} {chord} {word}")
        v_keys = ["", "-V", "-VP", "-VT", "-VY", "-VG", "-VH", "-VS"]
        if i == 0:
            out_dict.append((chord, word)) 
        elif i == 1:
            chord_v = add_v(chord)
            chord_vi = f"{chord}/{v_keys[i]}"
            out_dict.append((chord_v, word))
            out_dict.append((chord_vi, word))
        else:
            chord_vi = f"{chord}/{v_keys[i]}"
            chord_vii = f"{chord}{'/-V'*i}"
            out_dict.append((chord_vi, word))
            out_dict.append((chord_vii, word))

print("{")
for i, (k, v) in enumerate(out_dict):
    if i != len(out_dict)-1:
        print(f"\"{k}\": \"{{&{v}}}\",")
    else:
        print(f"\"{k}\": \"{{&{v}}}\"")
print("}")


