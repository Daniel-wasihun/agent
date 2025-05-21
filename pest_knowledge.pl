% Pest Knowledge Base
% Format: pest(Name, crops(Crops), regions(Regions), symptoms(Symptoms), control_measures(Control), life_cycle(LifeCycle),
%         economic_impact(Impact), environmental_conditions(Env), appearance(Appearance), synonyms(Synonyms)).

pest(aphid,
     crops([tomato, wheat, potato, cabbage, soybean, lettuce, rose, beans, peas]),
     regions([tropical, temperate, subtropical]),
     symptoms([yellowing_leaves, sticky_honeydew, curling_leaves, stunted_growth, virus_transmission, sooty_mold, distorted_shoots, reduced_yield]),
     control_measures(
         chemical([imidacloprid, malathion, neem_oil, pyrethrum, acetamiprid]),
         biological([ladybugs, lacewings, parasitic_wasps_aphidius_spp, syrphid_flies, predatory_midges]),
         cultural([crop_rotation, remove_infested_plants, use_reflective_mulch, intercropping_with_marigolds, water_jet_dislodgement])
     ),
     life_cycle('Eggs hatch in 7-10 days, nymphs mature in 10-14 days, multiple generations per season (up to 20 in warm climates).'),
     economic_impact('Reduces yield by 20-40% in severe infestations; significant in vegetables and ornamentals due to virus transmission.'),
     environmental_conditions(temperature('15-25°C'), humidity('Moderate to high'), soil_type('No specific preference')),
     appearance(color([green, black, brown, yellow, pink]), size(['small', '1-3mm'])),
     synonyms(['plant lice', 'greenfly', 'blackfly', 'Aphis spp.'])).

pest(whitefly,
     crops([tomato, cotton, cucumber, pepper, eggplant, sweet_potato, cassava, beans]),
     regions([tropical, subtropical, greenhouses]),
     symptoms([sticky_leaves, tiny_white_insects, yellowing_leaves, sooty_mold, virus_transmission, leaf_wilting, reduced_photosynthesis]),
     control_measures(
         chemical([insecticidal_soap, pyriproxyfen, buprofezin, dinotefuran, spiromesifen]),
         biological(['Encarsia formosa', 'Eretmocerus spp.', 'predatory_beetles_delphastus_spp', 'Macrolophus pygmaeus']),
         cultural([yellow_sticky_traps, maintain_weed_free_fields, use_reflective_mulch, screen_greenhouse_vents, monitor_with_traps])
     ),
     life_cycle('Eggs hatch in 5-10 days, lifecycle completes in 20-30 days, multiple generations per year.'),
     economic_impact('Yield losses up to 50% in greenhouse crops; affects export quality due to virus transmission (e.g., Tomato Yellow Leaf Curl Virus).'),
     environmental_conditions(temperature('20-30°C'), humidity('High'), soil_type('Well-drained')),
     appearance(color([white]), size(['tiny', '1-2mm'])),
     synonyms(['white fly', 'whiteflies', 'Bemisia tabaci', 'Trialeurodes vaporariorum'])).

pest(fall_armyworm,
     crops([maize, sorghum, rice, cotton, millet, sugarcane, pasture, wheat]),
     regions([tropical, subtropical, temperate]),
     symptoms([chewed_leaves, holes_in_stems, frass_on_plants, defoliation, larvae_in_whorls, damaged_cobs]),
     control_measures(
         chemical([spinosad, chlorantraniliprole, lambda_cyhalothrin, emamectin_benzoate]),
         biological(['Bacillus thuringiensis', 'Trichogramma wasps', 'predatory_bugs', 'Telenomus remus']),
         cultural([early_planting, intercropping_with_legumes, destroy_crop_residues, push_pull_strategy_with_napier_grass])
     ),
     life_cycle('Eggs hatch in 2-4 days, larvae feed for 14-30 days, lifecycle completes in 30-50 days, multiple generations in warm climates.'),
     economic_impact('Can cause 20-100% yield loss in maize; significant threat to subsistence farming in Africa and Asia.'),
     environmental_conditions(temperature('20-35°C'), humidity('Moderate'), soil_type('Loamy')),
     appearance(color([brown, green, gray]), size(['medium', '15-40mm larvae'])),
     synonyms(['Spodoptera frugiperda', 'armyworm', 'maize armyworm'])).

