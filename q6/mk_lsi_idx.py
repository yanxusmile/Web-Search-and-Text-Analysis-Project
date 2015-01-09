from gensim import models, similarities
import lsa
import index

if __name__ == '__main__':

    import sys

    if len(sys.argv) != 3:
        sys.stderr.write("USAGE: %s <index-tag> <ntpcs>\n" % (sys.argv[0]))
        sys.exit(1)

    index_tag = sys.argv[1]
    ntpcs = int(sys.argv[2])

    (lsi, dict_) = lsa.lsi_for_idx(index_tag, ntpcs)
    corpus = models.TfidfModel.load(index.get_tfidf_fname(index_tag))
    index_ = similarities.MatrixSimilarity(lsi[corpus])
     
    lsi_fname = index.get_lsi_fname(index_tag, ntpcs)
    lsi.save(lsi_fname)
    lsi_index_fname = index.get_lsi_index_fname(index_tag, ntpcs)
    index_.save(lsi_index_fname)
