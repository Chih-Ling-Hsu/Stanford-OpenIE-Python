
from nltk.tokenize import TweetTokenizer
import utils.OpenIE.main as mst
import os
import random
import time
import shutil

class OpenIEExtractor():
    def __init__(self, root='/tmp/openie/'):
        self.root = root
        if not os.path.exists(self.root):
            os.makedirs(self.root)
        #self.tokenizer = TweetTokenizer(preserve_case=True, reduce_len=False, strip_handles=False)
    
    '''
    Pre-processing that are required before openIE:
    - remove `$` in cashtags
    - remove URLs
    '''
    def text_preprocess(self, line):
        words = line.split()#self.tokenizer.tokenize(line)
        words = list(filter(lambda w: (w.startswith('http')==False) & (w.startswith('www.')==False) & (w!='$'), words))
        line =  ' '.join(words)
        line = line.replace('$', '')

        if line.endswith('.') or line.endswith('!') or line.endswith('?'):
            return line
        else:
            return line + '.'
    
    def prepare(self, grp, out_folder):
        lines = []
        with open(os.path.join(out_folder, 'input.txt'), 'w') as f:
            for post in grp:
                line = self.text_preprocess(post)            
                lines.append(line)
            f.write('\n'.join(lines))
        return lines
    
    def extract_relations(self, data):
        # Prepare folder
        out_folder = os.path.join(self.root, '{}_{}'.format(time.time(), random.randint(0, 1000000)))
        if not os.path.exists(out_folder):
            os.makedirs(out_folder)    

        # Run OpenIE
        _ = self.prepare(data, out_folder)
        relations = mst.stanford_ie(os.path.join(out_folder, 'input.txt'), 
                                          out_folder, verbose=False)

        # Remove folder
        shutil.rmtree(mst.tmp_folder)
        return relations
