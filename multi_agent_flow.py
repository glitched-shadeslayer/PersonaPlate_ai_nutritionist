import sglang as sgl
from time import time
from sglang import RuntimeEndpoint, set_default_backend


set_default_backend(RuntimeEndpoint(f"http://localhost:{30000}"))
@sgl.function
def nutri_agent(s, user): #Adding async here is not working
    s += sgl.system("You are a expert nutritionist agent and provide output for required daily nutrients based on the medical history of the given patient with hypertension.")
    s += sgl.user(f"Generate a list of daily nutrient targets for a given user {user} with hypertension and a sedentary lifestyle based on the DASH diet.")
    s += sgl.assistant(sgl.gen("answer", max_tokens=16384))
    # print('--------Agent----------')

@sgl.function
def recipe_agent(s, constraints, critical_comments = None, previous_plan = None): #Adding async here is not working
    s += sgl.system("You are a expert vegetarian and Indian food plans recipe generation agent and provide output for recipes based on the given constraints for just 3 meals a day which includes breakfast, lunch and dinner, with meal nutrition values.")
    if critical_comments:
        s += sgl.user(f"Generate a 1-day meal plan meet the following constraints {constraints} and includes diverse cuisines, vegetarian, Indian food plans. Also consider the critical comments {critical_comments} and previous meal plan {previous_plan}.")
    else:
        s += sgl.user(f"Generate a 1-day meal plan meet the following constraints {constraints}.")
    s += sgl.assistant(sgl.gen("answer", max_tokens=16384))
    # print('--------Agent----------')
    
@sgl.function
def optimization_agent(s, meal_plan, constraints, critical_comments = None, previous_plan = None): #Adding async here is not working
    s += sgl.system("You are a expert vegetarian and Indian food plans optimization agent which review the meal plan and provide updated meal plan as an output based on the given constraints for just 3 meals a day which includes breakfast, lunch and dinner, with meal nutrition values.")
    if critical_comments:
        s += sgl.user(f"Optimize the following meal plan {meal_plan} to meet the following nutrition goals: {constraints}. Also consider the critical comments {critical_comments} and previous meal plan {previous_plan}.")
    else:
        s += sgl.user(f"Optimize the following meal plan {meal_plan} to meet the following nutrition goals: {constraints}.")
    s += sgl.assistant(sgl.gen("answer", max_tokens=16384))
    # print('--------Agent----------')
    
@sgl.function
def feedback_agent(s, user, meal_plan):
    s += sgl.system("You are a expert feedback agent which review the (user medical history and provide meal plan) as an output provided 5 critical comments for the meal plan revision.")
    s += sgl.user(f"Check if the key requirement for meal to remove hypertension with user medical condition {user} is satisfied to not take any medicine and maintain hypertension well below. Provide necessary feedback for the following meal suggestion {meal_plan} .")
    s += sgl.assistant(sgl.gen("answer", max_tokens=8192))
    # print('--------Agent----------')
    
    
User_profile = "User profile: Age: 31, Diagnosis: Essential Hypertension (Stage 1), Duration of Hypertension: 5 years, Comorbidities: None (or list: diabetes, obesity, etc.), Blood Pressure Readings: Average 162/88 mm Hg (recent readings), Symptoms: Occasional headaches, mild shortness of breath; no chest pain, BMI: 31 kg/m² (Obese category), Relevant Laboratory Tests:, Electrocardiogram (ECG): Normal, Lipid Profile: Mildly elevated cholesterol, Kidney Function: Normal, Blood Glucose: Normal"

nutri_response = nutri_agent(User_profile)
# print(nutri_response['answer'])
recipe_response = recipe_agent(nutri_response['answer'])
print(recipe_response['answer'])
optimization_response = optimization_agent(recipe_response['answer'], nutri_response['answer'])
# print(optimization_response['answer'])
feedback_response = feedback_agent(User_profile, optimization_response['answer'])
# print(feedback_response['answer'])

for _ in range(2):
    recipe_response = recipe_agent(nutri_response['answer'], feedback_response['answer'], recipe_response['answer'])
    # print(recipe_response['answer'])
    optimization_response = optimization_agent(recipe_response['answer'], nutri_response['answer'], feedback_response['answer'], optimization_response['answer'])
    # print(optimization_response['answer'])
    feedback_response = feedback_agent(User_profile, optimization_response['answer'])
    # print(feedback_response['answer'])
    
print('########################')
print('Final meal plan:', recipe_response['answer'])
print('#########################')
# print('Final optimization:', optimization_response['answer'])
# print('Time per request:', time()-start, 'secs')