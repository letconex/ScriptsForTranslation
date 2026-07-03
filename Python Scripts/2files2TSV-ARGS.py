import sys
#  print("Usage: 2files2TSVwithARGS,.py source_language_file target_language_file resulting_TSV_file")
f = open(str(sys.argv[3]), 'w', encoding='utf-8')
with open(str(sys.argv[1]), 'r', encoding='utf-8') as f1, open(str(sys.argv[2]), 'r', encoding='utf-8') as f2:
  for x, y in zip(f1, f2):
     f.write("{0}\t{1}\n".format(x.strip(), y.strip()))
f.close
