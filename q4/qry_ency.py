import math
import shelve

def do_qry_inv_ind(qry_s, idx_file, mode):
	"""query on the inverted index"""
	mode = int(mode)
	qry_terms = qry_s.split()
	qry_vec = {}
	for qt in qry_terms:
		try:
			qry_vec[qt] += 1
		except KeyError:
			qry_vec[qt] = 1

	for qt, f_qt in qry_vec.items():
		qry_vec[qt] = math.log(1 + f_qt)

	accumulators = {}
	index = shelve.open(idx_file, 'r')
	for (qt, w_qt) in qry_vec.items():
		if qt in index:
			postings = index[qt]
			for (doc, w_dt) in postings.items():
				try:
					accumulators[doc] += w_qt * w_dt
				except KeyError:
					accumulators[doc] = w_qt * w_dt
	score_doc = [ (score, doc) for (doc, score) in accumulators.items() ]
	sorted_doc_socre = sorted(score_doc)[::-1]
	
	if mode == 0:
		index.close()
		return sorted_doc_socre
	else:
		new_sorted_doc_socre = []
		for score, doc in sorted_doc_socre:
			c = 1
			for term in qry_vec.keys():
				if doc not in index[term].keys():
					c = 0
					break
			if c == 1:
				new_sorted_doc_socre.append((score,doc))
		index.close()
		return new_sorted_doc_socre



if __name__ == '__main__':

	import shelve
	import sys

	if len(sys.argv) != 4:
		sys.stderr.write("USAGE: %s <db-file> <no.results> <mode 0 or 1> \"<qry>\"\n" % sys.argv[0])
		sys.exit()

	for line in sys.stdin:
		qry = line.strip()
		print '\n>> %s' %qry
		score_doc = do_qry_inv_ind(qry, sys.argv[1], sys.argv[3])
		# print len(score_doc)
		for sim, docid in score_doc[:int(sys.argv[2])]:
			print '%s %f' %(docid, sim)
