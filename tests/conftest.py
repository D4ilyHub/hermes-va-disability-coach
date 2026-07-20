from pathlib import Path
import sys
ROOT=Path(__file__).parents[1]
SCRIPTS=ROOT/'skills'/'va-disability-coach'/'scripts'
sys.path.insert(0,str(SCRIPTS))
