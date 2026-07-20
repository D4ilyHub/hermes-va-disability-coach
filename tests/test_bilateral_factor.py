from combine_ratings import Evaluation,calculate

def ev(p,label,side='none',group='none'):return Evaluation(p,label,side,group)
def test_regulatory_style_example():
 r=calculate([ev(60,'A'),ev(20,'B'),ev(10,'L','left','lower_extremities'),ev(10,'R','right','lower_extremities')]);assert r['bilateral']['bilateral_combined_value']==19;assert r['bilateral']['bilateral_value_used']==21;assert r['rounded_final_evaluation']==70

def test_twenty_pair():
 r=calculate([ev(20,'L','left','upper_extremities'),ev(20,'R','right','upper_extremities')]);assert r['bilateral']['bilateral_value_used']==40;assert r['rounded_final_evaluation']==40

def test_four_extremities():
 r=calculate([ev(20,'UL','left','upper_extremities'),ev(20,'UR','right','upper_extremities'),ev(20,'LL','left','lower_extremities'),ev(20,'LR','right','lower_extremities')]);assert r['bilateral']['bilateral_combined_value']==59;assert r['bilateral']['bilateral_value_used']==65;assert r['rounded_final_evaluation']==70

def test_most_favorable_exception():
 r=calculate([ev(90,'A'),ev(30,'B'),ev(10,'L','left','lower_extremities'),ev(10,'R','right','lower_extremities')]);assert r['rounded_final_evaluation']==100;assert r['bilateral'] is None;assert any('4.26(d)' in x for x in r['warnings'])

def test_no_pair():
 r=calculate([ev(20,'L','left','lower_extremities'),ev(10,'X')]);assert r['bilateral'] is None

def test_zero_not_pair():
 r=calculate([ev(20,'L','left','lower_extremities'),ev(0,'R','right','lower_extremities')]);assert r['bilateral'] is None
