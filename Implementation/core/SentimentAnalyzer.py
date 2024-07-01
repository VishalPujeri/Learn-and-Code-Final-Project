def analyze_sentiment(comment):
    positive_words = ['good', 'great', 'excellent', 'positive', 'fortunate', 'correct', 'superior', 'amazing', 'happy', 'love', 'like']
    negative_words = ['bad', 'terrible', 'poor', 'negative', 'unfortunate', 'wrong', 'inferior', 'awful', 'sad', 'hate', 'dislike']

    words = comment.lower().split()
    sentiment_score = 0

    for word in words:
        if word in positive_words:
            sentiment_score += 1
        elif word in negative_words:
            sentiment_score -= 1

    max_score = 5
    normalized_sentiment_score = (sentiment_score / max_score) * 5

    normalized_sentiment_score = min(max(normalized_sentiment_score, 0), 5)

    return normalized_sentiment_score
