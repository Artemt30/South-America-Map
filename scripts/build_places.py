#!/usr/bin/env python3
"""Build South American settlement catalogue from GeoNames country extracts (CC BY 4.0)."""
import io, json, pathlib, urllib.request, zipfile
CODES="AR BO BR CL CO EC GY GF PY PE SR UY VE FK".split()
OUT=pathlib.Path("data/places");OUT.mkdir(parents=True,exist_ok=True)
summary={}
for code in CODES:
    url=f"https://download.geonames.org/export/dump/{code}.zip"
    print("Fetching",code,flush=True)
    req=urllib.request.Request(url,headers={"User-Agent":"SouthAmericaStrategy/0.2 (GitHub Actions data build)"})
    with urllib.request.urlopen(req,timeout=120) as resp: archive=resp.read()
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        with z.open(code+".txt") as file:
            entries=[]
            for raw in file:
                parts=raw.decode("utf-8").rstrip("\n").split("\t")
                if len(parts)<15 or parts[6]!="P" or parts[7] in {"PPLQ","PPLH","PPLX"}:continue
                try:
                    entries.append([int(parts[0]),parts[1],round(float(parts[4]),5),round(float(parts[5]),5),int(parts[14] or 0)])
                except ValueError:continue
    (OUT/f"{code}.json").write_text(json.dumps(entries,ensure_ascii=False,separators=(",",":")),encoding="utf-8")
    summary[code]=len(entries)
    print(code,len(entries),flush=True)
(OUT/"manifest.json").write_text(json.dumps({"source":"GeoNames","license":"CC BY 4.0","countries":summary,"total":sum(summary.values())},ensure_ascii=False),encoding="utf-8")
print("TOTAL",sum(summary.values()))