pest(spider_mite,
     crops([tomato, strawberry, cucumber, soybean, apple, grape, rose, ornamentals]),
     regions([temperate, subtropical, arid, greenhouses]),
     symptoms([stippling_on_leaves, webbing, yellowing, bronzing, leaf_drop, reduced_photosynthesis, speckled_leaves]),
     control_measures(
         chemical([abamectin, bifenazate, spiromesifen, hexythiazox, etoxazole]),
         biological(['Phytoseiulus persimilis', 'Neoseiulus californicus', 'Amblyseius andersoni', 'Feltiella acarisuga']),
         cultural([increase_humidity, avoid_water_stress, remove_infested_leaves, avoid_broad_spectrum_pesticides])
     ),
     life_cycle('Eggs hatch in 3-5 days, lifecycle completes in 10-20 days under warm conditions, multiple generations per season.'),
     economic_impact('Reduces fruit quality; losses up to 30-60% in strawberries, grapes, and greenhouse crops.'),
     environmental_conditions(temperature('25-35°C'), humidity('Low to moderate'), soil_type('No specific preference')),
     appearance(color([red, yellow, green]), size(['tiny', '0.3-0.5mm'])),
     synonyms(['red spider mite', 'two-spotted spider mite', 'Tetranychus urticae'])).

pest(thrips,
     crops([onion, cotton, tomato, pepper, citrus, rose, greenhouse_crops, cucumber]),
     regions([tropical, subtropical, temperate]),
     symptoms([silvering_leaves, stippling, distorted_growth, virus_transmission, black_frass_spots, bud_damage]),
     control_measures(
         chemical([spinosad, imidacloprid, methomyl, cyantraniliprole, abamectin]),
         biological(['Orius spp.', 'Amblyseius swirskii', 'predatory_mites', 'Hypoaspis miles']),
         cultural([blue_sticky_traps, crop_rotation, remove_weeds, monitor_with_sticky_cards, avoid_over_fertilization])
     ),
     life_cycle('Eggs hatch in 3-5 days, lifecycle completes in 15-30 days, multiple generations per season.'),
     economic_impact('Reduces onion yield by 20-50%; impacts fruit and flower quality; vectors Tospoviruses.'),
     environmental_conditions(temperature('20-30°C'), humidity('Low to moderate'), soil_type('Sandy loam')),
     appearance(color([yellow, brown, black]), size(['tiny', '0.5-2mm'])),
     synonyms(['thrip', 'Frankliniella occidentalis', 'Thrips tabaci'])).

pest(cutworm,
     crops([maize, potato, tomato, cabbage, soybean, sunflower, peppers]),
     regions([temperate, subtropical]),
     symptoms([cut_stems, wilting_seedlings, chewed_leaves, larvae_in_soil, plant_collapse]),
     control_measures(
         chemical([permethrin, carbaryl, deltamethrin, chlorantraniliprole]),
         biological(['Trichogramma wasps', 'Steinernema carpocapsae', 'Heterorhabditis bacteriophora']),
         cultural([tillage, remove_weeds, use_barriers_collars, flood_irrigation])
     ),
     life_cycle('Eggs hatch in 5-10 days, larvae feed for 20-40 days, lifecycle completes in 35-60 days.'),
     economic_impact('Destroys 10-30% of seedlings in severe cases; significant in early-season crops.'),
     environmental_conditions(temperature('15-25°C'), humidity('Moderate'), soil_type('Moist, loamy')),
     appearance(color([gray, brown, black]), size(['medium', '20-40mm larvae'])),
     synonyms(['Agrotis spp.', 'black cutworm', 'common cutworm'])).

pest(corn_earworm,
     crops([maize, tomato, cotton, sorghum, bean, pepper, sunflower]),
     regions([tropical, subtropical, temperate]),
     symptoms([chewed_kernels, holes_in_fruits, frass, larvae_in_ears_or_pods, damaged_flowers]),
     control_measures(
         chemical([spinosad, lambda_cyhalothrin, methoxyfenozide, chlorantraniliprole]),
         biological(['Trichogramma wasps', 'Bacillus thuringiensis', 'nuclear polyhedrosis_virus']),
         cultural([early_planting, destroy_crop_residues, use_bt_crops, monitor_with_pheromone_traps])
     ),
     life_cycle('Eggs hatch in 2-5 days, larvae feed for 10-20 days, lifecycle completes in 30-40 days.'),
     economic_impact('Reduces maize and cotton yield by 15-30%; affects fruit and vegetable quality.'),
     environmental_conditions(temperature('20-30°C'), humidity('Moderate'), soil_type('No specific preference')),
     appearance(color([green, brown, yellow]), size(['medium', '15-35mm larvae'])),
     synonyms(['Helicoverpa zea', 'cotton bollworm', 'tomato fruitworm'])).

