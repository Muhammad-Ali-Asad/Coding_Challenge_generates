from src.database.models import SessionLocal, ChallengeQuota
from sqlalchemy.orm import Session

def reset_all_quotas():
    db: Session = SessionLocal()
    try:
        quotas = db.query(ChallengeQuota).all()
        for quota in quotas:
            quota.quota_remaining = 20
            print(f"Reset quota for user {quota.user_id} to 20")
        db.commit()
        print("All quotas reset successfully.")
    except Exception as e:
        print(f"Error resetting quotas: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    reset_all_quotas()
