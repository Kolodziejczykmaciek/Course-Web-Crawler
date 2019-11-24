import re

example = "Kot dzisaj zrobil sztuke, jakas taka robi akrobacje ze naskakuje na dzrzwi i sie od nich odbija"

pattern = 't$'

result = re.findall(pattern, example)
print(result)