pest(colorado_potato_beetle,
     crops([potato, tomato, eggplant, pepper]),
     regions([temperate, subtropical]),
     symptoms([defoliation, chewed_leaves, yellow_larvae, black_stripes_on_adults, reduced_tuber_yield]),
     control_measures(
         chemical([imidacloprid, spinosad, azadirachtin, chlorantraniliprole]),
         biological(['Lebia grandis', 'Bacillus thuringiensis_var_tenebrionis', 'Perillus bioculatus']),
         cultural([crop_rotation, hand_picking, use_resistant_varieties, mulching_with_straw])
     ),
     life_cycle('Eggs hatch in 4-10 days, larvae feed for 10-20 days, lifecycle completes in 30-50 days.'),
     economic_impact('Causes 30-50% yield loss in potatoes; significant in organic and small-scale farming.'),
     environmental_conditions(temperature('15-25°C'), humidity('Moderate'), soil_type('Loamy')),
     appearance(color([yellow, black_stripes]), size(['medium', '8-12mm adults', '5-15mm larvae'])),
     synonyms(['Leptinotarsa decemlineata', 'potato beetle', 'ten-lined beetle'])).

pest(diamondback_moth,
     crops([cabbage, broccoli, cauliflower, kale, mustard, brussels_sprouts]),
     regions([tropical, temperate, subtropical]),
     symptoms([holes_in_leaves, webbing, small_green_larvae, windowpane_effect, defoliation]),
     control_measures(
         chemical([spinosad, indoxacarb, emamectin_benzoate, chlorantraniliprole]),
         biological(['Diadegma insulare', 'Bacillus thuringiensis', 'Cotesia vestalis']),
         cultural([crop_rotation, remove_crop_debris, use_trap_crops_like_mustard, floating_row_covers])
     ),
     life_cycle('Eggs hatch in 4-6 days, lifecycle completes in 15-30 days, multiple generations per season.'),
     economic_impact('Reduces cabbage yield by 20-40%; costly due to pesticide resistance in some regions.'),
     environmental_conditions(temperature('15-30°C'), humidity('Moderate to high'), soil_type('No specific preference')),
     appearance(color([green_larvae, gray_brown_adults]), size(['small', '5-8mm larvae', '8-12mm adults'])),
     synonyms(['Plutella xylostella', 'cabbage moth', 'brassica moth'])).

pest(cabbage_looper,
     crops([cabbage, broccoli, lettuce, celery, spinach, cauliflower]),
     regions([temperate, subtropical]),
     symptoms([large_holes_in_leaves, green_larvae, frass, looping_movement, defoliation]),
     control_measures(
         chemical([spinosad, permethrin, methoxyfenozide, chlorantraniliprole]),
         biological(['Trichogramma wasps', 'Bacillus thuringiensis', 'nuclear_polyhedrosis_virus']),
         cultural([floating_row_covers, remove_infested_leaves, intercropping_with_dill])
     ),
     life_cycle('Eggs hatch in 3-5 days, larvae feed for 15-25 days, lifecycle completes in 25-35 days.'),
     economic_impact('Causes 20-30% yield loss in leafy vegetables; affects organic production.'),
     environmental_conditions(temperature('20-30°C'), humidity('Moderate'), soil_type('No specific preference')),
     appearance(color([green_larvae, brown_adults]), size(['medium', '20-30mm larvae', '15-20mm adults'])),
     synonyms(['Trichoplusia ni', 'looper caterpillar', 'cabbage worm'])).

pest(fruit_fly,
     crops([mango, citrus, banana, guava, papaya, peach, apple]),
     regions([tropical, subtropical]),
     symptoms([punctures_in_fruit, rotting_fruit, larvae_in_fruit, fruit_drop, discoloration]),
     control_measures(
         chemical([malathion, spinosad, dimethoate, fipronil]),
         biological(['parasitic_wasps_fopius_arisanus', 'sterile_insect_technique', 'Opius longicaudatus']),
         cultural([sanitation, bagging_fruit, trapping_with_methyl_eugenol, early_harvest])
     ),
     life_cycle('Eggs hatch in 1-3 days, lifecycle completes in 20-30 days, multiple generations per year.'),
     economic_impact('Causes 50-80% fruit loss in severe cases; restricts export due to quarantine regulations.'),
     environmental_conditions(temperature('25-35°C'), humidity('High'), soil_type('No specific preference')),
     appearance(color([yellow, brown, black]), size(['small', '3-5mm adults'])),
     synonyms(['Bactrocera spp.', 'Ceratitis capitata', 'Mediterranean fruit fly', 'tropical fruit fly'])).

