from rarity_tools_scraper.projects import BasePropDef, ConfigRankingsPreset


# key: "getPropWeight",
#   value: function(t, e, r) {
#     return t.isMatch && !r || e.combined && t.hasCombined || !e.combined && t.isCombined
#       ? 0
#       : e.propWeights && void 0 !== e.propWeights[t.name] && e.weights && "data" == t.type && "score" == e.method
#         ? e.propWeights[t.name]
#         : "primaryKey" == t.type || "data" == t.type
#           ? 0
#           : e.weights && e.propWeights
#             ? void 0 === e.propWeights[t.name]
#               ? 1
#               : e.propWeights[t.name]
#             : 1
#   }
def get_prop_weight(base_prop_def: BasePropDef, options: ConfigRankingsPreset, matches: str):
	prop_defs_weight = options.prop_weights[base_prop_def.name]
	# TODO: has_combined
	if base_prop_def.is_match and not matches or options.combined and base_prop_def["has_combined"] \
		or not options.combined and base_prop_def.is_combined:
		return 0
	else:
		if options.prop_weights and prop_defs_weight is not None and options.weights and base_prop_def.type == "data" \
				and options.method == "score":
			return prop_defs_weight
		else:
			if base_prop_def.type == "primaryKey" and options.method == "data":
				return 0
			else:
				if options.weights and options.prop_weights:
					if prop_defs_weight is None:
						return 0
					else:
						return prop_defs_weight
				else:
					return 1
