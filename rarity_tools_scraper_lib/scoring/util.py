from rarity_tools_scraper.projects import BasePropDef

# "options" would come from config.py
# key: "getPropWeight",
#   value: function(t, e, r) {
#     return t.isMatch && !r || e.combined && t.hasCombined || !e.combined && t.isCombined ? 0 : e.propWeights && void 0 !== e.propWeights[t.name] && e.weights && "data" == t.type && "score" == e.method ? e.propWeights[t.name] : "primaryKey" == t.type || "data" == t.type ? 0 : e.weights && e.propWeights ? void 0 === e.propWeights[t.name] ? 1 : e.propWeights[t.name] : 1
#   }
def get_prop_weight(base_prop_def: BasePropDef, options, matches: str):
	base_prop_def["isMatch"] and not matches or options["combined"] and t["isCombined"]