import sglang as sgl
from time import time
from sglang import RuntimeEndpoint, set_default_backend
from tqdm import tqdm
import json
import argparse

with open("input_profiles.json", "r") as f:
    input_profiles = json.load(f)

set_default_backend(RuntimeEndpoint(f"http://localhost:{30000}"))
@sgl.function
def nutri_agent(s, user, TYPE_DISEASE): #Adding async here is not working
    s += sgl.system("You are a expert nutritionist agent and provide output for required daily nutrients based on the medical history of the given patient with {TYPE_DISEASE}. Always return your response in the following format:\nNutrition Details: ...\nBreakFast: ...\nLunch: ...\nDinner: ...") 
    s += sgl.user(f"Generate a list of daily nutrient targets for a given user {user} with {TYPE_DISEASE} and a sedentary lifestyle based on the DASH diet. Format your response as: Nutrition Details: ... BreakFast: ... Lunch: ... Dinner: ...")
    s += sgl.assistant(sgl.gen("answer", max_tokens=8192))
    # print('--------Agent----------')

@sgl.function
def recipe_agent(s, constraints, critical_comments = None, previous_plan = None): #Adding async here is not working
    s += sgl.system("You are a expert vegetarian and Indian food plans recipe generation agent and provide output for recipes based on the given constraints for just 3 meals a day which includes breakfast, lunch and dinner, with meal nutrition values(calories, protein, carbs, fats, fiber, sodium, sugar, potassium, calcium, magnesium, vitamins) for one day only. ")
    if critical_comments:
        s += sgl.user(f"Generate a 1-day meal plan and nutrition values(calories, protein, carbs, fats, fiber, sodium, sugar, potassium, calcium, magnesium, vitamins) for that day meal meet the following constraints {constraints} and includes diverse cuisines, vegetarian, Indian food plans. Also consider the critical comments {critical_comments} and previous meal plan {previous_plan}.")
    else:
        s += sgl.user(f"Generate a 1-day meal plan and nutrition values(calories, protein, carbs, fats, fiber, sodium, sugar, potassium, calcium, magnesium, vitamins) for that day meal meet the following constraints {constraints}.")
    s += sgl.assistant(sgl.gen("answer", max_tokens=8192))
    # print('--------Agent----------')
    
@sgl.function
def optimization_agent(s, meal_plan, constraints, critical_comments = None, previous_plan = None): #Adding async here is not working
    s += sgl.system("You are a expert vegetarian and Indian food plans optimization agent which review the meal plan and provide updated meal plan as an output based on the given constraints for just 3 meals a day which includes breakfast, lunch and dinner, with meal nutrition values(calories, protein, carbs, fats, fiber, sodium, sugar, potassium, calcium, magnesium, vitamins) for one day only. Always return your response in the following format:\nNutrition Details: ...\nBreakFast: ...\nLunch: ...\nDinner: ...")
    if critical_comments:
        s += sgl.user(f"Optimize the following 1-day meal plan and nutrition values(calories, protein, carbs, fats, fiber, sodium, sugar, potassium, calcium, magnesium, vitamins) for {meal_plan} to meet the following nutrition goals: {constraints}. Also consider the critical comments {critical_comments} and previous meal plan {previous_plan}. Format your response as: Nutrition Details: ... BreakFast: ... Lunch: ... Dinner: ...")
    else:
        s += sgl.user(f"Optimize the following 1-day meal plan and nutrition values(calories, protein, carbs, fats, fiber, sodium, sugar, potassium, calcium, magnesium, vitamins) for {meal_plan} to meet the following nutrition goals: {constraints}. Format your response as: Nutrition Details: ... BreakFast: ... Lunch: ... Dinner: ...")
    s += sgl.assistant(sgl.gen("answer", max_tokens=8192))
    # print('--------Agent----------')
    
