import math
import df

def tfidf(doc, df, ndocs):
    tfidf_ = {}
    len_sq = 0
    for (term, freq) in doc:
        ti = math.log(1 + freq) * math.log(float(ndocs) / df[term])
        len_sq += ti ** 2
        tfidf_[term] = ti
    len_ = math.sqrt(len_sq)
    # if norm:
    #     tfidf_norm = {}
    #     for (term, ti) in tfidf_.iteritems():
    #         tfidf_norm[term] = ti / ((1-s)*len_mean + s*len_doc)
    #     return tfidf_norm
    # else:
    return tfidf_, len_

if __name__ == "__main__":

    import sys
    import coll

    if len(sys.argv) != 3:
        sys.stderr.write("USAGE: %s <coll-file> <docid>\n" % sys.argv[0])
        sys.exit()
    coll_fname = sys.argv[1]
    docid = sys.argv[2]
    coll_ = coll.parse_lyrl_coll(coll_fname)
    df_ = df.calc_df(coll_)
    doc = coll_.get_doc(docid)
    tfidf_ = tfidf(doc, df_, coll_.get_num_docs())

    len_ = 0
    for (term, score) in sorted(tfidf_.items()):
        len_ += score ** 2
        print "%s: %f" % (term, score)
    print "TOTAL LENGTH: %f" % len_
