import argparse, json


def genes(path):
    return {line.strip() for line in open(path, encoding="utf-8") if line.strip()}


parser = argparse.ArgumentParser()
parser.add_argument("--measured", required=True); parser.add_argument("--mapped", required=True); parser.add_argument("--model", required=True)
args = parser.parse_args()
measured, mapped, model = genes(args.measured), genes(args.mapped), genes(args.model)
usable = measured & mapped & model
print(json.dumps({"measured": len(measured), "orthology_mapped": len(measured & mapped), "model_usable": len(usable), "retained_fraction": len(usable) / max(len(measured), 1)}, indent=2))
