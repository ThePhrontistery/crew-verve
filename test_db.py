from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from .models import Survey_answer
# Set up the database connection (NO ES IGUAL A FLASK. NO ESTAMOS EN UN PROCESO DE FLASK AHORA!!!!)
engine = create_engine('sqlite:///./instance/crewverve.db')
Session = sessionmaker(bind=engine)
session = Session()

#--------------------------------------------------------------------------
print(f"SQLAlchemy example using SQL style select and not the deprecated Query interface")

# Retrieve the user with the name "john" and ID 1
# john = session.execute(select(User).where((User.name == 'john') & (User.id == 1))).scalar_one()
id_survey = 1
#answers = '[1, 1, 2, 1, 2, 2, 2, 3, 4]'
#mood_input = 1
#rating_input = [1,2,1,2,2,2,3,4]
#answers = [mood_input, rating_input]
#print(answers)
#answers_str = str(answers).replace('[', '').replace(']', '')
#print(answers_str)
#print (type(answers_str))
#mood = answers_str[0]
    #sumo el resto de ocurrencias de answer para guardarlo en rating
#rating = sum([int(x) for x in answers_str.split(',')])
##print("mood es ", mood)
##print("rating es ", rating)
#-----------------------------------------
print ("-----------------")
mood_input = '50'
rating0_input = '1'
rating1_input = '2'
rating2_input = '2'
rating3_input = '3'
rating4_input = '2'
rating5_input = '2'
rating6_input = '3'
rating7_input = '3'
answers = f'{mood_input},{rating0_input},{rating1_input},{rating2_input},{rating3_input},{rating4_input},{rating5_input},{rating6_input},{rating7_input}'
#print(answers)
answer = Survey_answer(id_survey=id_survey, answers=answers)
#session.add(answer)
#session.commit()
#----------------------------------------
id_survey = 1
#answers = session.execute(select(Survey_answer.answers).filter_by(id_survey=id_survey)).all()
answer = session.execute(select(Survey_answer.answers).where(Survey_answer.id_survey==id_survey)).scalars().all()
#print(survey_answer[0])     # imprime 2,3,5,2,1,3,4,2,5
#print(survey_answer[1])     # imprime 4,2,4,5,1,1,2,3,5
#print(survey_answer[0][0])
#columna = int(survey_answer[0][0])
#print(type(columna))
#survey_answer_answers = [survey_answer.answers for survey_answer in survey_answer]
#print (survey_answer_answers)
#mood_total = 0
#for i in answer:
#     print (i)
#     mood_total = mood_total + int(i[0])
#     print ("mood total dentro del bucle: ", mood_total)   
#codigo comprimido:
mood_total = sum(int(item_answer[0]) for item_answer in answer)    
participation_total = len(answer) 
#mood_total = (sum(int(element_answer[0])) for element_answer in answer) 
#print ("mood total con la comprensión: ", mood_total)   
#print ("participacion total con la comprensión: ", participation_total)
#
# 
rating_total = 0
for item_answer in answer:
     for e in range(2,17,2):
        rating_total = rating_total + int(item_answer[e])
        print ("e vale: ",e)
        print ("el valor de lo que sumamos : ", int(item_answer[e]))
        #rating_total = rating_total + int(i[2])+ int(i[4])+ int(i[6])+ int(i[8])+ int(i[10])+ int(i[12])+ int(i[14])+ int(i[16])
        print ("rating total dentro del bucle: ", rating_total)

rating_total = sum(int(item_answer[e]) for item_answer in answer for e in range(2,17,2)) 
print ("rating total conprension: ", rating_total)
#     
#rating_total = sum(int(element_answer[2]) for element_answer in answer) 
#print ("rating total con la comprension: ", rating_total)    
#    survey_answer_answers.append(i)
#survey_answer_answers = [survey_answer.answers for survey_answer in survey_answer]
#print("survey_answer_answers ", survey_answer_answers)
#resultado = create_answer(id_survey, answers)
#answer = Survey_answer(id_survey=id_survey, answers=answers)
#session.add(answer)
#session.commit()
#print(answer)

# Retrieve all tasks for a project with ID 1 and associated with John
#tasks = session.execute(select(Task).join(Task.project).join(Project.users).where((Project.id == 1) & (User.id == john.id))).scalars()

# Print the task names
#for task in tasks:
#    print(f"task: {task.name}")

#--------------------------------------------------------------------------
#print(f"SQLAlchemy example more in tune with Flask ORM atterns")

#john = session.execute(select(User).filter_by(id=1)).scalar_one()
#tasks = john.projects[0].tasks

# Print the task names
#for task in tasks:
#    print(f"task: {task.name}")