class BowDoc:
    """Bag-of-words representation of a document.

    The document has an ID, and an iterable list of terms with their
    frequencies."""

    def __init__(self, docid):
        """Constructor.

        Set the ID of the document, and initiate an empty term dictionary.
        Call add_term to add terms to the dictionary."""
        self.docid = docid
        self.terms = {} 

    def add_term(self, term):
        """Add a term occurrence to the BOW representation.

        This should be called each time the term occurs in the document."""
        try:
            self.terms[term] += 1
        except KeyError:  
            self.terms[term] = 1

    def get_term_count(self, term):
        """Get the term occurrence count for a term.

        Returns 0 if the term does not appear in the document."""
        try:
            return self.terms[term]
        except KeyError:
            return 0

    def get_term_freq_dict(self):
        """Return dictionary of term:freq pairs."""
        return self.terms

    def get_term_list(self):
        """Get sorted list of all terms occurring in the document."""
        return sorted(self.terms.keys())

    def get_docid(self):
        """Get the ID of the document."""
        return self.docid

    def __iter__(self):
        """Return an ordered iterator over term--frequency pairs.

        Each element is a (term, frequency) tuple.  They are iterated
        in alphabetical order."""
        return iter(sorted(self.terms.iteritems()))


class BowColl:
    """Collection of BOW documents."""

    def __init__(self):
        """Constructor.

        Creates an empty collection."""
        self.docs = {}

    def add_doc(self, doc):
        """Add a document to the collection."""
        self.docs[doc.get_docid()] = doc

    def get_doc(self, docid):
        """Return a document by docid.

        Will raise a KeyError if there is no document with that ID."""
        return self.docs[docid]

    def get_docs(self):
        """Get the full list of documents.

        Returns a dictionary, with docids as keys, and docs as values."""
        return self.docs

    def inorder_iter(self):
        """Return an ordered iterator over the documents.
        
        The iterator will traverse the collection in docid order.  Modifying
        the collection while iterating over it leads to undefined results.
        Each element is a document; to find the id, call doc.get_docid()."""
        return BowCollInorderIterator(self)

    def get_num_docs(self):
        """Get the number of documents in the collection."""
        return len(self.docs)

    def __iter__(self):
        """Iterator interface.

        See inorder_iter."""
        return self.inorder_iter()

class BowCollInorderIterator:
    """Iterator over a collection."""

    def __init__(self, coll):
        """Constructor.
        
        Takes the collection we're going to iterator over as sole argument."""
        self.coll = coll
        self.keys = sorted(coll.get_docs().keys())
        self.i = 0

    def __iter__(self):
        """Iterator interface."""
        return self

    def next(self):
        """Get next element."""
        if self.i >= len(self.keys):
            raise StopIteration
        doc = self.coll.get_doc(self.keys[self.i])
        self.i += 1
        return doc

def parse_lyrl_coll(fname):
    """Parse an LYRL data file into a collection.

    Fname is the file name of the LYRL data file.  The parsed collection
    is returned.  NOTE the function performs very limited error checking."""
    coll = BowColl()
    curr_doc = None
    for line in open(fname):
        terms = line.strip().split()
        curr_doc = BowDoc(terms[0])
        for term in terms[1:]:
            # print term
            curr_doc.add_term(term)
        # print curr_doc
        coll.add_doc(curr_doc)
        curr_doc = None
    return coll

if __name__ == '__main__':

    import sys

    if len(sys.argv) != 2:
        sys.stderr.write("USAGE: %s <coll-file>\n" % sys.argv[0])
        sys.exit()
    coll = parse_lyrl_coll(sys.argv[1])

    for doc in coll:
        print ".D %s" % doc.get_docid()
        for (term, freq) in doc:
            print "%s:%d" % (term, freq) 
        print "\n"
