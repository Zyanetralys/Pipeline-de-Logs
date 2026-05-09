import json, yaml, re, sys, logging, argparse
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

def load_rules(path):
    with open(path) as f: return list(yaml.safe_load_all(f))

def match(log, rule):
    sel = rule.get("detection", {}).get("selection", {})
    pat = sel.get("keyword", "")
    return bool(re.search(pat, str(log), re.I)) if pat else False

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("-r", "--rules", default="rules.yaml")
    args = p.parse_args()
    rules = load_rules(args.rules)
    for line in sys.stdin:
        try:
            log = json.loads(line.strip())
            alerts = [r["title"] for r in rules if match(log, r)]
            if alerts: logging.warning(json.dumps({"log": log, "alerts": alerts}))
        except: pass
