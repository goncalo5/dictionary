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
            add_word("house", "casa") -> {word: [{en: house, pt: casa, pts: 1}, ...]}
            add_word("house", "casa, vivenda") -> {word: [{en: "house", pt: "casa, vivenda", pts: 1}, ...]}
            add_word("rabbit, bunny", "coelho") -> {word: [{en: "rabiit, bunny", pt: "coelho", pts: 1}, ...]}
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
            check_solution(casa, house) -> True
            check_solution(casa, House) -> True
            check_solution(casa, HOUSE) -> True
            check_solution(casa, hose) -> False
            check_solution(house, casa) -> True
            check_solution(house, vivenda) -> True

    update_word_points:
        ex:
            update_word_points(casa, house)
                -> {words: [{en: house, pt: casa, pts: 2}, ...]}
            update_word_points(casa, hose})
                -> {words: [{en: house, pt: casa, pts: 0.5}, ...]}
            update_word_points(casa, ""})
                -> {words: [{en: house, pt: casa, pts: 0.5}, ...]}

    update_points:
        ex:
            update_points(points, is_correct) -> 550
            update_points(points, is_not_correct) -> 450

    order_by_points:
        ex:
            order_by_points() -> [{en: house, pt: casa, points: 1}, {... points: 2}, ...]
