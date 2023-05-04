import random
import string

# Sample word list
word_list = ["hello", "world", "cat", "apple", "banana", "orange", "linux", 
             "windows", "iPhone", "beth", "what", "is", "i", "a", "can", "do", 
             "the", "this", "of", "are", "yes", "damage", "maths", "integral", 
             "fedora", "garuda", "ubuntu", "arch", "btw", "make", "these", "in",
             "android", "discord", "wtf", "where", "when", "who", "it", "if", "try",
             "to", "eat", "force", "creeper"]

def random_words(n, words):
    return random.sample(words, n)

def obfuscate(words, num_obfuscations):
    obfuscated_words = []
    for word in words:
        transformed_word = word
        for _ in range(num_obfuscations):
            rand_transform = random.randint(1, 7)
            if rand_transform == 1:
                # Make word uppercase or lowercase
                transformed_word = transformed_word.upper() if random.choice([True, False]) else transformed_word.lower()
            elif rand_transform == 2:
                # Insert a random letter
                random_letter = random.choice(string.ascii_letters)
                random_position = random.randint(0, len(transformed_word))
                transformed_word = transformed_word[:random_position] + random_letter + transformed_word[random_position:]
            elif rand_transform == 3:
                # remove a random letter
                random_position = random.randint(0, len(transformed_word) - 1)
                transformed_word = transformed_word[:random_position] + transformed_word[random_position + 1:]
            
            elif rand_transform == 4:
                # Insert random punctuation
                random_special = random.choice(string.punctuation)
                random_position = random.randint(0, len(transformed_word))
                transformed_word = transformed_word[:random_position] + random_special + transformed_word[random_position:]

            elif rand_transform == 5:
                # Replace a random letter
                random_letter = random.choice(string.ascii_letters)
                random_position = random.randint(0, len(transformed_word) - 1)
                transformed_word = transformed_word[:random_position] + random_letter + transformed_word[random_position + 1:]
        obfuscated_words.append(transformed_word)
    return " ".join(obfuscated_words)

def add_random_punctuation(s):
    punctuation_options = [".", "?", "!"]
    random_punctuation = random.choice(punctuation_options)
    return s + random_punctuation if random.random() < 0.75 else s

def gen_string(num_words, num_obfuscations):
    selected_words = random_words(num_words, word_list)
    obfuscated_string = add_random_punctuation(obfuscate(selected_words, num_obfuscations))
    return obfuscated_string
