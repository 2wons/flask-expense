
def get_category_emote(category):
    category_emojis = {
        'food': '🍕',
        'grocery': '🛒',
        'medical': '⚕️',
        'bills': '📄',
        'entertainment': '🎉',
        'shopping': '🛍️',
        'travel': '✈️',
        'debt': '💳',
        'loan': '💸',
        'other': '🔍'
    }
    # Prepend the emoji to the category, default to question mark emoji if not found
    return category_emojis.get(category, '❓') + ' ' + category
    