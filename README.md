# dictionary

Game:  # obj/dict
    points:
    languages:
    words:
        word_i:
            language1
            language2
            points

Actions:  # functions using game obj/dict
    add_word:
        input:
            {lang1: word, lang2: translation}
            {lang1: word, lang2: [translation1, translation2]}
        ex:
            {en: house, pt: casa} -> {word: [{en: house, pt: casa, pts: 1}, ...]}
            {en: house, pt: [casa, vivenda]} -> {word: [{en: house, pt: [casa, vivenda], pts: 1}, ...]}
    edit_word:

    delete_word:
        input: word or word_dict
        ex:
            delete_word(house) -> {word: [ ...]}
            delete_word(casa) -> {word: [ ...]}
            delete_word({en: house, pt: casa, points: 1}) -> {word: [ ...]}

    pick_random_word:
        ex:
            pick_random_word(pt, en) -> {pt: casa, en: house, points: 5}

    check_solution:
        ex:
            check_solution({pt: casa, en: house}) -> True
            check_solution({pt: casa, en: House}) -> True
            check_solution({pt: casa, en: HOUSE}) -> True
            check_solution({pt: casa, en: hose}) -> False
            check_solution({en: house, pt: casa}) -> True
            check_solution({en: house, pt: vivenda}) -> True

    update_word_points:
        ex:
            update_word_points(casa, house)
                -> {word: [{en: house, pt: [casa, vivenda], pts: 2}, ...]}
            update_word_points(casa, hose})
                -> {word: [{en: house, pt: [casa, vivenda], pts: 0.5}, ...]}
            update_word_points(casa, ""})
                -> {word: [{en: house, pt: [casa, vivenda], pts: 0.5}, ...]}

    update_points:
        ex:
            update_points(points, is_correct) -> 100
            update_points(points, is_not_correct) -> 85
