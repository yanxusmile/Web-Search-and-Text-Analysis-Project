# General Python libraries
import logging

# Gensim libraries
from gensim import corpora, models, similarities

# Local libraries
import index

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', 
        level=logging.INFO)

def lsi_for_idx(index_tag, num_topics=100):
    dict_ = corpora.Dictionary.load(index.get_dict_fname(index_tag))
    corpus_raw = corpora.MmCorpus(index.get_corpus_fname(index_tag))
    corpus = models.TfidfModel.load(index.get_tfidf_fname(index_tag))

    lsi = models.LsiModel(corpus, id2word=dict_, num_topics=num_topics)
    return (lsi, dict_)

if __name__ == '__main__':

    import sys

    if len(sys.argv) != 4:
        sys.stderr.write("USAGE: %s <index-tag> <ntpcs> <nwords>\n" % (sys.argv[0]))
        sys.exit(1)

    index_tag = sys.argv[1]
    ntpcs = int(sys.argv[2])
    nwords = int(sys.argv[2])

    (lsi, dict_) = lsi_for_idx(index_tag, ntpcs)
    corpus_lsi = lsi[corpus]

    #lsi.print_topics(num_topics=10, num_words=20)
    tnum = 0
    for tpc in lsi.show_topics(num_topics=ntpcs, num_words=nwords):
        print ">>> Topic %d" % (tnum)
        print tpc
        print
        tnum += 1
