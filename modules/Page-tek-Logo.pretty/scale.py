import re

""" from https://rosettacode.org/wiki/S-Expressions#Python """
dbg = False
 
term_regex = r'''(?mx)
    \s*(?:
        (?P<brackl>\()|
        (?P<brackr>\))|
        (?P<num>\-?\d+\.\d+|\-?\d+)|
        (?P<sq>"[^"]*")|
        (?P<s>[^(^)\s]+)
       )'''
 
def parse_sexp(sexp):
    stack = []
    out = []
    if dbg: print("%-6s %-14s %-44s %-s" % tuple("term value out stack".split()))
    for termtypes in re.finditer(term_regex, sexp):
        term, value = [(t,v) for t,v in termtypes.groupdict().items() if v][0]
        if dbg: print("%-7s %-14s %-44r %-r" % (term, value, out, stack))
        if   term == 'brackl':
            stack.append(out)
            out = []
        elif term == 'brackr':
            assert stack, "Trouble with nesting of brackets"
            tmpout, out = out, stack.pop(-1)
            out.append(tmpout)
        elif term == 'num':
            v = float(value)
            if v.is_integer(): v = int(v)
            out.append(v)
        elif term == 'sq':
            out.append(value[1:-1])
        elif term == 's':
            out.append(value)
        else:
            raise NotImplementedError("Error: %r" % (term, value))
    assert not stack, "Trouble with nesting of brackets"
    return out[0]
 
def print_sexp(exp):
    out = ''
    if type(exp) == type([]):
        out += '(' + ' '.join(print_sexp(x) for x in exp) + ')'
    elif type(exp) == type('') and re.search(r'[\s()]', exp):
        out += '"%s"' % repr(exp)[1:-1].replace('"', '\"')
    else:
        out += '%s' % exp
    return out
 
 
if __name__ == '__main__':
    input_file = 'logo'
    silk_size = 7

    fp = open(input_file+'.kicad_mod', 'r')
    input_str = fp.read()
    fp.close()

    parsed = parse_sexp(input_str)
    
    # run through to find size
    min_x = 999.0
    max_x = -999.0
    min_y = 999.0
    max_y = -999.0
        
    for outer in parsed:
        if outer[0]=='fp_poly':
        	  for poly in outer[1]:
        	  	  if poly[0]=='xy':
        	  		    if poly[1] > max_x:
        	  		        max_x = poly[1]
        	  		    if poly[1] < min_x:
        	  		        min_x = poly[1]
        	  		    if poly[2] > max_y:
        	  		        max_y = poly[2]
        	  		    if poly[2] < min_y:
        	  		        min_y = poly[2]
        	  		                	  		
    scale_factor = (max_x - min_x)/silk_size
    
    # run through and scale
    for outer in parsed:
        if outer[0]=='fp_poly':
        	  for poly in outer[1]:
        	  	  if poly[0]=='xy':
        	  		    poly[1] = poly[1]/scale_factor
        	  		    poly[2] = poly[2]/scale_factor
    
    parsed[1] = parsed[1]+'_'+str(silk_size)+'mm'
        	  		     
    fp = open(input_file+'_'+str(silk_size)+'mm.kicad_mod','w')
    fp.write( print_sexp(parsed))
    fp.close()


