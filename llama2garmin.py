import sqlite3
import pandas as pd
import ollama

def load_data_from_dbs():
    db_paths = {'summary': 'HealthData/DBs/summary.db'}
    data = {}
    with sqlite3.connect(db_paths['summary']) as conn:
        data['df_days_summary'] = pd.read_sql_query("""
            SELECT day, hr_min, hr_max, hr_avg, rhr_avg, steps, steps_goal, 
                sleep_avg, stress_avg, calories_avg 
            FROM days_summary 
            WHERE day BETWEEN '2023-01-01' AND '2023-12-31'
        """, conn)
        data['df_days_summary'] = data['df_days_summary'].apply(pd.to_numeric, errors='coerce', axis=0).fillna(0)
        data['df_days_summary']['day'] = pd.to_datetime(data['df_days_summary']['day'])
            
        data['df_months_summary'] = pd.read_sql_query("""
            SELECT * FROM months_summary
        """, conn)
        data['df_months_summary'] = data['df_months_summary'].apply(pd.to_numeric, errors='coerce', axis=0).fillna(0)
        data['df_months_summary']['first_day'] = pd.to_datetime(data['df_months_summary']['first_day'])
    return data


def create_table(dataframe, title):
    table_str = f"\n{title}:\n"
    table_str += dataframe.to_string(index=False)
    return table_str

def create_observations(data):
    observations = []
    questions = []
    
    daily_summary_table = create_table(data['df_days_summary'], "Daily Summary")
    monthly_summary_table = create_table(data['df_months_summary'], "Monthly Summary")
    
    observations.append(daily_summary_table)
    observations.append(monthly_summary_table)
    
    max_stress_day = data['df_days_summary'].loc[data['df_days_summary']['stress_avg'].idxmax()]
    max_stress_day_str = max_stress_day['day'].strftime('%B %d, %Y')
    max_stress = max_stress_day['stress_avg']
    observations.append(f"Highest average stress was recorded on {max_stress_day_str}: {max_stress}.")

    questions = [
        "How does daily stress correlate with sleep quality and heart rate variability?",
        "Are there any visible trends in heart rate metrics over the months?",
        "Can we correlate calories burned with the step count goal achievement?",
        "What insights can we draw from the relationship between stress and physical activity levels?"
    ]
    
    return observations, questions

def analyze_data_with_ollama(observations, questions):
    prompt = "Here's a comprehensive analysis of my health data for 2023, including daily and monthly summaries:\n"
    prompt += "\n".join(observations) + "\n\n"
    prompt += "Based on these summaries, I have some questions that might help us understand my health patterns better:\n"
    prompt += "\n".join(f"- {q}" for q in questions)
    print("Prompt:")
    print(prompt)
    response = ollama.chat(model='llama2', messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']

def main():
    data = load_data_from_dbs()
    observations, questions = create_observations(data)
    analysis = analyze_data_with_ollama(observations, questions)
    print("Llama2's Analysis:")
    print(analysis)

if __name__ == '__main__':
    main()
