#import language_tool_python
import pprint
pp = pprint.PrettyPrinter(indent=2)

#tool = language_tool_python.LanguageTool('en-US')


def check_grammar(text):
    # get the matches
    #matches = tool.check(text)
    matches = []

    my_mistakes = []
    my_corrections = []
    start_positions = []
    end_positions = []

    for rules in matches:
        if len(rules.replacements)>0:
            start_positions.append(rules.offset)
            end_positions.append(rules.errorLength+rules.offset)
            my_mistakes.append(text[rules.offset:rules.errorLength+rules.offset])
            my_corrections.append(rules.replacements)

    review = []
    for index in range(len(my_mistakes)):
        review.append({
            "errors" : my_mistakes[index],
            "corrections" : my_corrections[index],
            "start" : start_positions[index],
            "end" : end_positions[index]
        })

    return review