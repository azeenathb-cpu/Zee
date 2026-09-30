from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.orm import declarative_base, sessionmaker


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

DATABASE_URL = "sqlite:///./fitbuddy_clean.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# --------------------------------------------------
# USER TABLE
# --------------------------------------------------

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    fitness_goal = Column(String(100), nullable=False)
    workout_intensity = Column(String(50), nullable=False)


# --------------------------------------------------
# WORKOUT PLAN TABLE
# --------------------------------------------------

class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, unique=True)
    original_plan = Column(Text, nullable=False)
    updated_plan = Column(Text, nullable=True)
    nutrition_tip = Column(Text, nullable=True)


# Create tables
Base.metadata.create_all(bind=engine)


# --------------------------------------------------
# SAVE USER
# --------------------------------------------------

def save_user(
    user_id,
    username,
    age,
    weight,
    fitness_goal,
    workout_intensity
):

    db = SessionLocal()

    try:
        existing_user = db.query(User).filter(
            User.user_id == user_id
        ).first()

        if existing_user:
            existing_user.username = username
            existing_user.age = age
            existing_user.weight = weight
            existing_user.fitness_goal = fitness_goal
            existing_user.workout_intensity = workout_intensity

            user = existing_user

        else:
            user = User(
                user_id=user_id,
                username=username,
                age=age,
                weight=weight,
                fitness_goal=fitness_goal,
                workout_intensity=workout_intensity
            )

            db.add(user)

        db.commit()
        db.refresh(user)

        return user

    finally:
        db.close()


# --------------------------------------------------
# GET USER
# --------------------------------------------------

def get_user(user_id):

    db = SessionLocal()

    try:
        return db.query(User).filter(
            User.user_id == user_id
        ).first()

    finally:
        db.close()


# --------------------------------------------------
# SAVE PLAN
# --------------------------------------------------

def save_plan(
    user_id,
    workout_plan,
    nutrition_tip
):

    db = SessionLocal()

    try:
        existing_plan = db.query(WorkoutPlan).filter(
            WorkoutPlan.user_id == user_id
        ).first()

        if existing_plan:

            existing_plan.original_plan = workout_plan
            existing_plan.updated_plan = None
            existing_plan.nutrition_tip = nutrition_tip

            plan = existing_plan

        else:

            plan = WorkoutPlan(
                user_id=user_id,
                original_plan=workout_plan,
                updated_plan=None,
                nutrition_tip=nutrition_tip
            )

            db.add(plan)

        db.commit()
        db.refresh(plan)

        return plan

    finally:
        db.close()


# --------------------------------------------------
# GET ORIGINAL PLAN
# --------------------------------------------------

def get_original_plan(user_id):

    db = SessionLocal()

    try:

        plan = db.query(WorkoutPlan).filter(
            WorkoutPlan.user_id == user_id
        ).first()

        if plan:
            return plan.original_plan

        return None

    finally:
        db.close()


# --------------------------------------------------
# UPDATE PLAN
# --------------------------------------------------

def update_plan(
    user_id,
    updated_plan
):

    db = SessionLocal()

    try:

        plan = db.query(WorkoutPlan).filter(
            WorkoutPlan.user_id == user_id
        ).first()

        if plan:
            plan.updated_plan = updated_plan
            db.commit()

        return plan

    finally:
        db.close()


# --------------------------------------------------
# GET ALL USERS
# --------------------------------------------------

def get_all_users():

    db = SessionLocal()

    try:
        return db.query(User).all()

    finally:
        db.close()


# --------------------------------------------------
# GET ALL PLANS
# --------------------------------------------------

def get_all_plans():

    db = SessionLocal()

    try:
        return db.query(WorkoutPlan).all()

    finally:
        db.close()