pest(boll_weevil,
     crops([cotton]),
     regions([tropical, subtropical, temperate]),
     symptoms([boll_damage, punctured_squares, larvae_in_bolls, square_drop, reduced_lint_quality]),
     control_measures(
         chemical([malathion, pyrethroids, organophosphates, spinosad]),
         biological(['Anthonomus grandis parasites', 'predatory_insects', 'Bracon spp.']),
         cultural([destroy_crop_residues, early_planting, pheromone_traps, use_bt_cotton])
     ),
     life_cycle('Eggs hatch in 3-5 days, larvae feed for 7-12 days, lifecycle completes in 20-25 days.'),
     economic_impact('Reduces cotton yield by 10-40%; historically devastating, reduced by eradication programs.'),
     environmental_conditions(temperature('20-30°C'), humidity('Moderate'), soil_type('Well-drained')),
     appearance(color([gray, brown]), size(['small', '4-6mm adults'])),
     synonyms(['Anthonomus grandis', 'cotton weevil', 'boll beetle'])).

pest(stem_borer,
     crops([maize, rice, sugarcane, sorghum, millet, wheat]),
     regions([tropical, subtropical]),
     symptoms([tunneling_in_stems, frass, wilting, dead_heart_in_young_plants, broken_stems]),
     control_measures(
         chemical([chlorantraniliprole, carbofuran, fipronil, imidacloprid]),
         biological(['Trichogramma wasps', 'Bacillus thuringiensis', 'Cotesia flavipes']),
         cultural([destroy_crop_residues, intercropping_with_legumes, use_resistant_varieties])
     ),
     life_cycle('Eggs hatch in 5-7 days, larvae feed for 20-40 days, lifecycle completes in 40-60 days.'),
     economic_impact('Causes 20-50% yield loss in maize and rice; significant in tropical agriculture.'),
     environmental_conditions(temperature('20-35°C'), humidity('Moderate to high'), soil_type('Loamy')),
     appearance(color([white, cream, brown_larvae]), size(['medium', '10-25mm larvae'])),
     synonyms(['Chilo partellus', 'Busseola fusca', 'maize stem borer', 'rice borer'])).

pest(leafhopper,
     crops([grape, potato, bean, rice, alfalfa, cotton, tomato]),
     regions([temperate, subtropical, tropical]),
     symptoms([yellowing, stippling, virus_transmission, sap_sucking, leaf_curling, hopper_burn]),
     control_measures(
         chemical([imidacloprid, pyrethroids, dinotefuran, thiamethoxam]),
         biological(['Anagrus spp.', 'predatory_bugs', 'Erythroneura spp.']),
         cultural([remove_weeds, use_resistant_varieties, monitor_with_yellow_sticky_traps])
     ),
     life_cycle('Eggs hatch in 6-10 days, lifecycle completes in 20-40 days, multiple generations per season.'),
     economic_impact('Reduces grape and rice yield by 15-30% via virus spread; affects vegetable quality.'),
     environmental_conditions(temperature('20-30°C'), humidity('Moderate'), soil_type('No specific preference')),
     appearance(color([green, yellow, brown]), size(['small', '3-5mm adults'])),
     synonyms(['Cicadellidae', 'jassid', 'grape leafhopper'])).

pest(mealybug,
     crops([grape, citrus, cotton, pineapple, coffee, cocoa, papaya]),
     regions([tropical, subtropical, greenhouses]),
     symptoms([sticky_honeydew, sooty_mold, stunted_growth, white_waxy_coating, leaf_yellowing, fruit_drop]),
     control_measures(
         chemical([insecticidal_soap, imidacloprid, buprofezin, spirotetramat]),
         biological(['Cryptolaemus montrouzieri', 'parasitic_wasps_leptomastix_dactylopii', 'ladybugs']),
         cultural([prune_infested_parts, maintain_plant_health, use_sticky_barriers, monitor_with_traps])
     ),
     life_cycle('Eggs hatch in 5-10 days, lifecycle completes in 30-40 days, multiple generations per year.'),
     economic_impact('Reduces fruit quality; losses up to 30-50% in grapes, citrus, and coffee.'),
     environmental_conditions(temperature('20-30°C'), humidity('High'), soil_type('No specific preference')),
     appearance(color([white, pink]), size(['small', '2-5mm'])),
     synonyms(['Pseudococcidae', 'mealy bug', 'cotton mealybug'])).

pest(scale_insect,
     crops([citrus, olive, apple, grape, mango, ornamentals, peach]),
     regions([tropical, subtropical, temperate]),
     symptoms([galls, yellowing, sooty_mold, stunted_growth, sticky_honeydew, leaf_drop]),
     control_measures(
         chemical([horticultural_oil, imidacloprid, pyriproxyfen, spirotetramat]),
         biological(['Aphytis melinus', 'Chilocorus spp.', 'Metaphycus helvolus', 'ladybugs']),
         cultural([prune_infested_branches, maintain_plant_vigor, monitor_with_sticky_traps])
     ),
     life_cycle('Eggs hatch in 7-14 days, lifecycle completes in 30-60 days, multiple generations per year.'),
     economic_impact('Reduces citrus and grape yield by 20-40%; affects fruit aesthetics and marketability.'),
     environmental_conditions(temperature('20-30°C'), humidity('Moderate to high'), soil_type('Well-drained')),
     appearance(color([brown, black, gray]), size(['tiny', '1-5mm'])),
     synonyms(['Coccidae', 'armored scale', 'soft scale'])).

