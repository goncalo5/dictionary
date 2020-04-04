# dictionary

Actions:
    new_word:
        input: {lang1: word, lang2: word}
        ex:
            {en: house, pt: casa} -> {word: [{en: house, pt: casa, pts: 1}, ...]}
            {en: house, abc: casa} -> error(that language doesnt exist)
    edit_word:

    delete_word:
        input: {lang: word}
        ex:
            {en: house} -> {word: [ ...]}