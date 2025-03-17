from text_normalization import text_normalize
from tc_utils import get_uroman_tokens


t_path='/home/mendo/Downloads/LM/LM-5/LM-TTS-Main/ztext_cleaner/text.txt'
uroman_path=''
lang=''

with open(t_path,'r') as f:
    transcripts = [line.strip() for line in f]
print("Read {} lines from {}".format(len(transcripts), t_path))

norm_transcripts = [text_normalize(line.strip(),'ksf') for line in transcripts]

tokens = get_uroman_tokens(norm_transcripts, uroman_path, lang)


print('Normalize texte:\n')
for t in norm_transcripts[:5]:
    print(t)