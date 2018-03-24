from django.utils import timezone


def update_predictions_points(match):
    # log("Match was updated - recalculated all predictions for match: ", match)
    result1 = match.result1
    result2 = match.result2
    start_date = match.start_date

    for prediction in match.prediction_set.all():
        calculate_points_for_prediction(result1, result2, prediction, start_date)


def calculate_points_for_prediction(result1, result2, prediction, start_date):
    old_points = prediction.points
    if not old_points:
        old_points = 0

    points = 0
    if (result1 is None or result1 < 0) or (result2 is None or result2 < 0) or timezone.now() < start_date:
        prediction.points = points
        prediction.correct1 = False
        prediction.correct2 = False
        prediction.correct_type = False
        prediction.correct_result = False
        prediction.save()
    else:
        prediction1 = prediction.result1
        prediction2 = prediction.result2
        if (prediction1 is None) or (prediction2 is None):
            pass
        else:
            if prediction1 == result1:
                points += 1
                prediction.correct1 = True
            else:
                prediction.correct1 = False

            if prediction2 == result2:
                points += 1
                prediction.correct2 = True
            else:
                prediction.correct2 = False

            if prediction1 == result1 and prediction2 == result2:
                points += 1
                prediction.correct_result = True
            else:
                prediction.correct_result = False

            if (prediction1 == prediction2 and result1 == result2) or \
                    (prediction1 > prediction2 and result1 > result2) or \
                    (prediction1 < prediction2 and result1 < result2):
                points += 2
                prediction.correct_type = True
            else:
                prediction.correct_type = False

        prediction.points = points
        prediction.save()

    diff = points - old_points
    if diff == 0:
        pass
    else:
        typer_card = prediction.typer_card
        typer_card.points += diff
        typer_card.save()


def format_result1(m, sign="-"):
    return m.result1 if m.result1 is not None and m.result1 != -1 else sign


def format_result2(m, sign="-"):
    return m.result2 if m.result2 is not None and m.result2 != -1 else sign


def prediction_row(predictions_dict, p, m):
    predictions_dict['id'] = m.id
    predictions_dict['team1'] = m.team1.name
    predictions_dict['team2'] = m.team2.name
    predictions_dict['start_date'] = m.start_date
    if predictions_dict.get('disabled'):
        predictions_dict['prediction1'] = format_result1(p)
        predictions_dict['prediction2'] = format_result2(p)
        predictions_dict['result1'] = format_result1(m)
        predictions_dict['result2'] = format_result2(m)
        predictions_dict['correct1'] = 1 if p.correct1 else 0
        predictions_dict['correct2'] = 1 if p.correct2 else 0
        predictions_dict['correct_type'] = 2 if p.correct_type else 0
        predictions_dict['correct_result'] = 1 if p.correct_result else 0
    else:
        predictions_dict['prediction1'] = format_result1(p, '')
        predictions_dict['prediction2'] = format_result2(p, '')

    return predictions_dict


def empty_prediction_row(predictions_dict, m):
    predictions_dict['id'] = m.id
    predictions_dict['team1'] = m.team1.name
    predictions_dict['team2'] = m.team2.name
    predictions_dict['start_date'] = m.start_date
    if predictions_dict.get('disabled'):
        predictions_dict['prediction1'] = "-"
        predictions_dict['prediction2'] = "-"
        predictions_dict['result1'] = format_result1(m)
        predictions_dict['result2'] = format_result2(m)
        predictions_dict['correct1'] = "-"
        predictions_dict['correct2'] = "-"
        predictions_dict['correct_type'] = "-"
        predictions_dict['correct_result'] = "-"
    else:
        predictions_dict['prediction1'] = ''
        predictions_dict['prediction2'] = ''

    return predictions_dict
