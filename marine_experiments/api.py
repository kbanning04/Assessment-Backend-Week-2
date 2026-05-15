"""An API for handling marine experiments."""

from datetime import datetime

from flask import Flask, jsonify, request
from psycopg2 import sql

from database_functions import get_db_connection


app = Flask(__name__)

"""
For testing reasons; please ALWAYS use this connection.

- Do not make another connection in your code
- Do not close this connection

If you do not understand this instructions; as a coach to explain
"""
conn = get_db_connection("marine_experiments")


@app.get("/")
def home():
    """Returns an informational message."""
    return jsonify({
        "designation": "Project Armada",
        "resource": "JSON-based API",
        "status": "Classified"
    })


def validate_type(experiment_type: str) -> bool:
    """ Validates if a experiment_type is a valid entry """
    return experiment_type.lower() in {'intelligence', 'obedience', 'aggression'}


def validate_score_over(score: str) -> bool:
    """ Validate if score is an integer in 0 -100 """
    score = int(score)
    if score < 0 or score > 100:
        raise Exception("Invalid input")
    return score


def get_specific_experiments(experiment_type: str, score_over=int):
    with conn.cursor() as cursor:
        query = f"""
        SELECT
            e.experiment_date,
            e.experiment_id,
            et.type_name AS experiment_type,
            CONCAT(ROUND(((e.score / et.max_score)*100), 2), '%') AS score,
            sp.species_name AS species,
            sb.subject_id
        FROM
            subject AS sb
        JOIN
            species AS sp
            USING(species_id)
        JOIN experiment AS e
            USING(subject_id)
        JOIN
            experiment_type AS et
            USING(experiment_type_id)
        WHERE
            et.type_name ILIKE '{experiment_type}'
            AND
            ((e.score / et.max_score)*100) > {score_over};
        """
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def get_all_experiments():
    with conn.cursor() as cursor:
        query = f"""
        SELECT
            e.experiment_date,
            e.experiment_id,
            et.type_name AS experiment_type,
            CONCAT(ROUND(((e.score / et.max_score)*100), 2), '%') AS score,
            sp.species_name AS species,
            sb.subject_id
        FROM
            subject AS sb
        JOIN
            species AS sp
            USING(species_id)
        JOIN experiment AS e
            USING(subject_id)
        JOIN
            experiment_type AS et
            USING(experiment_type_id)
        ORDER BY e.experiment_date DESC;
        """
        cursor.execute(query)
        result = cursor.fetchall()
    return result if result else {}


@app.get("/experiment")
def get_experiment():
    """ Returns the experiments with a percentage above score and of experiment type 'type'."""
    experiment_type = request.args.get("type")
    score_over = request.args.get("score_over")

    if experiment_type is None and score_over is None:
        result = get_all_experiments()
        return result

    elif experiment_type is None:
        experiment_type = 'intelligence'

    if not validate_type(experiment_type):
        return {"error": "Invalid value for 'type' parameter"}, 400

    try:
        validate_score_over(score_over)
    except Exception:
        return {"error": "Invalid value for 'score_over' parameter"}, 400
    score = int(score_over)

    dict = get_specific_experiments(experiment_type, score)
    return dict


def checking_valid_id():
    with conn.cursor() as cursor:
        query = """
            SELECT *
            FROM experiment
            WHERE experiment_id = %(id)s
            """
        cursor.execute(query, {'id': id})
        result = cursor.fetchall()
        if result == []:
            raise Exception("Invalid ID input")
    return id


@app.delete("/experiment/<int:id>")
def delete_experiment(id: int):
    with conn.cursor() as cursor:
        try:
            valid_id = checking_valid_id(id)
        except Exception as e:
            return {"error": str(e)}, 404
        query = """
        DELETE FROM
            experiment
        WHERE
            experiment_id = %(id)s
        RETURNING 
            experiment_id,
            to_char(experiment_date, 'YYYY-MM-DD');
        """
        cursor.execute(query, {'id': valid_id})
        result = cursor.fetchall()
    return result


if __name__ == "__main__":
    app.config["DEBUG"] = True
    app.config["TESTING"] = True

    app.run(port=8000, debug=True)

    conn.close()
