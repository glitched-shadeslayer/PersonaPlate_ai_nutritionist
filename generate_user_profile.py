import sglang as sgl
from time import time
from sglang import RuntimeEndpoint, set_default_backend
from tqdm import tqdm
import json
import argparse
import os

set_default_backend(RuntimeEndpoint(f"http://localhost:{30000}"))

# User_profile = "User profile: Age: 31, Diagnosis: Essential Hypertension (Stage 1), Duration of Hypertension: 5 years, Comorbidities: None (or list: diabetes, obesity, etc.), Blood Pressure Readings: Average 162/88 mm Hg (recent readings), Symptoms: Occasional headaches, mild shortness of breath; no chest pain, BMI: 31 kg/m² (Obese category), Relevant Laboratory Tests:, Electrocardiogram (ECG): Normal, Lipid Profile: Mildly elevated cholesterol, Kidney Function: Normal, Blood Glucose: Normal"
User_profile = "User profile: Age: 45, Diagnosis: Type 2 Diabetes Mellitus, Duration of Diabetes: 8 years, Comorbidities: Hypertension, Obesity (BMI 34 kg/m²), Blood Glucose Readings: Fasting 130–150 mg/dL; Post-prandial 180–200 mg/dL (recent averages), Symptoms: Polyuria, Polydipsia, Occasional blurred vision; no neuropathic pain or foot ulcers, BMI: 34 kg/m² (Obese category), Relevant Laboratory Tests: HbA1c 8.2% (recent), Lipid Profile: Elevated triglycerides (220 mg/dL) and LDL-C (140 mg/dL); HDL-C low (38 mg/dL), Kidney Function: eGFR 75 mL/min/1.73 m² (mildly reduced), Urine Microalbumin: 75 mg/g creatinine (moderately increased), Liver Function Tests: Within normal limits, ECG: Normal sinus rhythm, Retinal Exam: Background diabetic retinopathy (mild)"
@sgl.function
def prompt_generator(s, TYPE_DISEASE, User_profile):
    s += sgl.system(f"You are an expert medical profile generator. You will given a name of disease and you need to generate just one medical profile for given disease with any one stages. Following is an example user profile for user with hypertension - {User_profile}. This is just an example.") 
    s += sgl.user(f"Generate only 1 medical profile for {TYPE_DISEASE}.")
    s += sgl.assistant(sgl.gen("answer", max_tokens=8192))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate user profiles for a specific disease type.")
    parser.add_argument("--type_disease", type=str, required=True, help="Disease type (e.g., Diabetes, Hypertension, Heart Disease, Sleep Disorders, etc.)")
    parser.add_argument("--num_profiles", type=int, default=1, help="Number of user profiles to generate.")
    args = parser.parse_args()
    TYPE_DISEASE = args.type_disease
    NUM_PROFILES = args.num_profiles

    input_profiles_path = "input_profiles.json"
    if os.path.exists(input_profiles_path):
        with open(input_profiles_path, "r") as f:
            input_profiles = json.load(f)
    else:
        input_profiles = {}

    # Generate profiles
    generated_profiles = []
    for _ in tqdm(range(NUM_PROFILES)):
        response = prompt_generator(TYPE_DISEASE, User_profile)
        generated_profiles.append(response['answer'])

    if TYPE_DISEASE in input_profiles:
        input_profiles[TYPE_DISEASE].extend(generated_profiles)
    else:
        input_profiles[TYPE_DISEASE] = generated_profiles

    with open(input_profiles_path, "w") as f:
        json.dump(input_profiles, f, indent=2)