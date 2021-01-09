# Write your code here
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today().date())

    def __repr__(self):
        return self.task


class Todo:

    def __init__(self, db_session, class_table):
        self.session = db_session
        self.Table = class_table
        self.menu()

    def menu(self):
        menu_choice = input("1) Today's tasks\n2) Week's tasks\n3) All tasks\n"
                            "4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit\n")
        menu_fun = {
            '1': self.today_task,
            '2': self.weeks_task,
            '3': self.all_tasks,
            '4': self.missed_tasks,
            '5': self.add_task,
            '6': self.delete_task,
            '0': self._exit
        }
        try:
            return menu_fun[menu_choice]()
        except KeyError:
            print('Not valid, try again...')
            return self.menu()

    def today_task(self):
        rows = self.session.query(self.Table).filter(self.Table.deadline == datetime.today().date()).all()
        if not rows:
            print('Today:\nNothing to do!\n')
            return self.menu()
        else:
            print('Today:')
            print('\n'.join(map(str, rows)))
            return self.menu()

    def weeks_task(self):
        weekdays = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
        for i in range(0, 7):
            delta_day = datetime.today() + timedelta(days=i)
            rows = self.session.query(self.Table).filter(self.Table.deadline == delta_day.date()).all()
            print(f"{weekdays[delta_day.weekday()]} {delta_day.day} {delta_day.strftime('%b')}")
            if rows:
                [print(row.task) for row in rows]
                print('\n')
            else:
                print('Nothing to do!\n')
        return self.menu()

    def all_tasks(self, deleted_list=False):
        rows = self.session.query(self.Table).order_by(self.Table.deadline).all()
        if deleted_list:
            return rows
        if not rows:
            print('Today:\nNothing to do!\n')
            return self.menu()
        else:
            print('All tasks:')
            for i, row in enumerate(rows, start=1):
                print(f"{i}. {row.task}. {row.deadline.strftime('%-d %b')}")
        print("")
        return self.menu()

    def missed_tasks(self):
        rows = self.session.query(self.Table).filter(self.Table.deadline < datetime.today().date()).\
            order_by(self.Table.deadline).all()
        if not rows:
            print('Missed tasks:\nNothing is missed!\n')
            return self.menu()
        else:
            print("Missed tasks:")
            for i, row in enumerate(rows, start=1):
                print(f"{i}. {row.task}")
        print("")
        return self.menu()

    def add_task(self):
        task = input('Enter task:\n')
        deadline = input('Enter deadline\n')
        try:
            deadline = datetime.strptime(deadline, "%Y-%m-%d") if deadline else None
            new_row = self.Table(task=task, deadline=deadline)
            self.session.add(new_row)
            self.session.commit()
            print('The task has been added!\n')
        except:
            print()
            print('An error occurred, try again\n')
            return self.menu()
        return self.menu()

    def delete_task(self):
        rows = self.all_tasks(deleted_list=True)
        if not rows:
            print('Nothing to delete')
            return self.menu()
        else:
            for i, row in enumerate(rows, start=1):
                print(f"{i}. {row.task}")
            print(len(rows))
            del_choice = int(input('Choose the number of the task you want to delete:'))
            try:
                assert 0 < del_choice <= len(rows), "Wrong choice"
                self.session.query(self.Table).filter(self.Table.id == rows[del_choice-1].id).delete()
                self.session.commit()
                print('The task has been deleted!')
            except AssertionError as e:
                print(e+'\n')
            except:
                print("An error occurred, the tasks hasn't been deleted")
        return self.menu()

    @staticmethod
    def _exit():
        exit('Bye')


engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
Todo(session, Task)