pest(wireworm,
     crops([potato, maize, wheat, carrot, sugar_beet, onion, lettuce]),
     regions([temperate, subtropical]),
     symptoms([tunneling_in_roots, wilting, stunted_growth, holes_in_tubers, seedling_death]),
     control_measures(
         chemical([imidacloprid, fipronil, clothianidin, thiamethoxam]),
         biological([entomopathogenic_nematodes_steinernema_spp, 'Metarhizium anisopliae']),
         cultural([crop_rotation_with_non_hosts, deep_tillage, avoid_planting_in_infested_fields])
     ),
     life_cycle('Larvae live 2-5 years in soil, lifecycle completes in 3-6 years, one generation every few years.'),
     economic_impact('Causes 10-30% yield loss in root crops; significant in potatoes and carrots.'),
     environmental_conditions(temperature('10-20°C'), humidity('High'), soil_type('Moist, loamy')),
     appearance(color([yellow, brown]), size(['medium', '10-25mm larvae'])),
     synonyms(['Agriotes spp.', 'click beetle larvae', 'soil wireworm'])).

pest(armyworm,
     crops([maize, wheat, rice, pasture, sorghum, millet, barley]),
     regions([tropical, subtropical, temperate]),
     symptoms([defoliation, chewed_leaves, frass, larvae_in_clusters, skeletonized_leaves]),
     control_measures(
         chemical([spinosad, lambda_cyhalothrin, chlorantraniliprole, methoxyfenozide]),
         biological(['Trichogramma wasps', 'Bacillus thuringiensis', 'Spodoptera frugiperda NPV']),
         cultural([early_planting, destroy_crop_residues, intercropping_with_legumes])
     ),
     life_cycle('Eggs hatch in 3-5 days, larvae feed for 20-30 days, lifecycle completes in 30-50 days.'),
     economic_impact('Causes 20-50% yield loss in cereals; affects fodder crops and pastures.'),
     environmental_conditions(temperature('20-30°C'), humidity('Moderate'), soil_type('No specific preference')),
     appearance(color([green, brown, black]), size(['medium', '20-40mm larvae'])),
     synonyms(['Spodoptera spp.', 'common armyworm', 'beet armyworm'])).

pest(green_stink_bug,
     crops([soybean, tomato, pepper, cotton, rice, pecan, bean]),
     regions([tropical, subtropical, temperate]),
     symptoms([sap_sucking, fruit_damage, discoloration, seed_damage, deformed_pods]),
     control_measures(
         chemical([pyrethroids, neonicotinoids, bifenthrin, lambda_cyhalothrin]),
         biological(['Trissolcus basalis', 'predatory_bugs', 'Telenomus podisi']),
         cultural([trap_crops_sorghum, remove_weeds, monitor_with_pheromone_traps])
     ),
     life_cycle('Eggs hatch in 5-7 days, lifecycle completes in 30-45 days, multiple generations per season.'),
     economic_impact('Reduces soybean and nut yield by 10-30%; affects seed and fruit quality.'),
     environmental_conditions(temperature('20-30°C'), humidity('Moderate to high'), soil_type('No specific preference')),
     appearance(color([green, brown]), size(['medium', '10-15mm adults'])),
     synonyms(['Nezara viridula', 'southern green stink bug', 'stinkbug'])).

pest(tarnished_plant_bug,
     crops([strawberry, cotton, alfalfa, bean, celery, apple, peach]),
     regions([temperate, subtropical]),
     symptoms([plant_distortion, flower_drop, deformed_fruit, stippling, cat_facing_on_fruit]),
     control_measures(
         chemical([imidacloprid, pyrethroids, flonicamid, novaluron]),
         biological(['Peristenus relictus', 'predatory_bugs', 'Anaphes iole']),
         cultural([weed_control, monitor_early_season, use_trap_crops_alfalfa])
     ),
     life_cycle('Eggs hatch in 7-10 days, lifecycle completes in 25-35 days, multiple generations per season.'),
     economic_impact('Causes 20-40% loss in strawberries and cotton; affects seed crops and fruit quality.'),
     environmental_conditions(temperature('15-25°C'), humidity('Moderate'), soil_type('No specific preference')),
     appearance(color([brown, yellow, green]), size(['small', '4-6mm adults'])),
     synonyms(['Lygus lineolaris', 'plant bug', 'firebug'])).

