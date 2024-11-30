import tkinter as tk
from tkinter import messagebox, simpledialog
import uuid
import datetime
import google.generativeai as genai

class PatientManagementSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Patient Management System")
        self.geometry("400x300")
        self.patient_db = {}
        self.configure(bg="lightblue")

        # Menu
        self.menu_label = tk.Label(self, text="What would you like to do?")
        self.menu_label.pack(pady=10)
        self.menu_label.configure(bg="lightblue")
        self.add_patient_button = tk.Button(self, text="Add Patient Data", command=self.add_patient)
        self.add_patient_button.pack(pady=5)
        self.get_diagnosis_button = tk.Button(self, text="Get Diagnosis for Patient", command=self.get_diagnosis)
        self.get_diagnosis_button.pack(pady=5)
        self.retrieve_patient_button = tk.Button(self, text="Retrieve Patient Data", command=self.retrieve_patient)
        self.retrieve_patient_button.pack(pady=5)
        self.exit_button = tk.Button(self, text="Exit", command=self.quit)
        self.exit_button.pack(pady=5)

    def add_patient(self):
        first_name, last_name, age, sex, addictions, diet, prev_diagnosises, symptoms = self.form()
        if first_name and last_name and age and sex and diet and symptoms:
            patient_id = self.generate_patient_id(first_name, last_name)
            patient_info = {
                "patient_id": patient_id,
                "first name": first_name,
                "last name": last_name,
                "age": age,
                "sex": sex,
                "addictions": addictions,
                "diet": diet,
                "previous_diagnoses": prev_diagnosises,
                "symptoms": symptoms
            }
            self.patient_db[patient_id] = patient_info
            messagebox.showinfo("Patient Added", f"Patient ID: {patient_id}")
        else:
            messagebox.showwarning("Incomplete Data", "Please fill out all required fields.")

    def get_diagnosis(self):
        user_id = simpledialog.askstring("Input", "Enter Patient ID:")
        if user_id in self.patient_db:
            patient_dict = self.patient_db[user_id]    
            response =  self.generate_diagnosis(patient_dict["age"], patient_dict["sex"], patient_dict["addictions"], patient_dict["diet"], patient_dict["previous_diagnoses"], patient_dict["symptoms"])
            messagebox.showinfo("Diagnosis", f"""Patient {user_id}:
{response}""")



    def retrieve_patient(self):
        user_id = simpledialog.askstring("Input", "Enter Patient ID:")
        if user_id in self.patient_db:
            patient_dict = self.patient_db[user_id]
            data = simpledialog.askstring("Input", "What data would you like to see (age, sex, addictions, diet, previous diagnoses, symptoms):")
            if data in patient_dict:
                messagebox.showinfo("Patient Data", f"{data.capitalize()} of Patient {user_id}: {patient_dict[data]}")
            else:
                messagebox.showwarning("Invalid Data", "Invalid data requested.")
        else:
            messagebox.showwarning("Not Found", "Patient not found.")

    def form(self):
        #ensures first name is inputed and is a letter
        while True:
            first_name = simpledialog.askstring("Input", "First name:").strip().capitalize()
            if not first_name:
                messagebox.showwarning("Error", "Please enter a value.")
                continue
            else:
                break
        #ensures last name is inputed and is a letter
        while True:
            last_name = simpledialog.askstring("Input", "Last name:").strip().capitalize()
            if not last_name:
                messagebox.showwarning("Error", "Please enter a value.")
                continue
            else:
                break
        #ensures age is inputed and is a number
        age = simpledialog.askinteger("Input", "Age:")

        #ensures sex is inputed and is a letter and is either male or female
        while True:
            sex = simpledialog.askstring("Input", "Sex (male/female):").strip().lower()
            #checks if user input is in the list
            if sex not in ["male","female"]:  
                messagebox.showwarning("Error", "Invalid Input")
                continue
            else:
                break
        #ensures addictions is inputed and is a letter
        while True:
            addictions = simpledialog.askstring("Input", "Addictions (if none, put 'none'):").strip()
            if not addictions:
                messagebox.showwarning("Error", "Please enter a value.")
                continue
            else:
                break
        #ensures diet is inputed and is a letter
        while True:
            diet = simpledialog.askstring("Input", "Diet (vegetarian, vegan, balanced, fiberous, lacking fiber, carnivorous):").strip().lower()
            #checks if user input is in the list
            if diet not in ["vegetarian", "vegan", "balanced", "fiberous", "lacking fiber","carnivorous"]:  
                messagebox.showwarning("Error", "Invalid Input")
                continue
            else:
                break  
        #ensures previous diagnosises is inputed and is a letter
        while True: 
            prev_diagnosises = simpledialog.askstring("Input", "Previously diagnosed health conditions (if none, put 'none'):").strip()
            if not prev_diagnosises:
                messagebox.showwarning("Error", "Please enter a value.")
                continue
            else:
                break
        #gives example symptoms
        messagebox.showinfo("Symptom list:","""
        Abdominal Pain, Acid Reflux, Airsickness, Bad Breath, Belching, Bleeding, Breathing Problems, Bruises, Chest Pain, Choking, Chronic Pain, Constipation, Cough, Dehydration, Diarrhea, Dizziness and Vertigo, Edema, Fainting, Fatigue, Fever, Gas, Gastrointestinal Bleeding, Headache, Heartburn, Heat Illness, Hives, Hypothermia, Indigestion, Itching, Jaundice, Motion Sickness, Nausea and Vomiting, Pain, Pelvic Pain, Sciatica, Shortness of Breath, Speech and Communication Disorders, Stuttering, Sunstroke, Swelling, Thirst, Vaginal Bleeding, Vertigo, Vomiting, Wheezing""")
        
        #ensures symptoms is inputed and is a letter  

        while True: 
            symptoms = simpledialog.askstring("Input", "Symptoms:").strip()
            if not symptoms:
                messagebox.showwarning("Error", "Please enter a value.")
                continue
            else:
                break
                
        return first_name, last_name, age, sex, addictions, diet, prev_diagnosises, symptoms

    def generate_patient_id(self, first_name, last_name):
        unique_id = uuid.uuid4().hex[:6]
        current_date = datetime.datetime.now().strftime("%Y%m%d")
        patient_id = f"{first_name[0].upper()}{last_name[0].upper()}{current_date}{unique_id}"
        return patient_id

    def generate_diagnosis(self, age, sex, addictions, diet, prev_diagnosises, symptoms):
        genai.configure(api_key='AIzaSyAHdQ0JhwmZVua1gyk59nouP4sw7xEks78')
        generation_config = {
          "temperature": 1,
          "top_p": 0.95,
          "top_k": 64,
          "max_output_tokens": 8192,
          "response_mime_type": "text/plain",
        }
        model = genai.GenerativeModel(
          model_name="gemini-1.5-pro",
          generation_config=generation_config,
          # safety_settings = Adjust safety settings
          # See https://ai.google.dev/gemini-api/docs/safety-settings
        )
        
        if addictions.strip() == "none":
            prompt = f"input: What does {symptoms} mean for a {age} year old {sex} with no addictions and a {diet} diet and previously {prev_diagnosises}?"
        else:
            prompt = f"input: What does {symptoms} mean for a {age} year old {sex} with an addiction to {addictions} and a {diet} diet and previously {prev_diagnosises}"
            
        response = model.generate_content([
                                           "input: What does fatigue and weight loss mean for a 45-year-old male with no addictions and a vegetarian diet and previously diagnosed with hypertension and type 2 diabetes?",
                                           "output: These symptoms could indicate uncontrolled diabetes or potential complications such as chronic kidney disease or an undiagnosed thyroid disorder. A thorough medical evaluation, including blood tests and possibly imaging, is recommended to determine the exact cause.",
                                           "input: What does persistent cough and shortness of breath mean for a 60-year-old female with no addictions and a balanced diet and previously diagnosed with COPD?",
                                           "output: These symptoms are likely related to a flare-up or worsening of COPD. It could also indicate a respiratory infection or other complications such as heart failure. Immediate medical attention is advised to manage symptoms and prevent further complications.",
                                           "input: What does joint pain and swelling mean for a 30-year-old female with no addictions and a paleo diet and previously diagnosed with rheumatoid arthritis?",
                                           "output: These symptoms are likely due to an active phase of rheumatoid arthritis. It may require adjustments in her current treatment plan, including medications and lifestyle changes. Consulting with a rheumatologist would be beneficial.",
                                           "input: What does abdominal pain and nausea mean for a 50-year-old male with no addictions and a Mediterranean diet and previously diagnosed with GERD and peptic ulcer?",
                                           "output: The symptoms could signify a recurrence or worsening of his peptic ulcer disease or complications such as a perforation or bleeding. It's important to seek medical evaluation promptly to determine the cause and appropriate treatment.",
                                           "input: What does headache and dizziness mean for a 25-year-old female with no addictions and a vegan diet and previously diagnosed with anemia?",
                                           "output: These symptoms may suggest a recurrence or worsening of anemia. It could also indicate other conditions such as migraine or a vestibular disorder. A complete blood count (CBC) and possibly other investigations are recommended to diagnose and manage the underlying cause.",
                                           "input: What does frequent urination and increased thirst mean for a 35-year-old male with no addictions and a balanced diet and no previous diagnoses?",
                                           "output: These symptoms could be indicative of diabetes mellitus, particularly type 2 diabetes. It is advisable to have blood glucose levels checked through fasting blood sugar and HbA1c tests to confirm the diagnosis and begin appropriate management if necessary.",
                                           "input: What does constant coughing and shortness of breath mean for a 45-year-old male who is addicted to smoking, has a poor diet, and previously had chronic bronchitis?",
                                           "output: These symptoms could indicate Chronic Obstructive Pulmonary Disease, Lung Cancer, and Pneumonia. The history of chronic bronchitis and smoking significantly increases the risk of developing COPD. Persistent coughing and shortness of breath are also common symptoms of lung cancer, especially in smokers. Although less likely due to the chronic nature of the symptoms, recurrent infections could lead to pneumonia.",
                                           "input: What does frequent urination and extreme thirst mean for a 60-year-old female who is addicted to sugary foods, has a high-calorie diet, and previously had gestational diabetes?",
                                           "output: These symptoms could indicate Type 2 Diabetes Mellitus, Diabetes Insipidus, or an Urinary Tract Infection (UTI). The dietary habits and previous gestational diabetes history increase the risk of developing Type 2 Diabetes. Diabetes Insipidus, although less common, is also characterized by similar symptoms due to different underlying mechanisms. Frequent urination can sometimes be associated with a UTI, although it typically does not cause extreme thirst.",
                                           "input: What does persistent fatigue and unexplained weight loss mean for a 35-year-old male who is addicted to alcohol, has a vegetarian diet, and previously had hepatitis B?",
                                           "output: These symptoms could indicate Liver Cirrhosis, Liver Cancer, Malnutrition or Vitamin Deficiency, or Chronic Fatigue Syndrome. The combination of alcohol addiction and a previous hepatitis B diagnosis significantly raises the risk of liver cirrhosis. A previous hepatitis B infection and alcohol addiction also increase the risk of developing liver cancer. Despite a vegetarian diet, alcohol addiction can lead to poor nutrient absorption, causing fatigue and weight loss. Although less likely given the history, it is another potential cause of persistent fatigue.",
                                           "input: what does fatigue, weight loss, and increased thirst mean for a 45 year old male with no addictions, a vegan diet and no previous diagnoses?",
                                           "output: These symptoms could indicate a possible diagnosis of type 2 diabetes. Other potential conditions could include thyroid disorders or other metabolic issues. A thorough medical evaluation would be necessary to determine the exact cause.",
                                           prompt,
                                           "output: ",
                                         ])
        
        return response.text

if __name__ == "__main__":
    app = PatientManagementSystem()
    app.mainloop()

#47 to 57 and 147 to 155
