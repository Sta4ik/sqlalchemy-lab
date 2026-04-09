from sqlalchemy import create_engine, Column, Integer, Date, ForeignKey, NVARCHAR, text
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import credits as cred

engine = create_engine(f"mssql+pymssql://{cred.login}:{cred.password}@localhost:1433/TEST")
Base = declarative_base()

# 1 и 2 Задание

class Group(Base):
    __tablename__ = "GROUPS"

    id_group = Column(Integer, autoincrement=True, primary_key=True)
    name_group = Column(NVARCHAR(5))
    course = Column(Integer)

    students = relationship("Student", back_populates="group")
    plans = relationship("Plan", back_populates="group")


class Student(Base):
    __tablename__ = "STUDENTS"

    id_student = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(NVARCHAR(10))
    surname = Column(NVARCHAR(10))
    second_name = Column(NVARCHAR(10))
    birthday = Column(Date)
    groups = Column(Integer, ForeignKey("GROUPS.id_group"))

    group = relationship("Group", back_populates="students")


class Subject(Base):
    __tablename__ = "SUBJECTS"

    id_subject = Column(Integer, autoincrement=True, primary_key=True)
    name_subject = Column(NVARCHAR(50))
    hours = Column(Integer)

    plans = relationship("Plan", back_populates="subject")


class Plan(Base):
    __tablename__ = "PLANS"

    id_group = Column(Integer, ForeignKey("GROUPS.id_group"), primary_key=True)
    id_subject = Column(Integer, ForeignKey("SUBJECTS.id_subject"), primary_key=True)

    group = relationship("Group", back_populates="plans")
    subject = relationship("Subject", back_populates="plans")

Base.metadata.create_all(engine)

# 3 Задание

Session = sessionmaker(bind=engine)
session = Session()

firstGroup = Group(name_group="ПО135", course=1)
secondGroup = Group(name_group="ПО235", course=2)
thirdGroup = Group(name_group="ПО335", course=3)
session.add_all([firstGroup, secondGroup, thirdGroup])
session.commit()

students = [
    Student(name="П", surname="Федоренко", second_name="Р", birthday="1997-12-25", groups=1),
    Student(name="О", surname="Зингед", second_name="", birthday="1985-12-25", groups=1),
    Student(name="Н", surname="Савицкая", second_name="", birthday="1987-09-22", groups=2),
    Student(name="М", surname="Ковальчук", second_name="Е", birthday="1992-06-17", groups=2),
    Student(name="Т", surname="Ковриго", second_name="Р", birthday="1992-05-13", groups=3),
    Student(name="Н", surname="Шарапо", second_name="", birthday="1992-08-14", groups=3),
]
session.add_all(students)
session.commit()

subject = [
    Subject(name_subject="Физика", hours=200),
    Subject(name_subject="Математика", hours=120),
    Subject(name_subject="Основы алгоритмизации", hours=70),
    Subject(name_subject="Проектирование БД", hours=130),
    Subject(name_subject="Средства визуального программирования", hours=90),
    Subject(name_subject="Объектно-ориентированное программирование", hours=70),
]
session.add_all(subject)
session.commit()

plan = [
    Plan(id_group=1, id_subject=1),
    Plan(id_group=1, id_subject=2),
    Plan(id_group=2, id_subject=3),
    Plan(id_group=2, id_subject=4),
    Plan(id_group=3, id_subject=5),
    Plan(id_group=3, id_subject=6),
]
session.add_all(plan)
session.commit()

# 4 Задание

newGroup = Group(name_group="ПО134", course=1)
session.add(newGroup)
session.commit()

session.query(Plan).filter(Plan.id_group == 1).update({Plan.id_group: 4})
session.commit()

session.query(Student).filter(Student.groups == 1).update({Student.groups: 4})
session.commit()

# 5 Задание

group = session.query(Group).filter(Group.name_group == "ПО135").first()
session.delete(group)
session.commit()

# 6 Задание

firstSubject = session.query(Subject).filter(Subject.name_subject == "Средства визуального программирования").first()
firstSubject.hours = 120

secondSubject = session.query(Subject).filter(Subject.name_subject == "Объектно-ориентированное программирование").first()
secondSubject.hours = 100

session.commit()

# 7 Задание

session.execute(text("ALTER TABLE SUBJECTS ADD EXAM_TYPE NVARCHAR(10)"))
session.commit()

session.execute(text("UPDATE SUBJECTS SET EXAM_TYPE = 'Экзамен' WHERE EXAM_TYPE IS NULL"))
session.commit()

session.execute(text("UPDATE SUBJECTS SET EXAM_TYPE = 'Зачёт' WHERE name_subject = 'Основы алгоритмизации'"))
session.commit()

# 8 Задание

session.execute(text("ALTER TABLE STUDENTS DROP COLUMN SECOND_NAME"))
session.commit()

session.close()