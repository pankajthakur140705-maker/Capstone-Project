import json
from sqlalchemy.exc import SQLAlchemyError

from app.database.db import SessionLocal
from app.models.scheme_model import Scheme


# ---------------------------
# LOAD JSON DATA
# ---------------------------
with open("app/data/schemes.json", "r", encoding="utf-8") as file:
    schemes = json.load(file)


# ---------------------------
# DATABASE SESSION
# ---------------------------
db = SessionLocal()

try:
    # Clear old data
    db.query(Scheme).delete(synchronize_session=False)

    scheme_objects = []

    for item in schemes:

        scheme_objects.append(
            Scheme(
                name=item.get("name"),
                category=item.get("category"),
                description=item.get("description"),
                benefits=item.get("benefits"),
                eligibility=item.get("eligibility"),
                keywords=", ".join(item.get("keywords", [])),
                eligibility_tags=", ".join(item.get("eligibility_tags", [])),
                documents_required=", ".join(item.get("documents_required", [])),
                application_link=item.get("application_link"),
                state=item.get("state"),
                min_age=item.get("min_age"),
                max_age=item.get("max_age"),
                max_income=item.get("max_income"),
                type=item.get("type"),
                priority=item.get("priority")
            )
        )

    db.bulk_save_objects(scheme_objects)
    db.commit()

    print("✅ Database initialized successfully.")

except SQLAlchemyError as e:
    db.rollback()
    print("❌ Database error:", str(e))

except Exception as e:
    db.rollback()
    print("❌ Unexpected error:", str(e))

finally:
    db.close()