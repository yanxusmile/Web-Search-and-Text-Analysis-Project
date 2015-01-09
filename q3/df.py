def calc_df(coll):
    """Calculate DF of each term in vocab and return as term:df dictionary."""
    df_ = {}
    for doc in coll:
        for term in doc.get_term_list():
            try:
                df_[term] += 1
            except KeyError:
                df_[term] = 1
    return df_

if __name__ == '__main__':

    import sys
    import coll

    if len(sys.argv) != 2:
        sys.stderr.write("USAGE: %s <coll-file>\n" % sys.argv[0])
        sys.exit()
    coll_ = coll.parse_lyrl_coll(sys.argv[1])

    df_ = calc_df(coll_)
    for (term, df_) in iter(sorted(df_.iteritems())):
        print "%s: %d" % (term, df_)