pest(desert_locust,
     crops([maize, wheat, sorghum, pasture, vegetables, fruit_trees, barley]),
     regions([tropical, subtropical, arid]),
     symptoms([massive_defoliation, chewed_plants, swarming_behavior, complete_crop_destruction]),
     control_measures(
         chemical([malathion, deltamethrin, fipronil, chlorpyrifos]),
         biological(['Metarhizium acridum', 'Nosema locustae', 'predatory_birds']),
         cultural([early_warning_systems, coordinated_spraying, barriers, monitor_with_satellite_imagery])
     ),
     life_cycle('Eggs hatch in 10-14 days, lifecycle completes in 35-50 days, multiple generations in outbreak years.'),
     economic_impact('Can devastate entire harvests; up to 100% crop loss in swarms, critical in East Africa and Middle East.'),
     environmental_conditions(temperature('25-35°C'), humidity('Moderate'), soil_type('Sandy')),
     appearance(color([yellow, brown, green]), size(['large', '40-60mm adults'])),
     synonyms(['Schistocerca gregaria', 'locust', 'swarming locust'])).

pest(japanese_beetle,
     crops([soybean, maize, grape, apple, rose, turfgrass, raspberry]),
     regions([temperate]),
     symptoms([skeletonized_leaves, chewed_flowers, root_damage_by_grubs, defoliation]),
     control_measures(
         chemical([imidacloprid, carbaryl, chlorantraniliprole, acephate]),
         biological(['Bacillus popilliae', 'entomopathogenic_nematodes_heterorhabditis_spp', 'Tiphia vernalis']),
         cultural([hand_picking, use_trap_crops_white_clover, apply_mulch])
     ),
     life_cycle('Eggs hatch in 10-14 days, grubs feed for 8-10 months, lifecycle completes in 1 year.'),
     economic_impact('Causes 20-30% loss in grapes and turf; affects ornamental plants and home gardens.'),
     environmental_conditions(temperature('20-30°C'), humidity('Moderate'), soil_type('Loamy, well-drained')),
     appearance(color([metallic_green, bronze_wings]), size(['medium', '8-11mm adults'])),
     synonyms(['Popillia japonica', 'Japanese scarab', 'grub beetle'])).

pest(codling_moth,
     crops([apple, pear, walnut, plum, apricot]),
     regions([temperate]),
     symptoms([tunneling_in_fruit, frass_at_fruit_entry, larvae_in_core, fruit_drop]),
     control_measures(
         chemical([spinosad, chlorantraniliprole, phosmet, azadirachtin]),
         biological(['Trichogramma wasps', 'Cydia pomonella_granulovirus', 'predatory_bugs']),
         cultural([sanitation, pheromone_traps, bagging_fruit, remove_infested_fruit])
     ),
     life_cycle('Eggs hatch in 6-14 days, larvae feed for 3-5 weeks, lifecycle completes in 45-60 days.'),
     economic_impact('Causes 30-50% fruit loss in apples and pears; affects export quality.'),
     environmental_conditions(temperature('15-25°C'), humidity('Moderate'), soil_type('No specific preference')),
     appearance(color([gray, brown]), size(['small', '5-10mm larvae', '10-15mm adults'])),
     synonyms(['Cydia pomonella', 'apple moth', 'fruit moth'])).

pest(european_corn_borer,
     crops([maize, pepper, potato, snap_bean, sorghum]),
     regions([temperate]),
     symptoms([tunneling_in_stalks, frass, broken_tassels, holes_in_leaves, damaged_ears]),
     control_measures(
         chemical([spinosad, lambda_cyhalothrin, teflubenzuron, chlorantraniliprole]),
         biological(['Trichogramma ostriniae', 'Bacillus thuringiensis', 'predatory_beetles']),
         cultural([destroy_crop_residues, use_bt_maize, early_planting])
     ),
     life_cycle('Eggs hatch in 4-9 days, larvae feed for 20-30 days, lifecycle completes in 40-60 days.'),
     economic_impact('Causes 10-20% yield loss in maize; significant in non-Bt crops and organic farming.'),
     environmental_conditions(temperature('20-30°C'), humidity('Moderate'), soil_type('No specific preference')),
     appearance(color([cream, brown_larvae]), size(['medium', '15-25mm larvae'])),
     synonyms(['Ostrinia nubilalis', 'corn borer', 'maize borer'])).

