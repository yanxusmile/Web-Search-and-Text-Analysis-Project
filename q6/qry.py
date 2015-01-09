import lsa
import index
# import re
from gensim import corpora, models, similarities


def filter_res(qry, res, fname, docs):
	"""filter the results to make sure the components of mailing list domain occur in the results documents"""
	wiki_dict = {}
	for line in open(fname):
		line = line.strip().lower().split()
		wiki_dict[line[0]] = line
	filtered_res = []
	for doc, score in res:
		# print docs[doc]
		pj = qry[0].lower().split('.')
		c = 1
		for term in pj[:2]:
			if term not in wiki_dict[docs[doc].lower()]:
				c = 0
		if c:
			filtered_res.append((doc, score))
	return filtered_res


if __name__ == '__main__':

	import sys

	if len(sys.argv) != 5:
		sys.stderr.write("USAGE: %s <index-tag> <ntpcs> <nres> <wiki-file>\n" % (sys.argv[0]))
		sys.exit(1)

	index_tag = sys.argv[1]
	ntpcs = int(sys.argv[2])
	nres = int(sys.argv[3])

	lsi = models.LsiModel.load(index.get_lsi_fname(index_tag, ntpcs))
	dict_ = corpora.Dictionary.load(index.get_dict_fname(index_tag))
	docs = index.load_docids(index.get_docinfo_fname(index_tag))

	index = similarities.MatrixSimilarity.load(index.get_lsi_index_fname(index_tag, ntpcs))


	for qry in sys.stdin:
		qry_raw = qry.strip()
		qry = qry_raw.strip().lower().split()
		pj = qry[0].split('.')
		if len(pj)>1:
			# add components of mailing list domain to qry 
			qry.extend([pj[0]]*5+[pj[1]]*5)
		# print qry
		qry_bow = dict_.doc2bow(qry)		
		qry_lsi = lsi[qry_bow]
		res = list(enumerate(index[qry_lsi]))
		res = sorted(res, key=lambda item: -item[1])
		res = filter_res(qry, res, sys.argv[4], docs)
		print "\n>> '%s'" % qry_raw
		for (docnum, score) in res[0:nres]:
			docid = docs[docnum]
			print "%s %.3f" % (docid, score)

