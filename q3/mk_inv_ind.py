import shelve
import df
import tfidf

def mk_inv_ind(coll_, filename, s):
    """Make inverted index of a collection in a filename.
    Perform the inversion in memory; then write the term
    posting lists out to file
    tfidf_norm[term] = ti / ((1-s)*len_mean + s*len_doc)
    """
    inv_idx = {}
    len_dict = {}
    len_mean = 0
    df_ = df.calc_df(coll_)
    for doc in coll_:
        tfidf_, len_ = tfidf.tfidf(doc, df_, coll_.get_num_docs())
        len_dict[doc.get_docid()] = len_
        len_mean += len_
        for (term, weight) in tfidf_.iteritems():
            try:
                inv_idx[term][doc.get_docid()] = weight
            except KeyError:
                inv_idx[term] = { doc.get_docid() : weight }

    len_mean = len_mean / float(coll_.get_num_docs())
    # print len_mean, float(s)
    for term in inv_idx.keys():
        for doc, tfidf_ in inv_idx[term].items():
            inv_idx[term][doc] = tfidf_ / ((1-float(s))*len_mean + float(s)*len_dict[doc])

    index = shelve.open(filename)
    for (term, postings) in inv_idx.iteritems():
        index[term] = postings
    index.close()

if __name__ == '__main__':

    import coll
    import sys

    if len(sys.argv) != 4:
        sys.stderr.write("USAGE: %s <coll-file> <db-file> <s>\n" % sys.argv[0])
        sys.exit()
    coll_ = coll.parse_lyrl_coll(sys.argv[1])
    mk_inv_ind(coll_, sys.argv[2], sys.argv[3])