pest(red_palm_weevil,
     crops([palm, coconut, date_palm, oil_palm]),
     regions([tropical, subtropical]),
     symptoms([tunneling_in_trunk, wilting_fronds, frass, tree_collapse, chewed_leaf_bases]),
     control_measures(
         chemical([imidacloprid, fipronil, chlorpyrifos]),
         biological(['Steinernema carpocapsae', 'Beauveria bassiana', 'entomopathogenic_fungi']),
         cultural([sanitation, pheromone_traps, remove_infested_trees, monitor_with_acoustic_sensors])
     ),
     life_cycle('Eggs hatch in 3-7 days, larvae feed for 1-3 months, lifecycle completes in 4-6 months.'),
     economic_impact('Kills palms, causing 10-20% plantation loss; affects date and coconut production.'),
     environmental_conditions(temperature('25-35°C'), humidity('High'), soil_type('No specific preference')),
     appearance(color([red, brown]), size(['large', '30-50mm adults'])),
     synonyms(['Rhynchophorus ferrugineus', 'palm weevil', 'Asian palm weevil'])).

pest(citrus_psylla,
     crops([citrus, orange, lemon, grapefruit, lime]),
     regions([tropical, subtropical]),
     symptoms([leaf_curling, sooty_mold, stunted_growth, virus_transmission_citrus_greening, yellow_shoots]),
     control_measures(
         chemical([imidacloprid, spirotetramat, thiamethoxam, dimethoate]),
         biological(['Tamarixia radiata', 'ladybugs', 'parasitic_wasps']),
         cultural([prune_infested_shoots, monitor_with_yellow_sticky_traps, maintain_tree_health])
     ),
     life_cycle('Eggs hatch in 4-10 days, lifecycle completes in 20-40 days, multiple generations per season.'),
     economic_impact('Causes 20-50% yield loss via citrus greening disease transmission; major threat to citrus industry.'),
     environmental_conditions(temperature('20-30°C'), humidity('High'), soil_type('Well-drained')),
     appearance(color([brown, green]), size(['small', '2-4mm adults'])),
     synonyms(['Diaphorina citri', 'Asian citrus psyllid', 'citrus psyllid'])).

pest(pink_bollworm,
     crops([cotton]),
     regions([tropical, subtropical]),
     symptoms([damaged_bolls, larvae_in_seeds, reduced_lint_quality, boll_rot]),
     control_measures(
         chemical([spinosad, indoxacarb, chlorantraniliprole, pyrethroids]),
         biological(['Trichogramma wasps', 'Bacillus thuringiensis', 'predatory_bugs']),
         cultural([destroy_crop_residues, use_bt_cotton, pheromone_traps, early_harvest])
     ),
     life_cycle('Eggs hatch in 3-5 days, larvae feed for 10-14 days, lifecycle completes in 25-35 days.'),
     economic_impact('Causes 20-40% yield loss in cotton; affects fiber quality and export markets.'),
     environmental_conditions(temperature('25-35°C'), humidity('Moderate'), soil_type('Well-drained')),
     appearance(color([pink_larvae, brown_adults]), size(['small', '5-10mm larvae', '10-12mm adults'])),
     synonyms(['Pectinophora gossypiella', 'cotton bollworm', 'pink worm'])).

pest(coffee_berry_borer,
     crops([coffee]),
     regions([tropical, subtropical]),
     symptoms([holes_in_coffee_berries, larvae_in_beans, reduced_bean_quality, berry_drop]),
     control_measures(
         chemical([endosulfan, chlorpyrifos, cypermethrin]),
         biological(['Beauveria bassiana', 'parasitic_wasps_cephalonomia_stephanoderis', 'entomopathogenic_fungi']),
         cultural([sanitation, strip_picking, use_alcohol_traps, shade_management])
     ),
     life_cycle('Eggs hatch in 4-9 days, larvae feed for 10-26 days, lifecycle completes in 28-35 days.'),
     economic_impact('Causes 20-80% loss in coffee yield; affects export quality and smallholder farmers.'),
     environmental_conditions(temperature('20-30°C'), humidity('High'), soil_type('No specific preference')),
     appearance(color([black, brown]), size(['tiny', '1-2mm adults'])),
     synonyms(['Hypothenemus hampei', 'coffee borer', 'berry borer'])).

pest(tomato_hornworm,
     crops([tomato, pepper, eggplant, potato]),
     regions([temperate, subtropical]),
     symptoms([defoliation, large_green_larvae, frass, chewed_stems, fruit_damage]),
     control_measures(
         chemical([spinosad, carbaryl, methomyl, chlorantraniliprole]),
         biological(['Trichogramma wasps', 'Cotesia congregata', 'Bacillus thuringiensis']),
         cultural([hand_picking, use_companion_plants_marigolds, tillage])
     ),
     life_cycle('Eggs hatch in 5-7 days, larvae feed for 3-4 weeks, lifecycle completes in 40-50 days.'),
     economic_impact('Causes 20-40% yield loss in tomatoes; significant in home gardens and organic farms.'),
     environmental_conditions(temperature('20-30°C'), humidity('Moderate'), soil_type('No specific preference')),
     appearance(color([green_larvae, gray_brown_adults]), size(['large', '50-100mm larvae', '40-50mm adults'])),
     synonyms(['Manduca quinquemaculata', 'hornworm', 'tomato worm'])).

