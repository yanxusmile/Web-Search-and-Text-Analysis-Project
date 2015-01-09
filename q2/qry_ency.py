import math
import shelve

def do_qry_inv_ind(qry_s, idx_file):
	"""query on the inverted index"""
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
	index.close()
	score_doc = [ (score, doc) for (doc, score) in accumulators.items() ]
	return sorted(score_doc)[::-1]

if __name__ == '__main__':

	import shelve
	import sys

	if len(sys.argv) != 3:
		sys.stderr.write("USAGE: %s <db-file> <no.results> \"<qry>\"\n" % sys.argv[0])
		sys.exit()

	for line in sys.stdin:
		qry = line.strip()
		print '\n>> %s' %qry
		score_doc = do_qry_inv_ind(qry, sys.argv[1])
		for sim, docid in score_doc[:int(sys.argv[2])]:
			print '%s %f' %(docid, sim)
