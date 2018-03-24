
def validate_prediction(prediction):
    return prediction is not None and prediction.isdigit()


def update_prediction(new_prediction1, new_prediction2, prediction_obj):
    prediction_obj.result1 = new_prediction1
    prediction_obj.result2 = new_prediction2
    prediction_obj.save()


def check_if_updated_needed(new_prediction1, new_prediction2, old_prediction1, old_prediction2):
    return old_prediction1 != new_prediction1 or old_prediction2 != new_prediction2
