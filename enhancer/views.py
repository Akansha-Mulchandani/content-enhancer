from django.shortcuts import render

def correct_grammar(text):
    # Fix common spelling mistakes and grammar
    corrections = {
        'lik': 'like',
        'travl': 'travel',
        'i': 'I',
        'dont': "don't",
        'teh': 'the',
        'freind': 'friend',
        'wanna': 'want to',
    }
    # Phrase corrections for grammar
    phrase_corrections = {
        'I is': 'I am',
    }
    # Check for phrase corrections first
    corrected_text = text
    for wrong, right in phrase_corrections.items():
        corrected_text = corrected_text.replace(wrong, right)
    
    # Split into words
    words = corrected_text.split()
    corrected_words = []
    for word in words:
        # Preserve proper nouns (words starting with capital letter)
        if word[0].isupper() and word.lower() not in corrections:
            corrected_word = word
        else:
            # Fix spelling or keep word as is
            corrected_word = corrections.get(word.lower(), word)
            # Capitalize 'I'
            if word.lower() == 'i':
                corrected_word = 'I'
        corrected_words.append(corrected_word)
    
    corrected_text = ' '.join(corrected_words)
    # Add a period at the end
    if not corrected_text.endswith('.'):
        corrected_text += '.'
    return corrected_text

def enhance_content(text):
    # Generate a paragraph with >50 words
    enhancements = {
        'travel': ' I love exploring new destinations, discovering unique cultures, and experiencing breathtaking adventures.',
        'food': ' Enjoying delicious meals from various cuisines brings joy and satisfaction to my daily life.',
        'like': ' I find great pleasure in engaging with activities that spark my enthusiasm and creativity.',
        'happy': ' Feeling excited and joyful allows me to embrace every moment with a positive outlook.',
        'learn': ' Gaining new knowledge and skills is an enriching experience that fuels my personal growth.',
        'I am': ' Being myself allows me to pursue my passions and connect with others authentically.',
    }
    enhanced = text
    # Add multiple enhancements to reach >50 words
    added_count = 0
    for key, phrase in enhancements.items():
        if key.lower() in enhanced.lower() and added_count < 3:  # Limit to 3 enhancements
            enhanced += phrase
            added_count += 1
    
    # Default phrase if output is too short
    default_phrase = ' This experience inspires me to continue exploring, learning, and sharing my journey with others.'
    if len(enhanced.split()) < 50:
        enhanced += default_phrase
    
    # Trim if too long (optional, to keep it readable)
    words = enhanced.split()
    if len(words) > 100:
        enhanced = ' '.join(words[:100]) + '.'
    
    return enhanced

def generate_hashtags(text):
    # Make hashtags from important words
    words = text.split()
    hashtags = []
    skip_words = ['like', 'and', 'to', 'the', 'is', 'with', 'for']
    for word in words:
        if len(word) > 3 and word.lower() not in skip_words:
            hashtags.append(f'#{word.capitalize()}')
    return ' '.join(hashtags[:3])

def index(request):
    corrected_text = ''
    enhanced_text = ''
    hashtags = ''
    if request.method == 'POST':
        input_text = request.POST.get('input_text', '')
        if input_text:
            corrected_text = correct_grammar(input_text)
            enhanced_text = enhance_content(corrected_text)
            hashtags = generate_hashtags(corrected_text)
    return render(request, 'enhancer/index.html', {
        'corrected_text': corrected_text,
        'enhanced_text': enhanced_text,
        'hashtags': hashtags
    })