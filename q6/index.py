from gensim import corpora, models

def lyrl_to_docs(coll_fname):
    """Convert wiki into the GenSim texts representation.
    
    The representation is very simple: a list of documents, where
    the documents are lists of terms.  We return (docids, docs), 
    where docids gives the ids of the documents."""
    docs = []
    docids = []
    for line in open(coll_fname):
        line = line.strip().split()
        docids.append(line[0])
        wc = {}
        for word in line[1:]:
            wc[word] = wc.get(word,0) + 1
        fw = [w for w, c in wc.items() if c>1]
        docs.append(fw)
    return (docids, docs)

def save_docids(docids, fname):
    """Save docids to file."""
    fp = open(fname, 'w')
    docnum = 0
    for docid in docids:
        fp.write("%s %d\n" % (docid, docnum))
        docnum += 1
    fp.close()

def load_docids(fname):
    """Load docids from file."""
    fp = open(fname, 'r')
    docs = []
    for line in fp:
        (docid, docnum_s) = line.split()
        docnum = int(docnum_s)
        while len(docs) < (docnum - 1):
            docs.append(None)
        docs.append(docid)
    fp.close()
    return docs

def get_docinfo_fname(tag):
    return "%s.docinfo.db" % (tag)

def get_dict_fname(tag):
    return "%s.dict.db" % (tag)

def get_corpus_fname(tag):
    return "%s.corp.db" % (tag)

def get_tfidf_fname(tag):
    return "%s.corp.tfidf.db" % (tag)

def get_lsi_fname(tag, ntpcs):
    return "%s.corp.lsi.t%d.db" % (tag, ntpcs)

def get_lsi_index_fname(tag, ntpcs):
    return "%s.corp.lsi.idx.t%d.db" % (tag, ntpcs)

def make_index(coll_fname, index_tag):
    """Create a GenSim index of wiki.

    The index is contained in files whose names begin with
    index_tag.  index_tag may contain directories components,
    but the specified directories must already exist."""

    (docids, docs) = lyrl_to_docs(coll_fname)

    docinfo_fname = get_docinfo_fname(index_tag)
    dict_fname = get_dict_fname(index_tag)
    corpus_fname = get_corpus_fname(index_tag)
    tfidf_fname = get_tfidf_fname(index_tag)

    save_docids(docids, docinfo_fname)

    dict_ = corpora.Dictionary(docs)
    dict_.save(dict_fname)

    corpus = [ dict_.doc2bow(doc) for doc in docs ]
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    corpora.MmCorpus.serialize(corpus_fname, corpus)
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    corpus_tfidf.save(tfidf_fname)

if __name__ == '__main__':
    
    import sys

    if len(sys.argv) != 3:
        sys.stderr.write("USAGE: %s <wiki-fname> <index-tag>\n" % (sys.argv[0]))
        sys.exit(1)

    lyrl_fname = sys.argv[1]
    index_tag = sys.argv[2]
    make_index(lyrl_fname, index_tag)