pest(root_knot_nematode,
     crops([tomato, potato, carrot, soybean, cotton, pepper, cucumber]),
     regions([tropical, subtropical, temperate]),
     symptoms([root_galls, wilting, stunted_growth, yellowing_leaves, reduced_root_system]),
     control_measures(
         chemical([oxamyl, fenamiphos, ethoprop]),
         biological(['Paecilomyces lilacinus', 'Bacillus firmus', 'Pasteuria penetrans']),
         cultural([crop_rotation_with_cereals, use_resistant_varieties, soil_solarization, add_organic_matter])
     ),
     life_cycle('Eggs hatch in 10-14 days, lifecycle completes in 20-40 days depending on temperature.'),
     economic_impact('Causes 20-50% yield loss in vegetables; significant in sandy soils and warm climates.'),
     environmental_conditions(temperature('20-30°C'), humidity('Moderate'), soil_type('Sandy, loamy')),
     appearance(color([transparent, white]), size(['microscopic', '0.5-1mm'])),
     synonyms(['Meloidogyne spp.', 'nematode', 'root nematode'])).

pest(brown_marmorated_stink_bug,
     crops([apple, peach, soybean, corn, tomato, grape]),
     regions([temperate, subtropical]),
     symptoms([fruit_damage, cat_facing, sap_sucking, discoloration, seed_loss]),
     control_measures(
         chemical([pyrethroids, neonicotinoids, bifenthrin, dinotefuran]),
         biological(['Trissolcus japonicus', 'predatory_bugs', 'parasitic_wasps']),
         cultural([trap_crops_sunflower, monitor_with_pheromone_traps, remove_weeds])
     ),
     life_cycle('Eggs hatch in 4-7 days, lifecycle completes in 40-60 days, one to two generations per year.'),
     economic_impact('Causes 20-40% fruit loss in orchards; significant in apples and peaches.'),
     environmental_conditions(temperature('15-30°C'), humidity('Moderate'), soil_type('No specific preference')),
     appearance(color([brown, gray, white_bands]), size(['medium', '12-17mm adults'])),
     synonyms(['Halyomorpha halys', 'stink bug', 'brown stink bug'])).

pest(white_grub,
     crops([maize, sugarcane, turfgrass, potato, soybean, pasture]),
     regions([temperate, subtropical]),
     symptoms([root_damage, wilting, stunted_growth, irregular_patches_in_turf, larvae_in_soil]),
     control_measures(
         chemical([imidacloprid, chlorantraniliprole, thiamethoxam]),
         biological([entomopathogenic_nematodes, 'Bacillus popilliae', 'Metarhizium anisopliae']),
         cultural([crop_rotation, deep_tillage, use_resistant_grasses_in_turf])
     ),
     life_cycle('Eggs hatch in 10-20 days, larvae feed for 1-3 years, lifecycle completes in 1-4 years.'),
     economic_impact('Causes 10-30% yield loss in maize and turf; affects root crops and pastures.'),
     environmental_conditions(temperature('15-25°C'), humidity('High'), soil_type('Loamy, organic-rich')),
     appearance(color([white, cream]), size(['medium', '10-30mm larvae'])),
     synonyms(['Phyllophaga spp.', 'grub', 'scarab larvae'])).

pest(aphid_lion,
     crops([beneficial_insect, not_a_pest]),
     regions([tropical, temperate, subtropical]),
     symptoms([none_beneficial, preys_on_aphids_mealybugs_and_small_insects]),
     control_measures(
         chemical([none]),
         biological([encourage_populations, release_lacewing_larvae]),
         cultural([plant_nectar_sources, avoid_broad_spectrum_pesticides])
     ),
     life_cycle('Eggs hatch in 3-6 days, larvae feed for 2-3 weeks, lifecycle completes in 25-35 days.'),
     economic_impact('Beneficial; reduces pest populations, especially aphids, by up to 70% in some crops.'),
     environmental_conditions(temperature('20-30°C'), humidity('Moderate'), soil_type('No specific preference')),
     appearance(color([green_larvae, brown_adults]), size(['small', '5-10mm larvae', '15-20mm adults'])),
     synonyms(['Chrysoperla spp.', 'lacewing larvae', 'green lacewing'])).