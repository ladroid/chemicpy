import re
import sympy
from chemelement import atomicWeightsDecimal
ELEMENT_CLAUSE = re.compile("([A-Z][a-z]?)([0-9]*)")

def parse_compound(compound):
    assert "(" not in compound, "This parser doesn't grok subclauses"
    return {el: (int(num) if num else 1) for el, num in ELEMENT_CLAUSE.findall(compound)}

def chem_balance(formula_left, formula_right):
  formulal = formula_left.split()
  formular = formula_right.split()
  left_com = [parse_compound(compound) for compound in formulal]
  right_com = [parse_compound(compound) for compound in formular]
  print(left_com, right_com)

  els = sorted(set().union(*left_com, *right_com))
  els_index = dict(zip(els, range(len(els))))
  print(els, els_index)

  w = len(left_com) + len(right_com)
  h = len(els)
  A = [[0] * w for _ in range(h)]
  
  for col, compound in enumerate(left_com):
    for el, num in compound.items():
      row = els_index[el]
      A[row][col] = num
  for col, compound in enumerate(right_com, len(left_com)):
    for el, num in compound.items():
      row = els_index[el]
      A[row][col] = -num
  
  A = sympy.Matrix(A)
  coeffs = A.nullspace()[0]    
  coeffs *= sympy.lcm([term.q for term in coeffs])

  lhs = " + ".join(["{} {}".format(coeffs[i], s) for i, s in enumerate(formulal)])
  rhs = " + ".join(["{} {}".format(coeffs[i], s) for i, s in enumerate(formular, len(formulal))])
  print("\nBalanced solution:")
  print("{} -> {}".format(lhs, rhs))

def mendeleev(element):
  print(atomicWeightsDecimal[element])

chem_balance('Al O2', 'Al2O3')
mendeleev('H')