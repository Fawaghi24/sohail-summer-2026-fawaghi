def analyze_text(text):
    # Check if the text is empty
    if not text:
        return {
            "word_count": 0,
            "char_count_no_spaces": 0,
            "top_3_words": [],
            "longest_word": "",
        }

    # 1. Count characters excluding spaces
    char_count = 0
    for char in text:
        if not char.isspace():
            char_count += 1

    # 2. Clean the text
    text_clean = text.lower()
    punctuation = [".", ",", "!", "?", ";", ":", "(", ")", '"']
    for p in punctuation:
        text_clean = text_clean.replace(p, "")

    # Split the text into individual words
    words = text_clean.split()

    # Check if there are any valid words left
    if len(words) == 0:
        return {
            "word_count": 0,
            "char_count_no_spaces": char_count,
            "top_3_words": [],
            "longest_word": "",
        }

    # Total word count
    word_count = len(words)

    # 3. Find the longest word
    longest_word = words[0]
    for word in words:
        if len(word) > len(longest_word):
            longest_word = word

    # 4. Count frequency of each word
    word_counts = {}
    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

    # Find the top 3 most frequent words manually
    sorted_words = sorted(word_counts, key=word_counts.get, reverse=True)
    top_3_words = sorted_words[:3]

    # Return results in a dictionary
    return {
        "word_count": word_count,
        "char_count_no_spaces": char_count,
        "top_3_words": top_3_words,
        "longest_word": longest_word,
    }


# Test Section
if __name__ == "__main__":
    sample_paragraph = """
    Software engineering is an ever evolving field that demands continuous learning and strong problem 
    solving skills. As developers build software applications, they encounter numerous challenges ranging 
    from logic bugs to design decisions. Writing clean and maintainable code is essential for team 
    collaboration and long term project success. Internships provide an excellent opportunity to put 
    theoretical concepts into practice by working on real world tasks, learning developer tools, and 
    mastering version control systems like Git. By approaching each task with curiosity and consistency, 
    developers can significantly improve their software design capabilities over time.
    """

    results = analyze_text(sample_paragraph)

    print("Text Analysis Results")
    print("Word Count:", results["word_count"])
    print("Character Count (no spaces):", results["char_count_no_spaces"])
    print("Top 3 Words:", results["top_3_words"])
    print("Longest Word:", results["longest_word"])