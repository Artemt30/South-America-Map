#!/usr/bin/env python3
"""Select the 1000 most populous settlements from the checked-in GeoNames data."""
import json
from pathlib import Path
folder=Path("data/places")
manifest=json.loads((folder/"manifest.json").read_text(encoding="utf-8"))
best=[]
for country in manifest["countries"]:
    rows=json.loads((folder/(country+".json")).read_text(encoding="utf-8"))
    best.extend(row for row in rows if len(row)>=5 and isinstance(row[4],int) and row[4]>0)
    best.sort(key=lambda x:(-x[4],x[0]))
    del best[1000:]
best.sort(key=lambda x:(-x[4],x[0]))
(folder/"top1000.json").write_text(json.dumps(best,ensure_ascii=False,separators=(",",":")),encoding="utf-8")
print("Selected",len(best),"cities; min population",best[-1][4] if best else None)
