import itertools,pytest
from combine_ratings import Evaluation,RatingInputError,calculate,combine_pair,combine_values
@pytest.mark.parametrize('values,raw,final',[
([50,30],65,70),([40,20],52,50),([60,40,20],81,80),([0,0],0,0),([100,10],100,100),([70,50],85,90),([30,30,30],66,70)])
def test_vectors(values,raw,final):
    r=calculate([Evaluation(x,str(x)) for x in values]);assert r['raw_final_value']==raw;assert r['rounded_final_evaluation']==final

def test_pair_trace():
    value,step=combine_pair(60,40);assert value==76;assert step['remaining_efficiency']==40

def test_order_invariance():
    expected=None
    for p in itertools.permutations([60,30,20,10]):
        value=calculate([Evaluation(x) for x in p])['rounded_final_evaluation']
        expected=value if expected is None else expected;assert value==expected

def test_monotonicity():
    for a in range(0,101,10):
      for b in range(0,101,10):
        low=calculate([Evaluation(a),Evaluation(b)])['rounded_final_evaluation']
        high=calculate([Evaluation(min(100,a+10)),Evaluation(b)])['rounded_final_evaluation']
        assert high>=low

def test_invalid():
    with pytest.raises(RatingInputError):Evaluation.from_mapping({'percent':101},0)
