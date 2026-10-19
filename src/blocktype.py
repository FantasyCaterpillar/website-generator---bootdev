from enum import Enum

class BlockType(Enum):
    paragraph = 1
    heading = 2
    code = 3
    quote = 4
    unordered_list = 5
    ordered_list = 6

def block_to_block_type(text):
    if text.startswith('# ') or text.startswith('## ') or text.startswith('### ') or text.startswith('#### ') or text.startswith('##### ') or text.startswith('###### '):
        return BlockType.heading

    elif text.startswith("```\n") and text.endswith("```"):
        return BlockType.code

    elif text.startswith(">") or text.startswith("> "):
        lines = text.split('\n')
        for i in range(0, len(lines)):
            if not (lines[i].startswith('> ') or lines[i].startswith('>')):
                return BlockType.paragraph
        return BlockType.quote

    elif text.startswith("- "):
        lines = text.split('\n')
        for i in range(0, len(lines)):
            if not lines[i].startswith('- '):
                return('block is not an unordered list')
        return BlockType.unordered_list

    elif text.startswith('1. '):
        lines = text.split('\n')
        for i in range(0, len(lines)):
            if not lines[i].startswith(f'{i+1}. '):
                return('block is not an ordered list')
        return BlockType.ordered_list

    else:
        return BlockType.paragraph

