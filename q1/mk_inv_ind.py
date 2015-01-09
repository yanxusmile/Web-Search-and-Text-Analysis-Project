import shelve
import df
import tfidf

def mk_inv_ind(coll_, filename, norm=True):
    """Make inverted index of a collection in a filename."""

    # Perform the inversion in memory; then write the term
    # posting lists out to file
    inv_idx = {}
    df_ = df.calc_df(coll_)
    for doc in coll_:
        tfidf_ = tfidf.tfidf(doc, df_, coll_.get_num_docs(), norm=True)
        for (term, weight) in tfidf_.iteritems():
            try:
                inv_idx[term][doc.get_docid()] = weight
            except KeyError:
                inv_idx[term] = { doc.get_docid() : weight }
    index = shelve.open(filename)
    for (term, postings) in inv_idx.iteritems():
        index[term] = postings
    index.close()

if __name__ == '__main__':

    import coll
    import sys

    if len(sys.argv) != 3:
        sys.stderr.write("USAGE: %s <coll-file> <db-file>\n" % sys.argv[0])
        sys.exit()
    coll_ = coll.parse_lyrl_coll(sys.argv[1])
    mk_inv_ind(coll_, sys.argv[2], norm=True)
