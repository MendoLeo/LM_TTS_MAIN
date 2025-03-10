import re
import string

from unidecode import unidecode
from num2words import num2words
import unicodedata

import torch
import torchaudio.functional as F

#########################################################
# MMS feature extractor minimum input frame size (25ms)
# also the same value as `ratio`
# `ratio = input_waveform.size(1) / num_frames`
#########################################################

MMS_SUBSAMPLING_RATIO = 400

###################
# text utils
###################


def preprocess_verse(text: str) -> str:
    text = unidecode(text)
    text = unicodedata.normalize('NFKC', text)
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub("\s+", " ", text)
    return text


###############################################################################################################
# functions modified from https://pytorch.org/audio/main/tutorials/ctc_forced_alignment_api_tutorial.html
###############################################################################################################


def align(emission, tokens, device):
    targets = torch.tensor([tokens], dtype=torch.int32, device=device)
    alignments, scores = F.forced_align(emission, targets, blank=0)

    alignments, scores = alignments[0], scores[0]  # remove batch dimension for simplicity
    scores = scores.exp()  # convert back to probability
    return alignments, scores


def unflatten(list_, lengths):
    assert len(list_) == sum(lengths)
    i = 0
    ret = []
    for l in lengths:
        ret.append(list_[i : i + l])
        i += l
    return ret


def compute_alignments(emission, transcript, dictionary, device):
    tokens = [dictionary[char] for word in transcript for char in word]
    alignment, scores = align(emission, tokens, device)
    token_spans = F.merge_tokens(alignment, scores)
    word_spans = unflatten(token_spans, [len(word) for word in transcript])
    return word_spans


def compute_alignment_scores(emission, transcript, dictionary, device):
    tokens = [dictionary[char] for word in transcript for char in word]

    try:
        _, scores = align(emission, tokens, device)
        return scores
    except RuntimeError as e:
        # sometimes emission frames are too short for the transcript
        # comparing emission shape and targets length is insufficient due to CTC padding
        if e.args[0].startswith("targets length is too long for CTC"):
            # return 0 probability for this case
            return torch.zeros((1, emission.size(1)), device=device)
        else:
            raise e
