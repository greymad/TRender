import inspect
import os
from pathlib import Path
import imgaug.augmenters as iaa

from text_renderer.effect import *
from text_renderer.corpus import *
from text_renderer.config import (
    RenderCfg,
    NormPerspectiveTransformCfg,
    GeneratorCfg,
    FixedTextColorCfg,
    BlackColorCFG
)
from text_renderer.layout.same_line import SameLineLayout
from text_renderer.layout.extra_text_line import ExtraTextLineLayout


CURRENT_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
OUT_DIR = CURRENT_DIR / "random_output"
DATA_DIR = CURRENT_DIR
BG_DIR = DATA_DIR / "bg"
CHAR_DIR = DATA_DIR / "char"
FONT_DIR = DATA_DIR / "font"
FONT_LIST_DIR = DATA_DIR / "font_list"
TEXT_DIR = DATA_DIR / "text"

font_cfg = dict(
    font_dir=FONT_DIR,
    font_list_file=FONT_LIST_DIR / "fonts.txt",
    font_size=(14, 30),
)

perspective_transform = NormPerspectiveTransformCfg(20, 20, 1.5)


def get_char_corpus():
    return CharCorpus(
        CharCorpusCfg(
            text_paths=[TEXT_DIR / "finance.txt"],
            filter_by_chars=False,
            chars_file=CHAR_DIR / "turkish.txt",
            length=(3, 25),
            char_spacing=(-0.3, 1.3),
            **font_cfg
        ),
    )


def base_cfg(
    name: str, corpus, corpus_effects=None, layout_effects=None, layout=None, gray=True
):
    return GeneratorCfg(
        num_image=2000000,
        save_dir=OUT_DIR / name,
        
        render_cfg=RenderCfg(
            bg_dir=BG_DIR,
            height = 32,
            perspective_transform=perspective_transform,
            gray=gray,
            layout_effects=layout_effects,
            layout=layout,
            corpus=corpus,
            corpus_effects=corpus_effects,
        ),
    )




def enum_data():
    return base_cfg(
        inspect.currentframe().f_code.co_name,
        corpus=EnumCorpus(
            EnumCorpusCfg(
                text_paths=[TEXT_DIR / "finance.txt"],
                filter_by_chars=True,
                chars_file=CHAR_DIR / "turkish.txt",
                **font_cfg
            ),
        ),
    )


def rand_data():
    print("RAND DATA \n")
    return base_cfg(
        inspect.currentframe().f_code.co_name,
        corpus=RandCorpus(
            RandCorpusCfg(chars_file=CHAR_DIR / "turkish.txt", **font_cfg),
        ),
    )


def eng_word_data():
    print("ENG DATA \n")
    return base_cfg(
        inspect.currentframe().f_code.co_name,
        corpus=WordCorpus(
            WordCorpusCfg(
                text_paths=[TEXT_DIR / "articles_cleaned4.txt"],
                filter_by_chars=False,
                chars_file=CHAR_DIR / "turkish.txt",
                **font_cfg
            ),
        ),
        corpus_effects=Effects([DropoutVertical( p = 0.2,num_line = 5, thickness=1), DropoutHorizontal(p=0.2, num_line=1, thickness = 1),DropoutRand()]),
    )

def test_word_data():
    return base_cfg(
        inspect.currentframe().f_code.co_name,
        corpus=WordCorpus(
            WordCorpusCfg(
                text_paths=[TEXT_DIR / "articles_cleaned4.txt"],
                filter_by_chars=False,
                chars_file=CHAR_DIR / "turkish.txt",
                **font_cfg
            ),
        ),
         corpus_effects=Effects([DropoutVertical( p = 0.2,num_line = 5, thickness=1), DropoutHorizontal(p=0.2, num_line=1, thickness = 1),DropoutRand()]),
    )
          
    
def same_line_data():
    print("SAME DATA \n")
    return base_cfg(
        inspect.currentframe().f_code.co_name,
        layout=SameLineLayout(),
        gray=True,
        corpus=[
            
            CharCorpus(
                CharCorpusCfg(
                    text_paths=[
                        TEXT_DIR / "finance.txt"
                        
                    ],
                    filter_by_chars=True,
                    chars_file=CHAR_DIR / "turkish.txt",
                    length=(4, 15),
                    font_dir=font_cfg["font_dir"],
                    font_list_file=font_cfg["font_list_file"],
                    font_size=(15, 35),
                ),
            ),
        ],
        corpus_effects=Effects([DropoutVertical(thickness=2), DropoutHorizontal(thickness=2),DropoutRand()]),
        layout_effects=Effects(Line(p=1)),
    )


def extra_text_line_data():
    print("EXTRA DATA \n")
    return base_cfg(
        inspect.currentframe().f_code.co_name,
        layout=ExtraTextLineLayout(),
        corpus=[
            CharCorpus(
                CharCorpusCfg(
                    text_paths=[
                        TEXT_DIR / "finance.txt"
                        
                    ],
                    filter_by_chars=True,
                    chars_file=CHAR_DIR / "turkish.txt",
                    length=(4, 15),
                    font_dir=font_cfg["font_dir"],
                    font_list_file=font_cfg["font_list_file"],
                    font_size=(15, 35),
                ),
            ),
            CharCorpus(
                CharCorpusCfg(
                    text_paths=[
                        TEXT_DIR / "finance.txt",
                        TEXT_DIR / "finance.txt",
                    ],
                    filter_by_chars=True,
                    chars_file=CHAR_DIR / "turkish.txt",
                    length=(4, 10),
                    font_dir=font_cfg["font_dir"],
                    font_list_file=font_cfg["font_list_file"],
                    font_size=(15, 35),
                ),
            ),
        ],
        #corpus_effects=Effects([Padding(),NoEffects()]),
        layout_effects=Effects(Line(p=1)),
    )


def imgaug_emboss_example():
    return base_cfg(
        inspect.currentframe().f_code.co_name,
        corpus=get_char_corpus(),
        corpus_effects=Effects(
            [
                ImgAugEffect(aug=iaa.Emboss(alpha=(0.9, 1.0), strength=(1.5, 1.6))),
            ]
        ),
    )


# fmt: off
# The configuration file must have a configs variable
configs = [
    #rand_data(),
    test_word_data(),
    #eng_word_data(),
    #eng_word_data2()
    #same_line_data(),
    #extra_text_line_data()
    #imgaug_emboss_example()
]
# fmt: on
