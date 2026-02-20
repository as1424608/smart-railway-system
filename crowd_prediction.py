# crowd_prediction.py

crowd_data = {
    "Train42": [1, 2, 2, 1, 0, 2, 1],
    "Train50": [0, 0, 1, 0, 1, 0, 0],
    "Train60": [2, 2, 2, 2, 1, 2, 2]
}

def predict_crowd(train_id):

    history = crowd_data.get(train_id)

    if not history:
        return "UNKNOWN"

    avg = sum(history) / len(history)

    if avg < 0.7:
        return "LOW"
    elif avg < 1.5:
        return "MEDIUM"
    else:
        return "HIGH"


def suggest_best_train(train_list):

    best_train = None
    best_score = 3

    for train in train_list:
        level = predict_crowd(train)
        score = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}.get(level, 3)

        if score < best_score:
            best_score = score
            best_train = train

    return best_train


def crowd_alert(train_id):

    level = predict_crowd(train_id)

    if level == "HIGH":
        return f"⚠️ Alert: {train_id} is highly crowded!"
    elif level == "MEDIUM":
        return f"ℹ️ Notice: {train_id} has moderate crowd."
    else:
        return f"✅ {train_id} has low crowd. Comfortable travel!"
def confirmation_probability(train_id):

    level = predict_crowd(train_id)

    if level == "LOW":
        return "90%"
    elif level == "MEDIUM":
        return "60%"
    elif level == "HIGH":
        return "30%"
    else:
        return "Unknown"