@sgl.function
def feedback_agent(s, user, meal_plan, TYPE_DISEASE):
    s += sgl.system("You are a expert feedback agent which review the (user medical history and provide meal plan) as an output provided 5 critical comments for the meal plan revision.")
    s += sgl.user(f"Check if the key requirement for meal to remove {TYPE_DISEASE} with user medical condition {user} is satisfied to not take any medicine and maintain {TYPE_DISEASE} well below. Provide necessary feedback for the following meal suggestion {meal_plan} .")
    s += sgl.assistant(sgl.gen("answer", max_tokens=8192))
    # print('--------Agent----------')
    
    
# @sgl.function
# def get_nutri_agent(s, meal_plan):
#     s += sgl.system("You are an expert meal nutrition values evaluator. Given a meal plan you need to provide output of sodium intake for that day meal. If sodium intake mentioned then get extract that else evaluate sodium intake in that meal plan.") 
#     s += sgl.user(f"Just provide final value and no explanation. Get the sodium intake for the following meal plan {meal_plan}")
#     s += sgl.assistant(sgl.gen("answer", max_tokens=512))
    # print('--------Hypertension Sodium Intake Agent----------')
    
    
@sgl.function
def get_nutri_agent(s, meal_plan):
    s += sgl.system("You are an expert meal nutrition values evaluator. Given a meal plan you need to provide output of calorie and fat intake for that day meal. If data is not present then evaluate the calorie and fat intake in that meal plan. Always return your response as {Calories: ..., Fat: ...}") 
    s += sgl.user(f"Just provide final value and no explanation. Get the calorie and fat intake for given daily meals plan {meal_plan}")
    s += sgl.assistant(sgl.gen("answer", max_tokens=512))
    # print('--------Obesity Calorie and Fat Intake Agent----------')
    

def main(User_profile, TYPE_DISEASE):
    nutri_response = nutri_agent(User_profile, TYPE_DISEASE)
    recipe_response = recipe_agent(nutri_response['answer'])
    optimization_response = optimization_agent(recipe_response['answer'], nutri_response['answer'])
    feedback_response = feedback_agent(User_profile, optimization_response['answer'], TYPE_DISEASE)

    results = {
        "first_nutrition_plan": recipe_response['answer'],
        "intake_first_plan": get_nutri_agent(recipe_response['answer'])['answer']
    }

    for _ in range(3):
        recipe_response = recipe_agent(nutri_response['answer'], feedback_response['answer'], recipe_response['answer'])
        optimization_response = optimization_agent(recipe_response['answer'], nutri_response['answer'], feedback_response['answer'], optimization_response['answer'])
        feedback_response = feedback_agent(User_profile, optimization_response['answer'], TYPE_DISEASE)

    results["final_optimized_meal_plan"] = optimization_response['answer']
    results["intake_final_plan"] = get_nutri_agent(optimization_response['answer'])['answer']
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run multi-agent flow for a specific disease type.")
    parser.add_argument("--type_disease", type=str, required=True, help="Disease type (e.g., Diabetes, Hypertension, Heart Disease, Sleep Disorders, etc.)")
    args = parser.parse_args()
    TYPE_DISEASE = args.type_disease

    all_results = []
    i = 26
    with open("output_results.log", "w") as log_file:
        for profile in tqdm((input_profiles[TYPE_DISEASE][25:])):
            result = main(profile, TYPE_DISEASE)
            result["profile_index"] = i
            # result["user_profile"] = profile
            all_results.append(result)

            log_file.write(f"===== Profile {i} =====\n")
            log_file.write(f"===========First Nutrition Plan:\n{result['first_nutrition_plan']}\n\n")
            log_file.write(f"----------->Intake (Initial Plan):\n{result['intake_first_plan']}\n\n")
            log_file.write(f"===========Final Optimized Meal Plan:\n{result['final_optimized_meal_plan']}\n\n")
            log_file.write(f"------------>Intake (Final Plan):\n{result['intake_final_plan']}\n\n")
            log_file.write("========================\n\n")
            i += 1